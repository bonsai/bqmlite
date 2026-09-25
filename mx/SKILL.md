---
name: mx
description: MX（Marketing Transformation / マーケティング・トランスフォーメーション）フレームワーク。リポジトリ bonsai/MX の実践モデルに沿って、市場を観測し顧客との関係を設計・実行・計測・学習する。起動ワード「mx」「MXして」「MXを回して」「マーケティングトランスフォーメーション」「市場との関係を設計」「observe/segment/hypothesize」「マーケ施策を回す」「GTMをMXで」などで発動。製品・ブログ・本・サービスを市場に出す／売る／伸ばす相談のときに、observe→segment→hypothesize→position→communicate→measure→learn→update のサイクルで問いを整理し、施策を設計する。単なる広告コピー作成やコーディング依頼には使わない。
---

# MX — Marketing Transformation

出典: https://github.com/bonsai/MX

MX は単なるマーケティング業務ではなく、**市場を観測し、顧客との関係を設計し、仮説・施策・反応・学習を循環させるための実践モデル**。

## 定義（mx.yaml）

```yaml
name: MX
meaning: Marketing Transformation
subject: market
actor: marketer
cycle: [observe, segment, hypothesize, position, communicate, measure, learn, update]
outputs: [market_model, customer_model, hypothesis, campaign, measurement, learning]
relations:
  dx: field_business_customer_data
  ax: accurate_execution_of_change
  mx: market_customer_demand_touchpoints
```

## Marketer（ontology/marketer.yaml）

Marketer は「売る人」ではなく、**市場との関係を設計・観測・更新する人**。

- **role**: market_relationship_designer
- **inputs**: market_data, customer_signals, cultural_signals, business_constraints
- **activities**: research, segmentation, hypothesis, positioning, communication, measurement, learning, iteration
- **outputs**: market_model, customer_model, hypothesis, campaign, measurement, learning
- **feedback**: source=market → target=hypothesis

## Cycle

```
observe
  ↓
segment
  ↓
hypothesize
  ↓
position
  ↓
communicate
  ↓
measure
  ↓
learn
  ↓
update
  └────→ market
```

## DX / AX / MX

| Layer | 対象 | 主体 |
|---|---|---|
| DX | 現場・業務・顧客・データ | DXer |
| AX | 変化を正確に捉え実行 | Agent / AX |
| MX | 市場・需要・顧客接点 | Marketer |

MX ↔ Marketer は「変化する対象」と「それを担う主体」の関係として設計する。

## Structure

```
MX/
├── README.md
├── mx.yaml
├── ontology/
│   └── marketer.yaml
├── research/
├── market/
├── hypothesis/
├── campaign/
└── measurement/
```

将来的には Marketer Agent、market data、hypothesis、action、feedback のループを AW から生成する。

## 使い方（このスキルが起動したとき）

ユーザーが製品・ブログ・本・サービスを市場に出そうとしているとき、次の手順で MX を回す。

1. **observe** — 市場・需要・競合・既存資産を事実ベースで観測する。数字や具体的なシグナルを集める。
2. **segment** — 顧客を動機・状況で区分する（例：初心者／教養層／実務者）。各セグメントの「欲しい理由」を言語化。
3. **hypothesize** — 「もし◯◯なら、△△は買う/動く」形式の検証可能な仮説にする（H1, H2, …）。
4. **position** — 競合との差＝代替不可能な立ち位置を一文で定義する。
5. **communicate** — チャネル（SNS/ブログ/イベント/EC）とメッセージ、発信パルスを設計する。
6. **measure** — 転換率・DL数・販売数・離脱などの計測指標を先に決める。
7. **learn** — 反応から何が効いたかを言語化し、仮説を更新する。
8. **update** — 学びを市場モデル・顧客モデル・施策へ反映し、observe に戻る。

### 出力の型

- **market_model**（市場の見取り図）
- **customer_model**（顧客像・動機）
- **hypothesis**（検証可能な仮説リスト）
- **campaign**（施策・チャネル・メッセージ・スケジュール）
- **measurement**（指標と結果）
- **learning**（学びと次の仮説）

### 心構え

- 主語は常に「市場」。売り込みではなく**関係の設計**として扱う。
- 仮説は必ず**反証可能**にする。曖昧な願望を施策にしない。
- 一度で終わらせず、**cycle を回し続ける**。market が常にフィードバック源。
