import difflib
import re
from typing import Literal


DiffType = Literal["equal", "missing", "incorrect", "extra"]


def tokenize(text: str) -> list[str]:
    return re.findall(r"\b[\w']+\b|[^\w\s]", text)


def evaluate_sentence(sentence: str, user_input: str) -> dict:
    original_words = tokenize(sentence)
    user_words = tokenize(user_input)
    matcher = difflib.SequenceMatcher(a=original_words, b=user_words)

    diff: list[dict[str, str | DiffType]] = []
    matched_words = 0

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        expected = " ".join(original_words[i1:i2]).strip()
        actual = " ".join(user_words[j1:j2]).strip()

        if tag == "equal":
            if expected:
                diff.append({"type": "equal", "expected": expected, "actual": actual})
            matched_words += i2 - i1
        elif tag == "delete":
            diff.append({"type": "missing", "expected": expected, "actual": ""})
        elif tag == "replace":
            diff.append({"type": "incorrect", "expected": expected, "actual": actual})
        elif tag == "insert":
            diff.append({"type": "extra", "expected": "", "actual": actual})

    total_words = len(original_words)
    accuracy = round((matched_words / total_words) * 100, 2) if total_words else 100.0

    return {
        "accuracy": accuracy,
        "diff": diff,
        "correct_sentence": sentence,
    }
