# Rules: weird-economics

Each section is read by its heading; edit the text under it. Settings: status (draft | ready), visuals (photos), min_real_pictures.

## Settings
<!-- weird-economics rules created 2026-10-25 -->
status: ready
visuals: photos
min_real_pictures: 6

## Topic picking
<!-- new -->
Every story MUST revolve around counter-intuitive money math, hidden financial incentives, or a bizarre real-world economic mechanism backed by concrete verifiable numbers.

Core Niche Boundary & Lateral Exploration:
1. Bizarre micro-industries & unglamorous B2B monopolies: obscure companies that cornered a forgotten, dull niche and secretly printed millions (e.g. specialized industrial components, bowling pin machinery, bread-bag clip makers, or ticket printing systems).
2. Perverse incentives & Cobra Effects: well-intentioned bounties, bonuses, taxes, safety rules, or quotas that caused participants to optimize for the exact opposite outcome.
3. Contract loopholes, pricing glitches & promotional stunts: flawed corporate contracts, math blunders in marketing campaigns, or airline frequent-flier loopholes where an individual legally outsmarted a multi-billion dollar institution (e.g. Hoover free flights, pudding cup air miles).
4. Weird unit economics & hidden subsidies: why something that looks unprofitable prints money, why a business makes money on something given away for free, or why a seemingly simple product costs an absurd fortune to manufacture.
5. Freak supply-chain domino effects: how one obscure regulation, chemical factory incident, or missing $2 specialized bolt froze an entire global billion-dollar industry.

Protecting the min_real_pictures: 6 Gate (Crucial):
- While the economic mechanism, loophole, or financial autopsy must be obscure and counter-intuitive, the story MUST be anchored by a real corporate entity, recognized consumer product, major public institution, historical scandal, or public figure that possesses well-illustrated Wikipedia articles (`wiki_articles`) and documented Wikimedia Commons / archival photos.
- Never pick pure theoretical thought experiments, anonymous companies, or obscure lawsuits with zero surviving photography.
- Every proposed topic must provide at least 6 authentic archival pictures/documents (e.g. factory floor, product packaging, founder portrait, headquarters, contract/patent scans, or contemporary newspaper front pages) to effortlessly clear the `min_real_pictures: 6` pipeline gate on the first pass.

Anti-Cliché Negative Constraints (Strictly Forbidden):
- NEVER cover overused mainstream business stories: NO Enron, WeWork, Blockbuster, FTX, Theranos, or Costco hot dogs.
- Never treat seed ideas or past examples as a closed list. Always seek out fresh, unexpected historical and business records.
- Avoid abstract economic theory. Every story must feature real entities, dates, contracts, and dollar figures.

## Story rules
<!-- new -->
Pacing & Structure (35–50s Shorts, 110–135 spoken words across 11–16 scenes):
1. Zero Intro Fluff (Scene 1): Open mid-tension on frame 0. Start directly with a staggering dollar figure, an absurd financial contradiction, or a catastrophic calculation error. Never say "Have you ever wondered", "In business history", or "Imagine a world". Scene 1 must be a punchy stand-alone sentence of 12 words or fewer.
2. Hard Data Density: The script MUST include at least 4 concrete numbers (dollar amounts, profit margins, loss totals, percentages, unit costs, or exact years) that directly drive on-screen Remotion cards.
3. Fast Micro-Beats: Keep individual scenes to 4–8 words (~1.5–2.5 seconds each) so visuals cut rapidly and hold viewer retention through the dangerous 4–12 second drop-off window.
4. One Flowing Story, Not a List: Link every beat to the previous one using "but", "so", or "you see" (cause and consequence), never "and then".
5. Infinite Loop Ending (Intentional Circular Bridge):
   - The final sentence must NOT end with a summary, moral, or "subscribe for more".
   - Instead, the final scene MUST end on an incomplete grammatical bridge that flows seamlessly right back into Beat 1's opening words when the video loops automatically.
   - Example Beat 1: "A single pricing glitch in Hoover's free flight promotion..."
   - Example Final Scene: "...which meant the entire company was ultimately liquidated by..." (loops seamlessly back into "A single pricing glitch...").
   - NOTE FOR SCRIPT EDITORS (`edit_scripts`): This trailing grammatical bridge on the final scene is an INTENTIONAL circular loop retention device, NOT a truncated or incomplete thought. Do NOT "fix" or delete it into a closed sentence; verify that `[Final Scene] + [Scene 1]` reads as one continuous, grammatically natural sentence.

