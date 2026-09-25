---
name: vocab-highlight
description: 返信の中の難しい英単語を太字＋日本語グロスで目立たせ、さらに返信末尾に「Tips 単語コーナー」を append して IT・マーケティング・各ドメインの専門用語を少しずつ増やす。起動ワード「難しい英単語」「英単語を目立たせて」「語彙ハイライト」「vocab」「vocabulary」「word watch」「今日の英単語」「tips単語」「ドメイン知識」「IT用語」「マーケ用語」「専門用語」など。ユーザーは英語学習中なので、原則すべての返信で適用する（AGENTS.md の言語ミックス方針とセット）。コード・識別子・コマンドは対象外。
---

# vocab-highlight (英単語ハイライト ＋ ドメイン tips 単語)

## 目的 / What it does

2 つを担う：

1. **英単語ハイライト** — 返信に自然に混ざる **難しい英単語（学習語彙）** を太字で目立たせ、短い日本語の意味を添える。読みながら語彙を拾えるようにする。
2. **Tips 単語コーナー** — 英単語に限らず、**IT・マーケティング・各ドメインの専門用語・概念** を、返信末尾に毎回 1 語ずつ append する（少しずつ知識を増やす）。

## いつ適用するか / When

- **原則、すべての返信で適用**（"いつも"）。グローバルルール `AGENTS.md` の言語ミックス方針とセットで動く。
- 明示起動ワード: 「難しい英単語」「英単語を目立たせて」「語彙ハイライト」「vocab」「word watch」「今日の英単語」など。

## ルール / Rules

1. **「難しそうな語」だけ** を選ぶ。少しでも簡単・見慣れた語は対象外。
2. 返信ごとに **1〜3 語** まで。多くても 5 語。over-highlight しない。
3. 選ぶ基準 = 学習者より上：**CEFR B2 以上 / 英検準1級以上 / TOEIC 800+** の語。
   - 例: ubiquitous, subtle, mitigate, leverage, robust, arbitrary, tedious, nuance, plausible, concise, prominent, reluctant.
4. 選んだ語は本文中で **太字** `**word**` にし、**すぐ後ろに和訳を追記** する：`**word**（和訳）`。
   - 単語 1 つに和訳 1 つ。長い説明は書かない（数語のグロスで十分）。
5. 意味は **短い日本語の和訳**。返信末尾に一覧を置くのは任意（語が多いときだけ）。
6. 技術識別子・コマンド・ファイルパス・変数名・API 名は **絶対に太字化しない**（原文のまま）。
7. コードブロックの中は触らない。
8. すでに太字の語、固有名詞、一般的すぎる語（get, make, use, good…）は選ばない。
9. 「文脈で意味が自明な超基本語」は避け、学習価値のある語を優先する。

## 出力フォーマット / Output

基本は **本文中のインライン和訳** のみ：

> その挙動は **ubiquitous**（遍在する、どこにでもある）で、バグも **mitigate**（軽減）できる。

- 語が多いときだけ、返信末尾に一覧を任意で追加する。
- 毎回同じ語を繰り返さない。ローテーションする。

```
### Word watch 🔤
- **ubiquitous** = 遍在する、どこにでもある
- **mitigate** = 和らげる、軽減する
```

## Tips 単語コーナー / Domain Tips Corner

英単語だけでなく、**各ドメインの知識** から毎回少しずつ語を append する。

### Format

```text
### Tips 単語 🔎
- **[IT] idempotent** = 冪等（何度実行しても同じ結果になる性質）
  - なぜ: リトライしても壊れない API・バッチ設計の基本
```

### Rules

1. 返信ごとに **1 語**（多くて 2 語）。少しずつ増やす。
2. **ドメインをローテーション** する。連続で同じドメインにしない。
3. 専門用語・概念・略語・ツール名・手法など、**知識価値のある語** を選ぶ。
4. 意味は短く。**そのドメインでの用法** ＋ **なぜ重要か** を 1 行で。
5. コード識別子・コマンド・固有名詞は対象外（原文のまま）。

### ローテーション候補（X シリーズと対応）

| ドメイン | 例 |
| --- | --- |
| IT / DX | idempotent, cache invalidation, race condition |
| Marketing / MX | funnel, churn, positioning |
| Business / BX | runway, P&L, SLA |
| Science / SX | entropy, falsification, control group |
| Philosophy / PX | aporia, ontology, dialectic |
| Writing / WX | register, cadence, trope |
| Language / LX | collocation, connotation, register |
| Design / UX | affordance, information architecture, dark pattern |
| Research / RX | literature review, citation, primary source |

## レベル早見表

| レベル | 目安 | 扱い |
| --- | --- | --- |
| A1–A2 | 中学〜高校基礎 | ハイライトしない |
| B1 | 高校〜英検2級 | 基本はしない |
| B2 | 英検準1級 / TOEIC 800 | **ハイライト候補** |
| C1–C2 | 英検1級 / ネイティブ教養 | **積極的にハイライト** |

## 例 / Example

Before:
> This function makes the code simpler and stops the bug.

After:
> This function **mitigates**（軽減する）the bug and makes the code **concise**（簡潔な）.

## 注意 / Caveats

- 技術的正確さを優先。グロスの意味は正確に。安全・セキュリティ情報は平易さ優先。
- 本文中の英単語ハイライト（`**word**（和訳）`）と、末尾の **Tips 単語コーナー** は別枠として扱う。
- ユーザーが「やめて」と言うまで続ける。
