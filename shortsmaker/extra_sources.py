"""Public collection adapters. Returned records retain the source page and stated rights."""

import hashlib
import html
import json
import re
import subprocess
import time
import urllib.parse
import urllib.error
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser

from shortsmaker import image_sources, media_library, media_tools


_unavailable_until: dict[str, float] = {}
_brand_pages: dict[str, str | None] = {}


def source_json(name: str, url: str) -> dict:
    if not media_library.source_enabled(name):
        return {}
    cached = image_sources.CACHE / f"source-{hashlib.sha256(url.encode()).hexdigest()}.json"
    try:
        if cached.exists() and time.time() - cached.stat().st_mtime < 86400:
            return json.loads(cached.read_text(encoding="utf-8"))
        if time.time() < _unavailable_until.get(name, 0):
            return {}
        result = json.loads(media_tools.fetch(url, 18))
        cached.parent.mkdir(parents=True, exist_ok=True)
        media_tools.write_json(cached, result)
        media_library.source_status(name, "Available")
        return result
    except urllib.error.HTTPError as error:
        _unavailable_until[name] = time.time() + (900 if error.code == 429 else 300)
        message = ("Rate limited; retry later or configure your own free source key" if error.code == 429 else
                   f"Unavailable: publisher returned HTTP {error.code}")
        media_library.source_status(name, message)
        return {}
    except (OSError, ValueError):
        _unavailable_until[name] = time.time() + 30
        media_library.source_status(name, "Unavailable: request blocked, timed out or invalid response")
        return {}


def candidate(title: str, url: str, small: str, site: str, page: str, rights: str = "", artist: str = "") -> dict:
    rights = str(rights or "Rights not specified")
    credit = "; ".join(filter(None, [str(artist or site), rights, page]))
    return {"title": title, "url": url, "small": small or url, "source": site, "site": site,
            "source_page": page, "license": rights, "credit": credit}


def loc_images(query: str, limit: int = 3) -> list[dict]:
    data = source_json("loc", "https://www.loc.gov/photos/?" + urllib.parse.urlencode(
        {"fo": "json", "q": query, "c": 12}))
    found = []
    for row in data.get("results", []):
        urls = [u for u in row.get("image_url", []) if isinstance(u, str) and u.startswith("http")]
        if not urls:
            continue
        page = row.get("id") or row.get("url") or "https://www.loc.gov/"
        found.append(candidate(row.get("title", query), urls[-1], urls[0], "Library of Congress", page,
                               str(row.get("rights") or "See item rights statement")))
    return found[:limit]


def wellcome_images(query: str, limit: int = 3) -> list[dict]:
    data = source_json("wellcome", "https://api.wellcomecollection.org/catalogue/v2/works?" + urllib.parse.urlencode(
        {"query": query, "availabilities": "online", "workType": "k", "include": "items", "pageSize": 12}))
    found = []
    for row in data.get("results", []):
        thumb = row.get("thumbnail") or {}
        locations = [loc for item in row.get("items", []) for loc in item.get("locations", [])
                     if (loc.get("locationType") or {}).get("id") == "iiif-image"]
        if not locations or not thumb.get("url"):
            continue
        loc = locations[0]
        base = loc.get("url", "").removesuffix("/info.json")
        if not base.startswith("https://"):
            continue
        lic = loc.get("license") or thumb.get("license") or {}
        found.append(candidate(row.get("title", query), base + "/full/1920,/0/default.jpg", thumb["url"],
                               "Wellcome Collection", f"https://wellcomecollection.org/works/{row['id']}",
                               lic.get("label") or lic.get("url"), loc.get("credit")))
    return found[:limit]


def smithsonian_images(query: str, limit: int = 3) -> list[dict]:
    # DEMO_KEY is the Smithsonian's public, low-rate example key, not another person's credential.
    key = media_library.optional_key("smithsonian") or "DEMO_KEY"
    data = source_json("smithsonian", "https://api.si.edu/openaccess/api/v1.0/search?" + urllib.parse.urlencode(
        {"api_key": key, "q": f"{query} AND online_media_type:Images AND media_usage:CC0", "rows": 12}))
    found = []
    for row in (data.get("response") or {}).get("rows", []):
        desc = (row.get("content") or {}).get("descriptiveNonRepeating") or {}
        for item in (desc.get("online_media") or {}).get("media", []):
            if item.get("type") != "Images":
                continue
            resources = item.get("resources") or []
            url = next((r.get("url") for r in resources if r.get("label") in ("High-resolution JPEG", "Screen Image")), None) or item.get("content")
            if not url:
                continue
            usage = item.get("usage") or {}
            page = desc.get("record_link") or f"https://www.si.edu/object/{row.get('id', '')}"
            found.append(candidate(row.get("title", query), url, item.get("thumbnail"), "Smithsonian", page,
                                   usage.get("access") or usage.get("text") or "See item rights statement"))
            break
    return found[:limit]


