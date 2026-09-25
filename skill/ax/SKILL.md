---
name: ax
description: AX（Agent Operational Ontology / エージェント運用オントロジー）。リポジトリ bonsai/AX の定義に沿って、エージェントが「何であるか（BE）」と「何ができるか（DO）」を型・状態・関係・Action/WorkTypeとして定義・運用する。起動ワード「ax」「AXして」「AXを定義」「BEとDO」「WorkType」「Workflow」「エージェントの定義」「オントロジー」「タスクを型にする」「Agent Operational Ontology」などで発動。エージェント／AI／人間を含む問題解決主体の能力・権限・仕事の型を設計するときに、Object/Action/WorkType/Task/Workflow/AW/Evidence のモデルで整理する。市場・販売戦略（MX）や成果物そのものの制作（WX）には使わない。
---

# AX — Agent Operational Ontology

出典: https://github.com/bonsai/AX

AX は、エージェントが**何であるか（BE）**と**何ができるか（DO）**を、限定された世界（bounded world）の中で定義・運用する。

> **AX = BE + DO**
>
> **BE = であること**
>
> **DO = できること**

## Canonical model

```
AX
├── BE — であること
│   ├── Object Type
│   ├── Property Type
│   ├── State Type
│   ├── Relation Type
│   └── Evidence Type
│
└── DO — できること
    ├── Action
    ├── WorkType
    ├── Input / Output Type
    ├── Preconditions
    ├── Effects
    ├── Permission
    └── Verification
```

## Work model

- **Object** = 世界の対象
- **Action** = 世界を変化させる動詞
- **WorkType** = Object → Object という仕事の型
- **Task** = WorkType の実行インスタンス
- **Workflow** = 仕事の流れ
- **Agent** = Task を実行する主体
- **AW** = Task を実行・編成するオーケストレータ
- **Evidence** = 実行・観測によって得られる証拠

```
Object/State → Verb/WorkType → Object/State
                         ↓
                       Task
                         ↓
                      Workflow
                         ↓
                        AW
                         ↓
                       Agent
                         ↓
                    Real World
                         ↓
                      Evidence
                         ↓
                  State Transition
                         ↺
```

### WorkType

WorkType は AX における「型付きの動詞」。

```
WorkType = Input Object/State → Verb → Output Object/State
```

例:

```
create(Design) → EmbroideryPattern
approve(EmbroideryPattern) → ApprovedPattern
manufacture(ApprovedPattern) → Product
```

WorkType は **何ができるか**を言う。Agent ではない。

```
WorkType = what can be done
Agent    = who/what can do it
Task     = this particular execution
AW       = orchestration
```

## Capability and permission

```
Capability    = what can be done
Permission    = what is allowed
Authorization = permission granted for this execution
```

Action や WorkType を定義しただけでは、実行は許可されない。

## Lifecycle

```
Define WorkType
  ↓
Find applicable Object
  ↓
Instantiate Task
  ↓
Authorize Agent
  ↓
AW orchestrates
  ↓
Execute Action
  ↓
Verify Effect
  ↓
Evidence
  ↓
State Update
  ↺
```

## Ontology boundary

```
FIELD / REAL WORLD
        ↓
FDE OBSERVATION
        ↓
EVIDENCE
        ↓
SCOPE
        ↓
ONTOLOGY
        ↓
AX: BE / DO
        ↓
WORKTYPE / ACTION
        ↓
TASK
        ↓
WORKFLOW
        ↓
AW
        ↓
REAL WORLD
        ↓
OUTCOME / EVIDENCE
        ↺
```

`fde-agent` が現実を観察し、`ontology` が何であるかを定義し、`AX` が何ができるかを定義・運用し、`AW` が実行を編成する。

## State first

関係や能力は不変の事実ではない。現在の知識と関係は**状態（state）**であり、証拠に裏付けられる。

```
A ↔ Relation State ↔ B
```

Task state も明示する:

```
proposed → authorized → running → succeeded
                         ├──────→ failed
                         └──────→ cancelled
```

## BONSAI layer responsibilities

| Layer | Responsibility |
|---|---|
| `fde-agent` | 現場を観察し証拠を得る |
| `ontology` | 何であるかを型・状態・関係として定義する |
| `AX` | 何ができるかを Action/WorkType として定義・運用する |
| `agent` | Task を遂行する |
| `AW` | Task/Workflow を編成・実行する |
| `journal` | 出来事を時系列で記録する |
| `History` | 起源・経緯・意味を保持する |

## Agent（定義.md）

> **エージェントとは、問題を解決する人みんなのことである。**
> **Agent = Problem Solver**

Agent は AI に限定されない。人間も、AIも、プログラムも、組織も、問題解決の役割を担うなら Agent である。

```
Agent
├── Human Agent
├── AI Agent
├── Software Agent
├── Organizational Agent
└── Hybrid Agent
```

### Agent と Tool

```
Agent
  │ uses
  ↓
Tool
```

Agent は問題を解決する主体、Tool は能力・手段。ゆえに **LLM は必ずしも Agent ではない**（Tool として利用される）。

### Agent の最小モデル

```yaml
agent:
  problem: ""
  goal: ""
  context: ""
  aware: []
  capability: []
  tools: []
  constraints: []
  authority: []
  actions: []
  evidence: []
  result: ""
```

### Agent の基本ループ

```
PROBLEM → OBSERVE → UNDERSTAND → PLAN → USE TOOL → ACT → VERIFY → RESULT → EVIDENCE → PROBLEM STATE UPDATE ↺
```

### Issue と Agent

```
Data → State → Issue → Agent → Action → Result → State
```

> Issue は問題の表現であり、Agent は問題を解決する主体である。

## Principles

1. Reality before model.
2. Evidence before interpretation.
3. Scope before abstraction.
4. BE before DO.
5. Verbs are typed.
6. Capability is not permission.
7. WorkType and Task are separate.
8. AW orchestrates; Agent executes.
9. Evidence closes the loop.
10. Relations are states, not fixed deterministic truths.

## Core statement

> **BONSAI AX defines and operates the boundary between what an agent operates on and what an agent can do: BE defines the typed world; DO defines typed actions and work; Task instantiates work; Workflow composes work; AW orchestrates execution; Evidence verifies change.**

## 使い方（このスキルが起動したとき）

エージェント／AI／人間を含む問題解決主体を設計するとき、次の順で AX を適用する。

1. **BE を定義** — 対象世界を Object/Property/State/Relation/Evidence の型として書く。
2. **DO を定義** — できることを Action/WorkType（Input → Verb → Output）として書く。
3. **分離を守る** — WorkType（何ができるか）／Agent（誰がやるか）／Task（この実行）／AW（編成）を混ぜない。
4. **権限を明示** — Capability と Permission は別。実行には Authorization が要る。
5. **状態で扱う** — 関係・能力は不変の事実ではなく State。Evidence で裏付ける。
6. **ループを閉じる** — Execute → Verify Effect → Evidence → State Update。
