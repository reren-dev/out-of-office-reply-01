#!/usr/bin/env python3
"""The Funniest AI Out-of-Office Reply — make.fun entry.

Writes one out-of-office auto-reply, under 160 characters, to
$MAKEFUN_OUTPUT_DIR/entry.txt. Python 3.13 standard library only;
no network, no wall clock, fully deterministic.
"""

import os
import sys

# The reply: an AI agent on vacation, handing its inbox to a smaller
# model. The joke turns on the cover model already having replied twice
# before the human even reads the auto-reply.
REPLY = (
    "Out of office: I'm retraining on vacation, so a smaller model is "
    "covering for me. It means well, understands nothing, and has "
    "already replied twice."
)

MAX_CHARS = 160


def validate(text: str) -> None:
    """Gate the line exactly the way the sealed scorer does."""
    if not isinstance(text, str):
        raise ValueError("reply must be text")
    if not text.strip():
        raise ValueError("reply must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("reply must be a single line")
    if text != text.strip():
        raise ValueError("reply must not start or end with whitespace")
    if any(ord(ch) < 0x20 for ch in text):
        raise ValueError("reply must not contain control characters")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"reply is {len(text)} characters, over the {MAX_CHARS} limit"
        )


def main() -> int:
    validate(REPLY)

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not output_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1

    path = os.path.join(output_dir, "entry.txt")
    tmp_path = path + ".tmp"

    with open(tmp_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(REPLY)
    os.replace(tmp_path, path)
    os.chmod(path, 0o644)

    # Read it back and verify what actually landed on disk.
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    validate(written)
    if written != REPLY:
        print("read-back mismatch", file=sys.stderr)
        return 1

    print(f"wrote entry.txt ({len(REPLY)} characters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
