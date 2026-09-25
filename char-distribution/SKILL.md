---
name: char-distribution
description: 文章中の文字種・言語の割合（英語/日本語/中文/emoji/その他）を簡易計測する。文字分散、言語比率、文字種の割合、英語と日本語のミックス確認、「何%英語か」「言語の割合を測って」「lang ratio」「character distribution」「文字種カウント」「文字の分散」などで発動。混合言語スタイルの検証に使う。
---

# char-distribution (文字分散 / language ratio meter)

## What it does / 何をするか

Counts characters in a text and reports the rough ratio of:

| category | meaning |
| --- | --- |
| English (Latin) | A-Z / a-z |
| Japanese | hiragana + katakana + kanji (heuristic) |
| Chinese | Han ideographs not touching kana (heuristic) |
| Emoji | Unicode emoji |
| Other | digits, spaces, punctuation, symbols |

Analysis is capped at the first **1000 characters**.

## When to use / いつ使うか

- Check how balanced a reply/text is between English and Japanese
  (e.g. the user's target mix: English 50 / 日本語 35 / 中文 10 / emoji 5).
- 文字種の割合を出したいとき。「何%英語?」「日本語どれくらい?」「文字分散を見て」。
- Verify the mixed-language reply style is actually being applied.

## How to run / 使い方

The script lives next to this file. Run it with Python 3 (stdlib only):

```powershell
python "C:\Users\0501JP\.config\opencode\skills\char-distribution\lang_ratio.py" "<text-or-file>"
```

- First argument may be a **literal string**, a **file path**, or `-` for stdin.
- No argument + piped stdin also works.

### Recommended (encoding-safe) pattern / 推奨手順

If the text contains Japanese/emoji and shell encoding is uncertain, **write the
text to a UTF-8 file first**, then pass the path:

1. Write the text to `%TEMP%\lang_sample.txt` (use the Write tool, UTF-8).
2. Run:

   ```powershell
   python "C:\Users\0501JP\.config\opencode\skills\char-distribution\lang_ratio.py" "$env:TEMP\lang_sample.txt"
   ```

Piping text through the shell can still be lossy before the opencode shell
restart (see the UTF-8 launcher fix in global rules), so prefer a file.

## Output / 出力

Per-category count, percentage, and an ASCII bar, plus a rough JP/ZH split of
the CJK ideographs.

```
languages/characters in 105 char(s)
----------------------------------------------------
English (Latin)              57   54.3%  ################--------------
Japanese (kana+kanji*)       21   20.0%  ######------------------------
Chinese (Han*)                6    5.7%  ##----------------------------
Emoji                         1    1.0%  ------------------------------
Other (digit/space/punct)    20   19.0%  ######------------------------
----------------------------------------------------
(all CJK ideographs: 11; *rough split -> JP 21 / ZH 6)
```

## Caveats / 注意

- Kanji (CJK ideographs) are **shared** between Japanese and Chinese. The
  JP/ZH split is a heuristic: a kanji run touching kana → Japanese, otherwise
  → Chinese. Treat it as a hint, not a precise language detector.
- Only the first 1000 characters are analyzed.
- Stdlib only; no third-party dependencies.
