---
name: wx
description: WX（Work X / Agent Experience）。リポジトリ bonsai/WX の定義に沿って、Agent Experience を実際の Work として回す。基本ループは MX（見つける）→ RX（深掘る）→ AX（任せる）→ WX（生み出す）→ 市場へ。起動ワード「wx」「WXして」「見つける深掘る任せる生み出す」「Agent Experience」「何を生み出すか」「成果物を出す」「Work X」「MX RX AX WX」などで発動。何を発見し、何を研究し、何をAgentに任せ、何を成果物として生み出すか、という一連の仕事の流れを設計・実行するとき使う。市場との関係設計だけ（MX）やエージェントのBE/DO定義だけ（AX）には使わない。
---

# WX — Work X / Agent Experience

出典: https://github.com/bonsai/WX

WX は、**Agent Experience を実際の Work として扱うための層**である。

基本の経験型:

```
MX → RX → AX → WX → MX → …
```

> **見つける → 深掘る → 任せる → 生み出す**

## 1. Agent Experience の4つの型

### MX — Market X（見つける）

市場・ユーザー・社会を観察し、何をする価値があるのかを見つける。

```
Observe → Need / Reaction → Theme → Hypothesis
```

**MX = 見つける**

### RX — Research X（深掘る）

MX で見つけたテーマを調査し、理解・検証・構造化する。

```
Question → Research → Analysis → Knowledge → Method / Hypothesis
```

**RX = 深掘る**

### AX — Agent X（任せる）

RX で得た方法を Agent に渡し、実行可能・反復可能な仕事へ変換する。

```
Method → Agent → Tool / Context / Model → Automation → Repeatable Work
```

AX は Agent そのものではなく、**Agent に仕事を任せ、自動化する経験の層**である。

**AX = 任せる**

### WX — Work X（生み出す）

Agent を含む仕組みを使って、実際の成果物を作り、完成させ、外へ出す。

```
Plan → Do → Check → Revise → Output
```

成果物の例: 記事、コード、資料、作品、データ、サービス。

**WX = 生み出す**

## 2. 基本ループ

```
        ┌──────────────────────┐
        │                      ↓
MX → RX → AX → WX ────────────┘
│     │     │     │
│     │     │     └─ 生み出す
│     │     └─────── 任せる
│     └───────────── 深掘る
└─────────────────── 見つける
```

### 経験としての問い

| Layer | 問い | 動詞 |
|---|---|---|
| MX | 何をやるべきか？ | 見つける |
| RX | それをどう理解するか？ | 深掘る |
| AX | どこまで任せられるか？ | 任せる |
| WX | 何を生み出すか？ | 生み出す |

WX の成果は再び市場へ出て、MX の観測対象になる。

```
WX → OUTPUT → Market / User / Society → Reaction / Feedback → MX → RX → AX → WX
```

## 3. Agent Experience と Engineering

MX/RX/AX/WX を実際に回すための Engineering 側を、DX / AX / AW として支える。

```
HUMAN / SOCIETY → MX (Market X) → RX (Research X) → AX (Agent X) → WX (Work X) → OUTPUT → MX ↺
```

Engineering:

```
DX = Human-facing development environment
AX = Agent execution / delegation environment
AW = Agent workflow definition
```

※この文書では **AX** を「Agent Experience の略」ではなく、**Agent X / 任せる層**として扱う。Agent Experience 全体は **MX → RX → AX → WX** である。

## 4. 最小定義

> **MX = 見つける**
>
> **RX = 深掘る**
>
> **AX = 任せる**
>
> **WX = 生み出す**

```
見つける → 深掘る → 任せる → 生み出す → 届ける → また見つける
```

これは AI に「書かせる」だけではなく、**何を見つけ、何を研究し、何を Agent に任せ、何を成果として生み出すか**まで含めた Agent Experience の基本型である。

## 使い方（このスキルが起動したとき）

仕事を「見つける→深掘る→任せる→生み出す」の流れで回す。

1. **MX（見つける）** — 何をする価値があるか。市場・ユーザーの反応からテーマを出す。
2. **RX（深掘る）** — テーマを調査・検証・構造化し、方法（Method）まで落とす。
3. **AX（任せる）** — 方法を Agent に渡し、Tool/Context/Model を整え、反復可能な仕事にする。
4. **WX（生み出す）** — Plan→Do→Check→Revise で成果物を完成させ、外へ出す。
5. **還流** — 成果物を市場に出し、反応を MX の観測に戻す（ループを閉じる）。

### 注意（層の混同を避ける）

- MX のスキル（bonsai/MX）＝ 市場との関係設計（Marketing Transformation）。
- AX のスキル（bonsai/AX）＝ エージェントの BE/DO を定義・運用するオントロジー。
- WX のスキル（本スキル）＝ その両者を含む「仕事の経験ループ」。
- WX 文書内の「MX=Market X」「AX=Agent X」は経験型としての呼称であり、リポジトリ bonsai/MX・bonsai/AX の Engineering 定義とは層が異なる点に留意する。
