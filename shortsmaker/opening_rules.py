"""Shared opening instructions: show the hook while protecting what the narration reveals later."""

import json

from shortsmaker import plan_rules


GUIDANCE = """PROTECT THE UNANSWERED QUESTION (all opening styles):
Show the strange situation promised by the opening narration, but withhold the new answer that the ending
reveals. Check the actual picture, animation, props, document text, signs, labels, arrows and hook title together.
An unlabelled but unmistakable answer object can spoil it too. Reveal each withheld fact only when its narration
reveals it. Do not hide the person, place, object or fact that the opening already states.
Example: when the hook says a Niagara survivor slips and the ending says an orange peel tripped him, show the
loss of balance or reaction with the cause outside the frame. Do not draw the peel or label it ORANGE PEEL early.
Do not replace it with a different invented cause. Show danger/action clearly from frame 0 without a quiet setup.
Use only facts from the story; a whole-story diagram, answer label or ending montage is not an opening."""


def opening_brief(short: dict) -> str:
    scenes = short.get("scenes") or []
    lines = [str(sc.get("narration") or "") for sc in scenes if isinstance(sc, dict)] or short.get("lines") or []
    read = short.get("story_read") or {}
    question = read.get("question", "") if isinstance(read, dict) else ""
    return (GUIDANCE + "\nOpening narration: " + json.dumps(plan_rules.first_sentence(lines), ensure_ascii=False)
            + "\nUnanswered question: " + json.dumps(question or "Infer it from the opening and ending", ensure_ascii=False)
            + "\nEnding narration (context only; protect its new answer): " + json.dumps(lines[-2:], ensure_ascii=False))
