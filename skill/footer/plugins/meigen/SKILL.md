---
name: meigen
description: >
  フッター内の名言コーナー（Meigen）プラグイン。名言風の英文＋日本語訳を1組 append し、英文中の難しい単語を太字＋和訳で目立たせ、提示した単語を words.tsv に記録し、必要なら記録から単語クイズを作成する。
  起動ワード「名言」「名言コーナー」「meigen」「座右の銘」「今日の言葉」「クイズ」「quiz」「単語クイズ」「復習」などで発動。
---

# meigen（名言風英文 コーナー / footer プラグイン 2）

## 目的 / What it does

返信の締めに「**名言風の英文（English only）**」を 1 句だけ添える。**偉人**（哲学者・歴史学者／人文科学者・ビジネスマン・IT・科学者）の信頼できる言葉。英文中の **難しい単語を太字** で目立たせ、提示した語は **記録** し、**記録からクイズ** を生む。和訳は書かない。

```
引用プール(meigen.tsv)
   ↓ 1つ選ぶ（domain をローテーション）
英文のみ   ← 難しい単語を **太字**（和訳は書かない）
   ↓
提示語を words.tsv へ記録（date|word|gloss|quote）← gloss は記録とクイズ用
   ↓
（要望時）make_quiz.py → quiz.json
```

## 出力フォーマット / Format（1 行）

```text
### 名言コーナー 🖋️
> "It is the mark of an **educated** mind to be able to **entertain** a thought without accepting it." — Aristotle
```

1. **英文のみ 1 行**。和訳は書かない（"English only"）。
2. 出典（偉人名）を `— Author` で添える。
3. 英文中の難語 **1〜2 語** を太字にするだけ（和訳グロスは本文に混ぜない。グロスは `words.tsv` の記録とクイズで渡す）。
4. コード・識別子・コマンド・固有名詞は太字化しない。

## 偉人プールのドメイン / Domains

- **philosophy**: ソクラテス・アリストテレス・マルクス・アウレリウス・ニーチェ・カント・老子…（ストア派・東洋思想含む）
- **history / humanities**: サンタヤナ・E.H.カー・マルク・ブロック・イブン・ハルドゥーン・トゥキュディデス・バールウィン…
- **business**: ドラッカー・バフェット・フォード・ゲイツ・チョークル（チャーチル）・ジョブズ…
- **it / science**: チューリング・ノース・デミング・アインシュタイン・キュリー・パスツール…
- 提示は domain をローテーションして偏りを防ぐ。

## 提示した単語の記録 / Word Record

返信のたび、登場させた難語を **必ず** `data/words.tsv` へ append する（tab区切り、1語=1行）:

```
date(YYYY-MM-DD)  word  gloss  source_quote  lang(=en)
```

例:
```
2026-09-25	ultimate	究極の	Simplicity is the ultimate sophistication.	en
2026-09-25	exemplify	~の好例である	... exemplify ...	en
```

- 既出の語は連続で使い回さない（ローテーション）。同語再提示時は gloss は既存を踏襲。
- 記録は増やし続ける。**消さない**（soubi 台帳と同思想: 装備＝語彙の保全）。

## クイズ作成 / Quiz

- 起動ワード: 「クイズ」「quiz」「単語クイズ」「今日の復習」。
- `scripts/make_quiz.py`（WSL, python3）が `data/words.tsv` を読み、`data/quiz.json` を生成:

```bash
python3 scripts/make_quiz.py            # data/quiz.json 出力（デフォルト 5問, 4択）
python3 scripts/make_quiz.py --n 10 --out /tmp/q.json
python3 scripts/make_quiz.py --seed 7   # 決定的再現
```

- quiz.json 形式: `{"generated": date, "questions":[{"word":..., "en":..., "choices":[...], "answer":..., "jp":...}]}`
  - 問題: 英文中の語（太字語）→ 和訳 4 択。誤答は他の語の gloss から抽出（ランダム選択）。
- 生成後、フッターに結果を 1〜2 行で提示（例: 「復習クイズ 5問 → data/quiz.json をどうぞ ✅」）。

## ルール / Rules

1. 毎回 **英文 1 行のみ**。和訳は書かない。
2. 難語は太字 **1〜2 語**。文脈で意味が自明な語は避ける。
3. 出典は正確に。不確かなら「(伝)」を付ける。
4. 記録は必ず append。新しい語を増やす方向。
5. 偉人（哲学・歴史／人文・ビジネス・IT・科学）の名言をローテーションする。

## 名言プール / Pool

`data/meigen.tsv`（`tab`区切り: 句 | 出典 | カテゴリ | 言語）。足りなければ知識から補うが出典確実なものだけ。英文のまま太字1〜2語を選んで提示し、和訳は自分で付ける。

## 注意 / Caveats

- 「難しい単語が目立つ」が今回の再構成の要。太字化を忘れない。
- 記録ファイルは消さない（Soubi の管理下と想定）。
- ユーザーが「やめて」と言うまで続ける。