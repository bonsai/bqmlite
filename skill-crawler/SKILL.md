---
name: skill-crawler
description: 全プラットフォーム（Windows / WSL / repos）から「使えるスキル」を探索して棚卸しする。「skillクローラ」「skill crawler」「スキルを探す」「スキル棚卸し」「全部のスキル」「どのスキルがある?」「skna検索」「スキル一覧」などで発動。opencode/pi/Claude Code など異なるエージェントからでも、C:\Users\0501JP\.config\opencode\skills（単一ソース）、~/.agents/skills、~/.claude/skills、symlink実体（repos/my-skills 等）を走査し、存在・種別（dir/symlink/壊れ）・SKILL.md有無・フロントマター不一致・重複を一覧化する。
---

# skill-crawler — スキル棚卸しクローラ

異なるエージェント（opencode / pi / Claude Code）からでも「今どのスキルがあるか、どこにあるか、生きているか」を正確に把握するための探索スキル。

## 走査対象（このマシンの配置ルール）

| # | 場所 | 種別 |
|---|------|------|
| 1 | `C:\Users\0501JP\.config\opencode\skills\*` | **単一ソース（集約先）** |
| 2 | `C:\Users\0501JP\.agents\skills\*` | opencode 外部接続（~/.agents 自動ロード） |
| 3 | `C:\Users\0501JP\.claude\skills\*` | 外部接続（~/.claude 自動ロード） |
| 4 | `\\wsl.localhost\Ubuntu\home\bons\.config\opencode\skills` | WSL→Windows への symlink（同一） |
| 5 | `\\wsl.localhost\Ubuntu\home\bons\.agents\skills\*` | WSL 外部接続（symlink 実体 は repos/ を参照し得る） |
| 6 | `\\wsl.localhost\Ubuntu\home\bons\repos\my-skills\*` | スキル実体のリポジトリ |
| 7 | `\\wsl.localhost\Ubuntu\home\bons\github-api-skill` | （実体が存在しない壊れリンク例） |

> 2026-09-18 に WSL `.opencode/skills` は Windows グローバルへ統合・削除済み。今後スキルは **#1 に一本化** する。クローラは残骸（壊れ symlink・重複）の発見が主目的。

## 出力項目（スキルごと）

- `name`（フォルダ名）＋ 場所
- 種別: `dir` / `symlink`（実体表示） / `BROKEN`（実体消失）
- `SKILL.md` 有無（無い＝ロードされない=死亡）
- frontmatter: `name` がフォルダ名と一致するか / `description` 有無（無い＝モデルに見えない）
- 重複: 同名が複数場所にあるか

## 実行手順（PowerShell・Windows opencode）

```powershell
$roots = @(
  'C:\Users\0501JP\.config\opencode\skills',
  'C:\Users\0501JP\.agents\skills',
  'C:\Users\0501JP\.claude\skills',
  '\\wsl.localhost\Ubuntu\home\bons\.agents\skills',
  '\\wsl.localhost\Ubuntu\home\bons\repos\my-skills'
)
foreach ($r in $roots) {
  if (-not (Test-Path -LiteralPath $r)) { Write-Output "MISS: $r"; continue }
  Get-ChildItem -LiteralPath $r -Force -ErrorAction SilentlyContinue | ForEach-Object {
    $kind = if ($_.LinkType) { "symlink->$($_.Target)" } else { "dir" }
    $skillMd = Join-Path $_.FullName 'SKILL.md'
    $has = if (Test-Path -LiteralPath $skillMd) { 'SKILL.md:YES' } else { 'SKILL.md:NO(死亡)' }
    Write-Output ("{0,-22} {1,-24} {2}" -f $_.Name, $kind, $has)
  }
}
```

WSL 内 shell で走査する場合（pi 等）:
```bash
for r in ~/.config/opencode/skills ~/.agents/skills ~/.claude/skills ~/repos/my-skills; do
  [ -d "$r" ] && find "$r" -maxdepth 1 -mindepth 1 | while read -r s; do
    if [ -L "$s" ]; then t="$(readlink "$s")"; [ -e "$s" ] && k="symlink->$t" || k="BROKEN->$t"
    else k="dir"; fi
    [ -f "$s/SKILL.md" ] && m=YES || m=NO
    printf '%-22s %-28s SKILL.md:%s\n' "$(basename "$s")" "$k" "$m"
  done
done
```

## 判定ルール

1. `BROKEN` symlink → 実体が消えている。物理コピー不可能。削除候補（skill-consolidator で報告）
2. `SKILL.md:NO` → opencode にロードされない。空フォルダは削除候補
3. frontmatter `name` がフォルダ名と不一致 / description 無し → ロードの問題。是正候補
4. 同名が #1 と他に両方ある → 重複。スキル名は全場所で一意が必要（loader が混乱）
5. #1 が単一ソース → 他の場所の実体は **コピーして #1 へ、原本は削除or統合** が基本方針

## 検証（エージェントはこの順で確認する）

1. 全 root を走査して表に出す（上記コマンド）
2. `skill-crawler` だけで ok → 単一ソース維持
3. `SKILL.md:NO` / `BROKEN` / 不一致 / 重複 があれば → **skill-consolidator** を起動して解消
4. 全員（opencode / pi / Claude Code）から見えるかは `name` + `description` の有無で確認

## 注意

- WSL のシェルは `bash`、Windows は PowerShell で走査コマンドが異なる。エージェントは使える方を選ぶ
- symlink の実体だけをコピーする（リンクごとコピーしない）
- このスキル自身は #1（単一ソース）にあるので、どのエージェントからもロードできる