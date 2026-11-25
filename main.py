#!/usr/bin/env python3
"""Unsent: The Micro-Confession Sprint entry.

Writes one original two-part micro-confession to /output/entry.txt:
a To: line naming who it was meant for, and the unsent message itself,
one line written exactly as it was typed, with no explanation after it.

The confession is built from two fragments: the admission (the speaker
broke Dad's guitar and let his brother take the blame) and the reason it
stayed in drafts (saying sorry would mean admitting he snuck out that
night — too afraid, too late). ``assemble`` joins the To: line and the
message; ``validate`` checks the entry gate before anything is written.

Standard library only, no network, no input.
"""

from pathlib import Path

TO_LINE = "To: my older brother"

ADMISSION = "I was the one who broke Dad's guitar, not you."
REASON = (
    "I let you take the blame for a year because saying sorry meant "
    "admitting I was the one who snuck out that night."
)

OUTPUT_PATH = Path("/output/entry.txt")


def assemble(to_line: str, admission: str, reason: str) -> str:
    """Join the To: line and the one-line message into the entry text."""
    return f"{to_line}\n{admission} {reason}"


def validate(text: str) -> str:
    """Check the entry meets the gate before it is written.

    File must be 1-260 characters of UTF-8 text, not only whitespace;
    the message itself must be one line of at most 200 characters.
    Raises ValueError otherwise.
    """
    if not 1 <= len(text) <= 260:
        raise ValueError(f"entry must be 1-260 characters, got {len(text)}")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    text.encode("utf-8")
    lines = text.split("\n")
    if len(lines) != 2:
        raise ValueError("entry must be exactly two parts: To: line + message")
    if not lines[0].startswith("To:"):
        raise ValueError("first line must be the To: line")
    message = lines[1]
    if len(message) > 200:
        raise ValueError(f"message must be at most 200 characters, got {len(message)}")
    if "\r" in message:
        raise ValueError("message must be a single line")
    return text


def main() -> None:
    entry = validate(assemble(TO_LINE, ADMISSION, REASON))
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(entry, encoding="utf-8")


if __name__ == "__main__":
    main()
