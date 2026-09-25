---
name: footer
description: >
  返信末尾のフッターを統合管理するマネージャースキル。Meigen（名言風の英文＋日本語訳、難しい単語を太字で目立たせ、提示語を記録し、クイズも作成）を主役に、Eigo（本文の語彙ハイライト＋Tips 単語コーナー）を添える。
  起動ワード「名言」「名言コーナー」「フッター」「footer」「tips英単語の下に」「eigo」「meigen」「単語の記録」「クイズ」「今日の言葉」などで発動。原則、すべての返信で適用（AGENTS.md の言語ミックス / 語彙ハイライト方針とセット）。
---

# footer（フッター統合マネージャー）

## 目的 / What it does

返信本文の **末尾** にプラグインを **決められた順** で積む。

```
本文...
───────── footer ─────────
[1] Eigo    語彙ハイライトは本文内（vocab-highlight）＋ Tips 単語コーナー（tips-word）
[2] Meigen  名言風英文 only（難語 太字）  ← 主役
       └ 提示語は data/words.tsv に記録（gloss は記録・クイズ用）
       └ 「クイズ」で data/quiz.json 生成（要求時）
```

## 再構成方針（今回） / What changed

- Meigen を「名言風の **英文のみ**」に再構成。和訳は書かない。
- 英文中の難しい単語は **太字** で目立たせる。
- 提示した単語は **必ず記録**（`plugins/meigen/data/words.tsv` へ append、gloss 付き）。
- 記録単語から **復習クイズ** を作成できる（`plugins/meigen/scripts/make_quiz.py`）。

## いつ適用するか / When

- **原則、すべての返信で適用**（"いつも"）。短い返信でも Meigen 1 組は付ける。
- 明示起動ワード: 「名言」「名言コーナー」「footer」「eigo」「meigen」「単語の記録」「クイズ」「今日の言葉」など。

## 手順 / Process

1. 各プラグインの `SKILL.md` を読み、フォーマットに従う。
   - `plugins/eigo/SKILL.md`（本文ハイライト + Tips コーナー）
   - `plugins/meigen/SKILL.md`（名言 + 和訳 + 記録 + クイズ）
2. 順序は **Eigo(Tips) → Meigen**。Meigen が最下部。
3. 提示した難語は `plugins/meigen/data/words.tsv` に append（"いつも"）。
4. 「クイズ」発言時は `make_quiz.py` を実行して quiz.json を作り、結果 1 行で報告。

## ルール / Rules

1. Meigen は **英文1行のみ**（和訳なし）。
2. 難語の太字化（1〜2語）と記録を忘れない。
3. 出典は偉人（哲学・歴史／人文・ビジネス・IT・科学）をローテーション。
3. Eigo ブロックの内容変更はしない（vocab-highlight / tips-word に委譲）。
4. 決定版は各プラグインの SKILL.md。ここは調整役。

## 注意 / Caveats

- プラグイン名はディレクトリ `plugins/<name>/SKILL.md` の `name` と一致させる。
- `words.tsv` は消さない（soubi 台帳化の対象）。
- ユーザーが「やめて/外して」と言うまで続ける。