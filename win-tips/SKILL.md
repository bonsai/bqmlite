---
name: win-tips
description: Windows 11 の小技・自動化スクリプト集。実体は C:\Users\0501JP\win-tips。「win-tips」「Windowsの小技」「Windows tips」「小技」「Copilot 無効」「disable copilot」「コピーキーがCtrl+Cを使う問題」「Ctrl+C が SIGINT」「stty intr」「キーボードマップ」「IP 到達監視」「android 同期スクリプト」などで発動。opencode/pi などのエージェントから、Windows の設定変更・トラブル対処・自動化スクリプト利用を支援する。
---

# win-tips — Windows 11 テクニック集

Windows 11 のテクニック・自動化スクリプトの目次と、具体的な操作手順。
実体ファイルは `C:\Users\0501JP\win-tips`（このスキルの外。参照先）。

## コンテンツ一覧

| トピック | ファイル | 用途 |
|---------|----------|------|
| Copilot ボタン無効化 | `disable-copilot.ps1` / `blog-copilot-disable.md` | Copilot ボタン（タスクバー/虫眼鏡アイコン）を PowerShell 一発で消す。`-Revert` で再表示 |
| キーボードマップ入門 | `keyboard-map-tools.ps1` / `blog-keyboard-map.md` | レイアウト確認・変更・テスト |
| Ctrl+C の伝搬レイヤ | `keyboard-layers.md` | Windows Terminal → ConPTY → Shell(stty/trap) → App → Kernel の 5 層構造と制御点 |
| Android 連携スクリプト | `android-*.ps1` / `qr_scan.py` | MTP/FTP での音楽・ファイル同期（詳細は **android-ftp-sync スキル** へルーティング） |
| IP 到達監視 | `ip-reach-monitor.ps1` / `.log` | 指定 IP の到達性ポーリング監視 |

## クイック操作

### Copilot ボタン無効化（1発）
```powershell
& "$env:USERPROFILE\win-tips\disable-copilot.ps1"        # 無効化
& "$env:USERPROFILE\win-tips\disable-copilot.ps1" -Revert # 再表示
```

### Ctrl+C がプロセスを殺してしまう問題（根本対策）
シェル側が唯一の完全制御点。「選択なし Ctrl+C → SIGINT」を防ぐには:
```bash
# ~/.bashrc / ~/.zshrc に追記（毎回ではなく恒久化）
stty intr ''
# 強制終了が必要なときは Ctrl+\ (SIGQUIT)
```
- レイヤ別の全面解説は `C:\Users\0501JP\win-tips\keyboard-layers.md`
- Windows Terminal のコピーは `Ctrl+Shift+C` へ（settings.json の keybindings）
- `trap '' INT`（プロセス内で無視）は `stty` と別層。用途で使い分け

### IP 到達監視
```powershell
& "$env:USERPROFILE\win-tips\ip-reach-monitor.ps1"   # 引数/設定はスクリプト内を確認
```

## 使い方のルール

1. どのトピックか決まったら、まず `C:\Users\0501JP\win-tips\<ファイル>` を `Read` して最新手順を確認する（ここは索引。詳細はファイルが正）
2. 実行前に戻せるか確認（`disable-copilot.ps1 -Revert` のような復元手段を提示する）
3. Android との同期の話が出たら **android-ftp-sync スキル** へ寄せる（スクリプト重複防止）
4. 小技は追加・修正したら `win-tips\README.md` の表も更新する（実体と索引の乖離防止）

## 検証コマンド
```powershell
Get-ChildItem -LiteralPath "$env:USERPROFILE\win-tips"   # 実体一覧
Test-Path -LiteralPath "$env:USERPROFILE\win-tips\README.md"
```

## 注意
- このスキル自身はグローバル（単一ソース `C:\Users\0501JP\.config\opencode\skills`）に置くため、どのエージェント／ディレクトリからもロードできる
- scripts は 管理者権限（elevation）が必要なものがある。実行時は権限状態を確認する