---
name: tips-word
description: >
  返信末尾に「Tips 単語コーナー」を append して、IT・マーケティング・ビジネス・科学など各ドメインの専門用語を 1 語ずつ、ドメインをローテーションしながら少しずつ増やすスキル。
  起動ワード「tips単語」「Tips 単語コーナー」「単語コーナー」「ドメイン知識」「domain tips」「専門用語」「IT用語」「マーケ用語」「用語を教えて」「今日の用語」などで発動。
  英単語本体のハイライト（太字＋和訳）は vocab-highlight スキルの担当。
  コード・識別子・コマンド・パスは対象外。
---

# tips-word（Tips 単語コーナー / ドメイン知識を少しずつ増やす）

## 目的 / What it does

英単語の学習とは別に、**IT・マーケティング・各ドメインの専門用語・概念** を、
返信末尾に **毎回 1 語ずつ**（多くて 2 語）追加して、少しずつ知識を育てる。

- 語彙学習の対象は「英語という言語」ではなく「その分野の概念・用語」。
- 名称・略語・ツール・手法・考え方を、短い説明と「なぜ重要か」を添えて渡す。

## いつ適用するか / When

- **原則、すべての返信で適用**（"いつも"）。グローバルルール `AGENTS.md` の「語彙ハイライト」とセットで動く。
- 明示起動ワード: 「tips単語」「単語コーナー」「ドメイン知識」「専門用語を教えて」など。
- 英単語本体のハイライト（`**word**（和訳）`)は **vocab-highlight** スキルの担当。本スキルはコーナー（末尾のドメイン用語）のみ。

## フォーマット / Format

返信の末尾（語彙ハイライトの後）に append する:

```text
### Tips 単語 🔎
- **[IT] idempotent** = 冪等（何度実行しても同じ結果になる性質）
  - なぜ: リトライしても壊れない API・バッチ設計の基本
```

## ルール / Rules

1. 返信ごとに **1 語**（多くて 2 語）。少しずつ増やす。増やしすぎない。
2. **ドメインをローテーション** する。連続で同じドメインにしない。
3. 専門用語・概念・略語・ツール名・手法など、**知識価値のある語** を選ぶ。
4. 意味は短く。**そのドメインでの用法** ＋ **なぜ重要か** を 1 行で。
5. コード識別子・コマンド・固有名詞・ファイルパスは対象外（原文のまま）。
6. 技術的正確さを優先。意味・用法を間違えない。安全・セキュリティ情報は平易さ優先。

## ローテーション候補（X シリーズと対応）

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

## 例 / Example

> この設定は `~/.bashrc` に置くのが安全です。
>
> ### Tips 単語 🔎
> - **[IT] idempotent** = 冪等（何度実行しても同じ結果になる性質）
>   - なぜ: リトライしても壊れない API・バッチ設計の基本

## 注意 / Caveats

- 本文中の英単語ハイライト（`**word**（和訳）`)と、末尾の **Tips 単語コーナー** は別枠として扱う。
- 元は `vocab-highlight/SKILL.md` の「Tips 単語コーナー / Domain Tips Corner」節。独立スキル化したので、単語コーナーは本スキルを参照する。
- ユーザーが「やめて」と言うまで続ける。