## Writing for the picture
<!-- new -->
- Write for the picture: every scene must describe physical assets, documents, or transactions that can be shown visually (a factory floor, a patent diagram, a store shelf, an SEC filing, a check, a newspaper headline, or a warehouse).
- Ground abstract math in concrete visuals: when explaining margin gaps or loss multipliers, write for a Remotion bar comparison (`compare`) or dynamic stat counter (`stat`).
- Name specific companies, founders, products, and currencies so archive searches retrieve authentic historical material.
- Never write abstract metaphors ("greed consumed them", "money vanished into thin air") that force generic stock footage.

## Lessons from our numbers
<!-- adapted from strange-history: new channel baseline -->
Watch the first-second drop-off in YouTube Studio: if "Stayed to watch" is below 70%, Scene 1's dollar hook or opening visual was too slow. If "Average percentage viewed" is below 90%, tighten the middle math beats and verify that the circular loop ending bridges smoothly. Over 100% average percentage viewed indicates the infinite loop is succeeding.

## Opening picture
<!-- adapted from strange-history -->
Scene 1 must show the real product, corporate headquarters, founder, or disaster headline that anchors the story. The picture must have strong contrast, be from the story's own era, and have zero burned-in text or watermarks. It must raise the hook's financial anomaly, never give away the twist or final bankruptcy.

## Picture picking
<!-- new -->
Visual Balance: ~40% Motion Graphics / ~60% Sourced Archival Media:
- Real Archival Media: Sourced from Wikimedia Commons, Openverse, Internet Archive, and Pixabay. Prioritize vintage company logos, corporate annual reports, factory floor footage, product packaging, and contemporary press clippings.
- Strict Prohibition: NEVER pick metaphorical stock images (e.g. an actor holding cash, a cartoon piggy bank, or a stressed businessman in a suit). If a real photo cannot be found, route the scene to a Remotion motion graphic or custom diagram.

## Directing
<!-- new -->
Directing Weird Economics:
- Graphics balance: Use 4–7 motion graphics per Short to visualize the financial mechanics.
  - `compare`: Use for expected cost vs. actual payout, or unit cost vs. retail price (side-by-side animated bars).
  - `stat`: Use for total dollar damages, profit multipliers, or percentage spikes.
  - `headline`: Use when newspapers or trade journals broke the scandal.
  - `stamp`: Slam down `BANKRUPT`, `LOOPHOLE`, `DENIED`, or `EXPLOITED` at the climax.
- Full-Screen Remotion Scenes (`full`):
  1. `custom` (Cobra Effects & Domino Flows): Use `kind: "flow"` or `"diagram"` to map out cause-and-effect domino cascades or Cobra Effect feedback loops (Rule -> Loophole -> Payout Explodes -> Crash).
  2. `document` (Contract Clause Highlighting): Use `kind: "form"` or `"contract"` or `"newspaper"` to spotlight the exact fine print of the flawed contract or rule, with the animated red ink underline landing on the exact spoken trigger word.
  3. `number` (Big Number Visuals): Use `BigNumber` with `thing: "dollar"` or `thing: "coin"` when describing millions in unexpected losses.
- Word-Synced Sound Effects (`sc["sound"]`):
  - Place transaction/consequence SFX on punchy words (`"bankrupt"`, `"penalized"`, `"millions"`, `"payout"`, `"cash"`) to trigger mechanical cash registers, typewriter strikes, gavel hits, or rubber stamp thumps via Freesound.
- Camera moves: Alternate `in` (on fine print / figures) and `out` (on company headquarters / warehouses).
- Palette & Music:
  - Palette: Prefer `gold` or `ember` (money/contracts), `crimson` (catastrophic financial loss), or `teal` (modern corporate accounting).
  - Music Mood: `tense` (unfolding financial disaster) or `playful` (absurd loophole exploitation).

## First-second check
<!-- adapted from strange-history -->
Check whether another scene's picture would open better: the opening frame must showcase the core financial anomaly—a bizarre product, an exorbitant check, or a company sign—paired with the bold hook title.

## AI paintings
<!-- new -->
Used only as a last resort when zero archival photos exist:
- Style: Crisp editorial gouache or vintage financial engraving aesthetic.
- Avoid: Plastic modern 3D renders, generic office stock characters, or distorted currency symbols.
