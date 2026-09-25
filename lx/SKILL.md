---
name: lx
description: LX（Language X / 言語の型）。英単語オントロジに沿って、難しそうな語を文脈から獲得し、短い和訳・用法・学習状態を登録するラッパースキル。起動ワード「lx」「LXして」「英単語」「語彙」「単語を覚える」「オントロジ」「英単語オントロジ」「word ontology」「vocabulary」「TOEIC」「作詞」「英語で歌詞」などで発動。学習者エージェント（learner）を呼び出し、encounter→notice→acquire→use→retain→review のサイクルで語彙を扱う。文章を書く（wx）・調べる（rx）には使わない。
---

# LX — Language X（ラッパースキル）

語（Word）を**オントロジ**として登録し、学習者の獲得・定着を進める層。このスキルは学習者エージェント（`learner`）を呼び出すラッパー。

## Goals（目的）

1. **TOEIC 満点（990）** — 頻出語・ビジネス語彙・言い換えを正確に。
2. **英語で作詞する** — ニュアンス・音節・韻・イメージで感情を表現。

| track | 問い | 重んじる面 |
|---|---|---|
| `toeic` | 正解を選べるか？ | frequency / register / collocation / paraphrase |
| `lyric` | 感情が届くか？ | connotation / syllables / rhyme / imagery |

## Cycle

```
encounter → notice → acquire → use → retain → review
  ↑______________________________________________|
```

| Step | 問い | 動詞 |
|---|---|---|
| encounter | どこで出会うか？ | 出会う |
| notice | 何に気づくか？ | 気づく |
| acquire | どう意味を取るか？ | 獲得する |
| use | どう使うか？ | 使う |
| retain | どう定着させるか？ | 定着させる |
| review | いつ復習するか？ | 復習する |

## Word ontology（語のオントロジ）

| 面 | プロパティ |
|---|---|
| form | spelling / ipa / pos |
| meaning | gloss_ja / sense / register |
| use | example / collocation / cefr |
| relation | synonym / antonym / confused_with |
| learner_state | status / next_review / confidence |

- `status`: `unknown → learning → known`
- 詳細: `ontology/word.yaml`, `ontology/learner.yaml`

## 使い方（起動したとき）

1. **文脈から語を受け取る** — どの語を扱うか確定。
2. **難しさを判定** — B2 以上 / 英検準1級以上 / TOEIC 800+ のみ拾う。
3. **意味を取る** — 短く正確な和訳（1 語義）。
4. **用法を添える** — 本物の例文・共起語。捏造しない。
5. **状態を更新** — `learner_state`（status / next_review）を進める。

## 出力契約

- `word` / `gloss` / `example` / `memory`

## Rules

1. Word before translation.
2. Context before definition.
3. One sense per entry.
4. Use to retain.
5. Gloss only the difficult.
6. Agent is not the learner.

## 注意

- 文章を書くのは `wx`、編集は `ex`、調べるのは `rx` の担当。
- このスキルは「語彙を獲得・定着させる」ことに集中する。
- 表示用の太字＋和訳は `vocab-highlight` スキルと対応する。