def europeana_images(query: str, limit: int = 3) -> list[dict]:
    key = media_library.optional_key("europeana")
    if not key:
        media_library.source_status("europeana", "Needs your free Europeana API key; other sources remain available")
        return []
    data = source_json("europeana", "https://api.europeana.eu/record/v2/search.json?" + urllib.parse.urlencode(
        {"wskey": key, "query": query, "qf": "TYPE:IMAGE", "media": "true", "rows": 12}))
    found = []
    for row in data.get("items", []):
        urls = row.get("edmIsShownBy") or []
        if not urls:
            continue
        page = (row.get("edmIsShownAt") or [row.get("guid", "")])[0]
        found.append(candidate((row.get("title") or [query])[0], urls[0], (row.get("edmPreview") or urls)[0],
                               "Europeana", page, ", ".join(row.get("rights") or []),
                               ", ".join(row.get("dataProvider") or [])))
    return found[:limit]


def pixabay_images(query: str, limit: int = 3) -> list[dict]:
    key = media_library.optional_key("pixabay")
    if not key:
        return []
    data = source_json("pixabay_photos", "https://pixabay.com/api/?" + urllib.parse.urlencode(
        {"key": key, "q": query[:100], "image_type": "photo", "safesearch": "true", "per_page": 12}))
    found = []
    for row in data.get("hits", []):
        if not image_sources.on_topic(row.get("tags", ""), query, strict=True) or "ai generated" in row.get("tags", "").lower():
            continue
        if row.get("largeImageURL"):
            found.append(candidate(row.get("tags", query), row["largeImageURL"], row.get("previewURL"), "Pixabay",
                                   row.get("pageURL", "https://pixabay.com/"), "Pixabay Content License", row.get("user")))
    return found[:limit]


class BrandImages(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
        self.links = []
        self.videos = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
            if urllib.parse.urlsplit(attrs["href"]).path.lower().endswith((".mp4", ".webm", ".mov")):
                self.videos.append(attrs["href"])
        if tag in ("video", "source") and attrs.get("src"):
            self.videos.append(attrs["src"])
        if tag == "img":
            url = attrs.get("data-src") or attrs.get("src")
            if url:
                self.images.append((url, attrs.get("alt") or ""))


def brand_page(page: str) -> str | None:
    """Read each configured official page once per run, including a failed/blocked request."""
    if page not in _brand_pages:
        try:
            _brand_pages[page] = media_tools.fetch(page, 15).decode("utf-8", errors="replace")
        except (OSError, ValueError):
            _brand_pages[page] = None
            media_library.source_status("brand_media", "Official site blocked automated access; use media.bat to import saved assets")
    return _brand_pages[page]


def brand_images(query: str, limit: int = 4) -> list[dict]:
    if not media_library.source_enabled("brand_media"):
        return []
    found = []
    for brand in media_library.settings().get("brands", []):
        if not any(alias.lower() in query.lower() for alias in brand.get("aliases", [])):
            continue
        for page in brand.get("pages", [])[:2]:
            parsed = BrandImages()
            raw = brand_page(page)
            if raw is None:
                continue
            parsed.feed(raw)
            # Follow only explicitly configured official pages; never crawl unrelated sites.
            for url, alt in parsed.images:
                url = html.unescape(urllib.parse.urljoin(page, url))
                if not url.startswith("https://") or any(w in (alt + url).lower() for w in ("sprite", "favicon", "hamburger-icon")):
                    continue
                if not any(x in url.lower() for x in (".jpg", ".jpeg", ".png", "scene7.com")):
                    continue
                large = re.sub(r"[?].*$", "", url) if "scene7.com/" in url else url
                found.append(candidate(f"{brand['name']}: {alt or 'official media photograph'}", large, url,
                                       f"{brand['name']} official media", page, "Official media asset; see publisher terms", brand["name"]))
            if found:
                media_library.source_status("brand_media", "Available")
                break
    return list({row["url"]: row for row in found}.values())[:limit]


def brand_films(query: str, limit: int = 2, names=()) -> list[dict]:
    """Official downloadable video links only; no logged-in players or other creators' uploads."""
    if not media_library.source_enabled("brand_media"):
        return []
    found = []
    for brand in media_library.settings().get("brands", []):
        if not any(alias.lower() in query.lower() for alias in brand.get("aliases", [])):
            continue
        for page in brand.get("pages", [])[:2]:
            parser = BrandImages()
            raw = brand_page(page)
            if raw is None:
                continue
            parser.feed(raw)
            for url in dict.fromkeys(parser.videos):
                url = urllib.parse.urljoin(page, html.unescape(url))
                if not url.startswith("https://"):
                    continue
                try:
                    duration = media_tools.duration(url)
                except (OSError, ValueError, subprocess.SubprocessError):
                    continue
                if 3 <= duration <= 1200:
                    found.append({"title": f"{brand['name']} official footage", "src": url, "dur": duration,
                                  "site": f"{brand['name']} official media", "source_page": page,
                                  "credit": f"{brand['name']}; Official media; see publisher terms; {page}",
                                  "category": "advertisement", "crop": "preserve"})
                if len(found) >= limit:
                    return found
    return found


def collection_images(query: str) -> list[dict]:
    """Budgeted queries keep the expanded pool usable on a home PC."""
    result = []
    searches = (wellcome_images, loc_images, smithsonian_images, europeana_images, pixabay_images, brand_images)
    with ThreadPoolExecutor(4) as ex:
        for rows in ex.map(lambda search: search(query), searches):
            result.extend(rows)
    if media_library.source_enabled("local"):
        result.extend(media_library.local_assets(query))
    return result
