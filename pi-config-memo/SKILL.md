---
name: pi-config-memo
description: Pi (pi-coding-agent, the terminal AI coding agent) の設定・構成ファイルの場所と編集方法を覚えておくためのメモ。Pi のデフォルトモデル・プロバイダ・設定を変更したいとき、または「Pi の設定ファイル」「pi config」「pi のモデルをデフォルトに」と言われたときに使う。
---

# Pi 設定ファイルの場所 (memory path)

Pi は `@mariozechner/pi-coding-agent` という npm グローバルパッケージの CLI エイジェント。
Windows 上の設定はすべて `~/.pi/agent/` 配下にある。

## 主要な設定ファイル

| パス | 役割 |
|------|------|
| `~/.pi/agent/settings.json` | グローバル設定（全プロジェクト）。デフォルトモデル/プロバイダをここに書く |
| `~/.pi/agent/models.json` | カスタムプロバイダ/モデル定義（OpenAI互換APIなど） |
| `~/.pi/agent/auth.json` | 認証情報・API キー |
| `~/.pi/agent/AGENTS.md` | グローバル AGENTS.md（起動時に読まれる） |
| `~/.pi/agent/SYSTEM.md` | デフォルトシステムプロンプトの置き換え（グローバル） |
| `~/.pi/agent/sessions/` | セッション自動保存（作業ディレクトリごと） |
| `~/.pi/agent/extensions/` | 拡張機能（例: `lmstudio/`） |
| `~/.pi/agent/keybindings.json` | キーバインド |
| `~/.pi/agent/skills/`, `~/.pi/agent/prompts/`, `~/.pi/agent/themes/` | スキル/プロンプト/テーマ |

## デフォルトのモデル/プロバイダ設定

`settings.json` の `defaultProvider` と `defaultModel` で指定する:

```json
{
  "lastChangelogVersion": "0.73.1",
  "defaultProvider": "lmstudio",
  "defaultModel": "google/gemma-4-e4b"
}
```

- `defaultProvider`: プロバイダ名（例: `"lmstudio"`, `"anthropic"`, `"openai"`）
- `defaultModel`: モデル ID（例: `"google/gemma-4-e4b"`）
- `defaultThinkingLevel`: `"off"` | `"minimal"` | `"low"` | `"medium"` | `"high"` | `"xhigh"`
- モデル切り替えの UI: `/model` コマンド、Ctrl+L（モデル選択）、Ctrl+P（有効モデルを巡回）

## カスタムプロバイダ（LM Studio など）

`models.json` に OpenAI 互換 API のプロバイダを追加する:

```json
{
  "providers": {
    "lmstudio": {
      "name": "LM Studio",
      "baseUrl": "http://localhost:1234/v1",
      "apiKey": "lm-studio",
      "api": "openai-completions"
    }
  }
}
```

## 変更の反映

- これらの設定は Pi 起動時に一度だけ読み込まれる。変更後は **Pi を再起動** しないと反映されない。
- コマンドラインでモデルを指定して起動することも可能（`--models` フラグ、`enabledModels` 設定）。

## 他のツールとの関係

- opencode（別ツール）の設定は `~/.config/opencode/opencode.jsonc` にあり、Pi とは無関係。
- ユーザーが「pi の設定」と言ったら、これは **Pi ではなく opencode** を指していないか確認する。
