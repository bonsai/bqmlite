#!/usr/bin/env python3
"""lang_ratio.py - 简易测量文字种/语言比例 (simple character-type & language ratio meter)

Measures the rough ratio of English / Japanese / Chinese / Emoji / Other in a
piece of text. Analysis is capped at the first 1000 characters.

Usage:
    python lang_ratio.py "some text"
    python lang_ratio.py path/to/file.txt
    echo "some text" | python lang_ratio.py
    python lang_ratio.py -            # read from stdin explicitly

Notes / 注意:
  * Kanji (CJK ideographs) are shared between Japanese and Chinese, so they
    are reported as "CJK" plus a rough heuristic split: a kanji run touching
    kana is counted as Japanese, otherwise as Chinese. Treat it as a hint,
    not a precise language detector.
  * Only the Python standard library is used.
"""
from __future__ import annotations

import re
import sys
import unicodedata

MAX_CHARS = 1000

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

EMOJI_RE = re.compile(
    "["
    "\U0001F000-\U0001FAFF"  # pictographs / symbols / supplemental
    "\U00002600-\U000027BF"  # misc symbols & dingbats
    "\U00002B00-\U00002BFF"  # misc symbols and arrows
    "\U00002190-\U000021FF"  # arrows
    "\U0000FE00-\U0000FE0F"  # variation selectors
    "\U0000200D"             # zero-width joiner
    "\U00002B50\U00002764"   # star, heart
    "]"
)


def is_emoji(ch: str) -> bool:
    return bool(EMOJI_RE.match(ch))


def is_kana(ch: str) -> bool:
    cp = ord(ch)
    return 0x3040 <= cp <= 0x309F or 0x30A0 <= cp <= 0x30FF


def is_han(ch: str) -> bool:
    cp = ord(ch)
    return (
        0x4E00 <= cp <= 0x9FFF
        or 0x3400 <= cp <= 0x4DBF
        or 0xF900 <= cp <= 0xFAFF
        or 0x20000 <= cp <= 0x2A6DF
    )


def base_of(ch: str) -> str:
    if is_emoji(ch):
        return "emoji"
    if is_kana(ch):
        return "kana"
    if is_han(ch):
        return "han"
    if ("a" <= ch <= "z") or ("A" <= ch <= "Z"):
        return "latin"
    return "other"


def analyze(text: str):
    text = text[:MAX_CHARS]
    chars = list(text)
    n = len(chars)
    base = [base_of(c) for c in chars]

    def kana_left(i: int) -> bool:
        j = i - 1
        while j >= 0:
            if chars[j].isspace() or base[j] == "han":
                j -= 1
                continue
            return base[j] == "kana"
        return False

    def kana_right(j: int) -> bool:
        k = j
        while k < n:
            if chars[k].isspace() or base[k] == "han":
                k += 1
                continue
            return base[k] == "kana"
        return False

    counts = {
        "english": 0,       # Latin letters
        "japanese": 0,      # kana + Japanese-kanji (heuristic)
        "chinese": 0,       # Han not touching kana (heuristic)
        "cjk": 0,           # all Han (kana + chinese above)
        "emoji": 0,
        "other": 0,         # digits / punctuation / spaces / symbols
    }

    i = 0
    while i < n:
        if base[i] == "han":
            j = i
            while j < n and base[j] == "han":
                j += 1
            is_ja = kana_left(i) or kana_right(j)
            counts["cjk"] += j - i
            if is_ja:
                counts["japanese"] += j - i
            else:
                counts["chinese"] += j - i
            i = j
        else:
            b = base[i]
            if b == "latin":
                counts["english"] += 1
            elif b == "kana":
                counts["japanese"] += 1
            elif b == "emoji":
                counts["emoji"] += 1
            else:
                counts["other"] += 1
            i += 1

    return counts, text


def read_input(argv) -> str:
    if len(argv) > 1:
        arg = argv[1]
        if arg == "-":
            return sys.stdin.read()
        import os

        if os.path.isfile(arg):
            with open(arg, "r", encoding="utf-8", errors="replace") as f:
                return f.read()
        return " ".join(argv[1:])
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return ""


def bar(pct: float, width: int = 30) -> str:
    filled = int(round(pct / 100 * width))
    return "#" * filled + "-" * (width - filled)


def main() -> int:
    text = read_input(sys.argv)
    if not text.strip():
        print(__doc__)
        return 1

    truncated = len(text) > MAX_CHARS
    counts, used = analyze(text)
    total = len(used)

    print(f"languages/characters in {total} char(s)"
          + ("  [truncated to 1000]" if truncated else ""))
    print("-" * 52)

    rows = [
        ("English (Latin)", counts["english"]),
        ("Japanese (kana+kanji*)", counts["japanese"]),
        ("Chinese (Han*)", counts["chinese"]),
        ("Emoji", counts["emoji"]),
        ("Other (digit/space/punct)", counts["other"]),
    ]
    for label, c in rows:
        pct = (c / total * 100) if total else 0.0
        print(f"{label:<26} {c:>4}  {pct:>5.1f}%  {bar(pct)}")

    print("-" * 52)
    ja = counts["japanese"]
    zh = counts["chinese"]
    print(f"(all CJK ideographs: {counts['cjk']}; "
          f"*rough split -> JP {ja} / ZH {zh})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
