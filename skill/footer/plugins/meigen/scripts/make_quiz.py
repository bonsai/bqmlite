#!/usr/bin/env python3
"""meigen 単語記録 (words.tsv) から復習クイズ (quiz.json) を生成する。

Usage:
  make_quiz.py                 # data/quiz.json (デフォルト 5問・4択)
  make_quiz.py --n 10 --out /tmp/q.json
  make_quiz.py --seed 7        # 決定的
"""
import argparse
import csv
import json
import random
import sys
from datetime import date
from pathlib import Path

HEADER = ["date", "word", "gloss", "quote", "lang"]
BASE = Path(__file__).resolve().parent.parent  # meigen/
WORDS_TSV = BASE / "data" / "words.tsv"


def load_words(path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        rows = list(csv.reader(f, delimiter="\t"))
    words = []
    for i, r in enumerate(rows):
        if not r or r[0].lstrip().startswith("#"):
            continue
        if r[0] == HEADER[0]:
            continue
        d = dict(zip(HEADER, (r + [""] * len(HEADER))[: len(HEADER)]))
        if d["word"] and d["gloss"]:
            words.append(d)
    return words


def build_quiz(words, n, rng):
    pick = rng.sample(words, min(n, len(words)))
    glosses = [w["gloss"] for w in words]
    questions = []
    for w in pick:
        distractors = rng.sample([g for g in glosses if g != w["gloss"]], min(3, max(0, len(glosses) - 1)))
        choices = [w["gloss"]] + distractors
        rng.shuffle(choices)
        questions.append({
            "word": w["word"],
            "en": w["quote"],
            "choices": choices,
            "answer": w["gloss"],
            "jp": w["gloss"],
        })
    return questions


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=5, help="questions count (default 5)")
    ap.add_argument("--out", type=str, default=str(BASE / "data" / "quiz.json"))
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--words", type=str, default=str(WORDS_TSV))
    a = ap.parse_args()

    words = load_words(Path(a.words))
    if not words:
        print(f"words.tsv が空です: {a.words}", file=sys.stderr)
        sys.exit(1)

    n = min(a.n, len(words))
    rng = random.Random(a.seed)
    quiz = {"generated": date.today().isoformat(), "total": n, "questions": build_quiz(words, n, rng)}
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(quiz, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK: {out} ({n} questions / pool {len(words)} words)")


if __name__ == "__main__":
    main()