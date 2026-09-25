#!/usr/bin/env python3
"""
弁慶 スキル棚卸し + DB構築 + DS分析 一括スクリプト
"""

import os, json, hashlib, sqlite3, subprocess, re
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter, defaultdict

# ===== CONFIG =====
SKILLS_WSL = "/home/bons/.skills"
SKILLS_WIN = "/mnt/c/Users/0501JP/.config/opencode/skills"
SKILLS_LOG = "/home/bons/.skills/_skills_log.jsonl"
SKILLS_DB = "/home/bons/.skills/skills.db"
OUTPUT_DIR = "/home/bons/.skills/output"
SKIP = {
    "README.md", "INDEX.md", "skills.catalog.json", "scripts_push.sh",
    "_inventory_before.gh.txt", "_inventory_before.local.txt",
    "_inventory_before.md", "_inventory_before.rows.tsv",
    ".git", ".github", ".vscode",
    "pain", "SHITAGAKI", "TORISETSU", "natalie", "play-mp4",
    "ai-feelings", "chatgpt-ext", "gen-favicon", "hakkutu",
    "kankyou-hub", "kenja", "leanvj", "makaizou-init",
    "owarai-live", "repo-theme-conversion", "research-by-bookmark",
    "research-rakugo", "showa-covers", "supervised-delegation",
    "talkscripts", "vanilla-web-dev", "voice-bbs-dev",
    "wf-errors", "yose-db", "yoshimoto-theater",
    "daihon", "daily-ss", "bbs-manager", "bons.ai",
    "dev-sprint10", "emoji-shiritori", "exercise-automation",
    "ext-install", "ext-install-skill", "lm-hex-eval",
    "portmanager", "progressive-life-temp", "progressive-life-v2",
    "scoop-java-kotlin-clj", "svn-skill", "sync-db",
    "talk-db", "sync-repos", "ux-guardian", "wt-startdir",
    "xX", "PX", "TX", "LX", "OX", "UX", "BX", "EX", "IX", "SX", "XX",
}

def scan_dirs(base):
    """Scan directories for subdirs."""
    try:
        entries = os.listdir(base)
        dirs = [e for e in entries if os.path.isdir(os.path.join(base, e))]
        return sorted(dirs)
    except:
        return []

def get_symlinks(base):
    """Get symlinks info."""
    result = {}
    try:
        for name in os.listdir(base):
            full = os.path.join(base, name)
            if os.path.islink(full):
                target = os.readlink(full)
                result[name] = {"target": target, "exists": os.path.exists(full)}
    except:
        pass
    return result

def parse_frontmatter(content):
    """Extract name and description from SKILL.md frontmatter."""
    fm_name = None
    fm_desc = None
    in_fm = False
    for line in content.split('\n'):
        stripped = line.strip()
        if stripped == '---':
            if not in_fm:
                in_fm = True
            else:
                break
        elif in_fm:
            m = re.match(r'^(\w+):\s*(.+)$', stripped)
            if m:
                key, val = m.group(1), m.group(2).strip().strip('"').strip("'")
                if val:
                    if key == 'name':
                        fm_name = val
                    elif key == 'description':
                        fm_desc = val
    return fm_name, fm_desc

def read_file(path):
    """Read file content."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return None

def sha256_short(s):
    """SHA-256 of string, first 8 hex chars."""
    return hashlib.sha256(s.encode()).hexdigest()[:8]

# ===== MAIN =====
print("=" * 60)
print(" 弁慶 スキル棚卸し + DB構築 + DS分析")
print("=" * 60)

# --- Step 1: Scan ---
print("\n[1] スキル一覧スキャン中...")
opencode_dirs = scan_dirs(SKILLS_WIN)
wsl_dirs = scan_dirs(SKILLS_WSL)
wsl_symlinks = get_symlinks(SKILLS_WSL)

opencode_set = set(opencode_dirs)
wsl_set = set(wsl_dirs)
all_names = sorted(opencode_set | wsl_set)

print(f"  opencode/skills: {len(opencode_set)}")
print(f"  .skills/ (dir):  {len(wsl_set)}")
print(f"  symlinks:        {len(wsl_symlinks)}")
print(f"  合計一意:         {len(all_names)}")

# --- Step 2: Crawl ---
print("\n[2] SKILL.md フロントマター解析中...")

duplicates = {}
broken_symlinks = []
no_skill_md = []
fm_issues = []
records = []

for name in all_names:
    if name in SKIP:
        continue
    
    # Locations
    locs = []
    if name in opencode_set:
        locs.append("opencode/skills")
    if name in wsl_set:
        locs.append("wsl/.skills")
    
    # Duplicates
    if len(locs) > 1:
        duplicates[name] = locs
    
    # Symlink check
    is_symlink = name in wsl_symlinks
    sym_info = wsl_symlinks.get(name, {})
    
    if is_symlink and not sym_info.get("exists", True):
        broken_symlinks.append({"name": name, "target": sym_info.get("target", "?")})
    
    # SKILL.md check
    check_path = None
    if name in opencode_set:
        check_path = os.path.join(SKILLS_WIN, name, "SKILL.md")
    else:
        check_path = os.path.join(SKILLS_WSL, name, "SKILL.md")
    
    content = read_file(check_path)
    has_md = content is not None and len(content) > 10
    status = "OK"
    
    if is_symlink and not sym_info.get("exists", True):
        status = "BROKEN_SYMLINK"
    elif not has_md:
        status = "NO_SKILL_MD"
        no_skill_md.append({"name": name, "locations": locs})
    
    # Frontmatter
    fm_name = None
    fm_desc = None
    line_count = 0
    
    if has_md:
        lines = [l for l in content.split('\n') if l.strip()]
        line_count = len(lines)
        fm_name, fm_desc = parse_frontmatter(content)
        
        if fm_name and fm_name != name:
            fm_issues.append({"name": name, "issue": "frontmatter_name_mismatch",
                            "detail": f"expected={name} actual={fm_name}"})
        if not fm_desc:
            fm_issues.append({"name": name, "issue": "no_description",
                            "detail": "no_description_found"})
    
    desc_len = len(fm_desc) if fm_desc else 0
    
    records.append({
        "name": name,
        "locations": ";".join(locs),
        "is_symlink": is_symlink,
        "status": status,
        "has_skill_md": has_md,
        "frontmatter_name": fm_name,
        "has_description": bool(fm_desc),
        "line_count": line_count,
        "desc_length": desc_len,
    })

print(f"  解析済みスキル: {len(records)}")
print(f"  重複: {len(duplicates)} 壊れ: {len(broken_symlinks)} SKILL.md欠落: {len(no_skill_md)} FM問題: {len(fm_issues)}")

# --- Step 3: Save crawl data ---
print("\n[3] 結果保存中...")
os.makedirs(OUTPUT_DIR, exist_ok=True)

crawl_data = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "summary": {
        "total_unique": len(all_names),
        "crawled": len(records),
        "duplicates_count": len(duplicates),
        "broken_symlinks_count": len(broken_symlinks),
        "no_skill_md_count": len(no_skill_md),
        "fm_issues_count": len(fm_issues),
        "opencode_count": len(opencode_set),
        "wsl_count": len(wsl_set),
    },
    "duplicates": duplicates,
    "broken": broken_symlinks,
    "no_skill_md": no_skill_md,
    "fm_issues": fm_issues,
}

with open("/home/bons/.skills/crawl_result.json", "w") as f:
    json.dump(crawl_data, f, indent=2, ensure_ascii=False)

# Save TSVs
# Duplicates
with open(f"{OUTPUT_DIR}/02_duplicates.tsv", "w") as f:
    f.write("name\twindows\tws\n")
    for name, locs in sorted(duplicates.items()):
        f.write(f"{name}\t{'Y' if 'opencode/skills' in locs else 'N'}\t{'Y' if 'wsl/.skills' in locs else 'N'}\n")

# Broken symlinks
with open(f"{OUTPUT_DIR}/03_broken_links.tsv", "w") as f:
    f.write("name\ttarget\n")
    for b in broken_symlinks:
        f.write(f"{b['name']}\t{b['target']}\n")

# No SKILL.md
with open(f"{OUTPUT_DIR}/04_no_skill_md.tsv", "w") as f:
    f.write("name\topencode\tws\n")
    for n in no_skill_md:
        locs = n["locations"]
        f.write(f"{n['name']}\t{'Y' if 'opencode/skills' in locs else 'N'}\t{'Y' if 'wsl/.skills' in locs else 'N'}\n")

# FM issues
with open(f"{OUTPUT_DIR}/05_fm_issues.tsv", "w") as f:
    f.write("name\tissue\tdetail\n")
    for i in fm_issues:
        f.write(f"{i['name']}\t{i['issue']}\t{i['detail']}\n")

print(f"  crawl_result.json + TSV files -> {OUTPUT_DIR}/")

# --- Step 4: Update _skills_log.jsonl ---
print("\n[4] _skills_log.jsonl 更新中...")

with open(SKILLS_LOG, "a") as f:
    for rec in records:
        entry = {
            "sid": rec["name"],
            "hash8": sha256_short(rec["name"]),
            "name": rec["name"],
            "locations": rec["locations"].split(";"),
            "status": rec["status"],
            "has_skill_md": rec["has_skill_md"],
            "has_description": rec["has_description"],
            "line_count": rec["line_count"],
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

print("  _skills_log.jsonl appended")

# --- Step 5: Build SQLite DB ---
print("\n[5] skills.db 構築中...")

conn = sqlite3.connect(SKILLS_DB)
c = conn.cursor()

c.executescript("""
    DROP TABLE IF EXISTS skills;
    DROP TABLE IF EXISTS skill_issues;
    CREATE TABLE skills (
        name TEXT PRIMARY KEY,
        locations TEXT,
        is_symlink INTEGER,
        status TEXT,
        has_skill_md INTEGER,
        frontmatter_name TEXT,
        has_description INTEGER,
        line_count INTEGER,
        desc_length INTEGER,
        crawled_at TEXT
    );
    CREATE TABLE skill_issues (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        skill_name TEXT,
        issue_type TEXT,
        detail TEXT,
        crawled_at TEXT
    );
    CREATE INDEX idx_s_status ON skills(status);
    CREATE INDEX idx_s_has_desc ON skills(has_description);
    CREATE INDEX idx_s_lines ON skills(line_count);
    CREATE INDEX idx_s_desc_len ON skills(desc_length);
""")

now = datetime.now(timezone.utc).isoformat()

for rec in records:
    c.execute("""
        INSERT OR REPLACE INTO skills 
        (name,locations,is_symlink,status,has_skill_md,frontmatter_name,
         has_description,line_count,desc_length,crawled_at)
        VALUES (?,?,?,?,?,?,?,?,?,?)
    """, (
        rec["name"], rec["locations"],
        1 if rec["is_symlink"] else 0, rec["status"],
        1 if rec["has_skill_md"] else 0, rec["frontmatter_name"],
        1 if rec["has_description"] else 0,
        rec["line_count"], rec["desc_length"], now
    ))

for name in duplicates:
    c.execute("INSERT INTO skill_issues (skill_name, issue_type, detail, crawled_at) VALUES (?,?,?,?)",
              (name, "duplicate", json.dumps(duplicates[name]), now))

for b in broken_symlinks:
    c.execute("INSERT INTO skill_issues (skill_name, issue_type, detail, crawled_at) VALUES (?,?,?,?)",
              (b["name"], "broken_symlink", b["target"], now))

for i in fm_issues:
    c.execute("INSERT INTO skill_issues (skill_name, issue_type, detail, crawled_at) VALUES (?,?,?,?)",
              (i["name"], i["issue"], i["detail"], now))

conn.commit()

# Verify
total = c.execute("SELECT COUNT(*) FROM skills").fetchone()[0]
issues = c.execute("SELECT COUNT(*) FROM skill_issues").fetchone()[0]
print(f"  skills: {total} rows, skill_issues: {issues} rows")
conn.close()
print("  skills.db 構築完了")

# --- Step 6: DS Analysis ---
print("\n[6] DS 分析開始...")

# Re-read DB for analysis
conn = sqlite3.connect(SKILLS_DB)
c = conn.cursor()

# 6a. Category distribution (by skill name prefix)
print("\n  [6a] カテゴリ別分布 (名前プレフィックスで分類)...")
categorized = defaultdict(int)
for name in [r[0] for r in c.execute("SELECT name FROM skills").fetchall()]:
    if name.startswith("uipath-"):
        categorized["UiPath"] += 1
    elif name.startswith("uipath-maestro"):
        categorized["UiPath-Maestro"] -= 1  # will be adjusted
    elif name.startswith("uipath-"):
        categorized["UiPath-Other"] += 1
    elif name.startswith("ax"):
        categorized["AX"] += 1
    elif name.startswith("bqmlite"):
        categorized["BQMLite"] += 1
    elif name.startswith("char-distribution"):
        categorized["CharDist"] += 1
    elif name.startswith("footer"):
        categorized["Footer"] += 1
    elif name.startswith("grill-me"):
        categorized["Grill"] += 1
    elif name.startswith("lx"):
        categorized["LX"] += 1
    elif name.startswith("mimic-me"):
        categorized["Mimic"] += 1
    elif name.startswith("mx"):
        categorized["MX"] += 1
    elif name.startswith("pain"):
        categorized["Pain"] += 1
    elif name.startswith("recap"):
        categorized["Recap"] += 1
    elif name.startswith("skill-consolidator"):
        categorized["SkillTools"] += 1
    elif name.startswith("skill-crawler"):
        categorized["SkillTools"] += 1
    elif name.startswith("tips-word"):
        categorized["TipsWord"] += 1
    elif name.startswith("tsumete"):
        categorized["Tsumete"] += 1
    elif name.startswith("vocab-highlight"):
        categorized["Vocab"] += 1
    elif name.startswith("win-tips"):
        categorized["WinTips"] += 1
    elif name.startswith("writing"):
        categorized["Writing"] += 1
    elif name.startswith("wx"):
        categorized["WX"] += 1
    elif name.startswith("wsl-migrate"):
        categorized["Infra"] += 1
    elif name.startswith("check-repos"):
        categorized["Infra"] += 1
    elif name.startswith("pi-config"):
        categorized["Infra"] += 1
    else:
        categorized["Other"] += 1

# Fix maestro double counting
maestro_count = c.execute("SELECT COUNT(*) FROM skills WHERE name LIKE 'uipath-maestro%'").fetchone()[0]
c.execute("DELETE FROM skills WHERE name LIKE 'uipath-maestro%'")
categorized["UiPath-Maestro"] = maestro_count
total_ui = c.execute("SELECT COUNT(*) FROM skills WHERE name LIKE 'uipath-%' AND name NOT LIKE 'uipath-maestro%'").fetchone()[0]
categorized["UiPath-Other"] = total_ui

categorized_sorted = sorted(categorized.items(), key=lambda x: -x[1])
print("  カテゴリ別:")
for cat, count in categorized_sorted:
    print(f"    {cat:20s}: {count:3d}")

# 6b. Line count statistics
print("\n  [6b] 行数統計...")
rows = c.execute("SELECT line_count FROM skills").fetchall()
lines = [r[0] for r in rows if r[0] > 0]
if lines:
    print(f"    最小: {min(lines):4d}行  最大: {max(lines):4d}行  平均: {sum(lines)/len(lines):.1f}行  中央値: {sorted(lines)[len(lines)//2]:4d}行")

# 6c. Description length statistics
print("\n  [6c] 説明長統計...")
rows = c.execute("SELECT desc_length FROM skills").fetchall()
desc_lens = [r[0] for r in rows if r[0] > 0]
if desc_lens:
    print(f"    最小: {min(desc_lens):4d}文字  最大: {max(desc_lens):4d}文字  平均: {sum(desc_lens)/len(desc_lens):.1f}文字")
else:
    print("    説明長データなし")

# 6d. Duplicate descriptions
print("\n  [6d] 類似説明の検出...")
rows = c.execute("SELECT name, frontmatter_name FROM skills WHERE has_skill_md=1 AND frontmatter_name IS NOT NULL").fetchall()
name_groups = defaultdict(list)
for name, fm_name in rows:
    if fm_name:
        name_groups[fm_name].append(name)

dup_descs = {k: v for k, v in name_groups.items() if len(v) > 1}
if dup_descs:
    print(f"    frontmatter_name 重複グループ: {len(dup_descs)} 個")
    for desc, names in list(dup_descs.items())[:5]:
        print(f"      '{desc}' -> {names}")
else:
    print("    重複なし")

# 6e. Missing descriptions
print("\n  [6e] 未定義 description の検出...")
no_desc = c.execute("SELECT name FROM skills WHERE has_skill_md=1 AND has_description=0").fetchall()
print(f"    SKILL.mdは存在するが description 未定義: {len(no_desc)} 個")
for r in no_desc[:10]:
    print(f"      - {r[0]}")

# 6f. Status breakdown
print("\n  [6f] ステータス別...")
status_rows = c.execute("SELECT status, COUNT(*) FROM skills GROUP BY status").fetchall()
for status, count in status_rows:
    print(f"    {status:20s}: {count:3d}")

# 6g. Core insights
print("\n  [6g] コアインサイト...")
total_skills = c.execute("SELECT COUNT(*) FROM skills").fetchone()[0]
with_desc = c.execute("SELECT COUNT(*) FROM skills WHERE has_description=1").fetchone()[0]
with_md = c.execute("SELECT COUNT(*) FROM skills WHERE has_skill_md=1").fetchone()[0]
dup_count = c.execute("SELECT COUNT(*) FROM skill_issues WHERE issue_type='duplicate'").fetchone()[0]
broken_count = c.execute("SELECT COUNT(*) FROM skill_issues WHERE issue_type='broken_symlink'").fetchone()[0]

insights = []

# Insight 1: Coverage
coverage = with_desc / total_skills * 100 if total_skills > 0 else 0
insights.append(f"① 説明カバレッジ: {coverage:.0f}% ({with_desc}/{total_skills}) - description が未定義のスキルが残り{total_skills - with_desc}個")

# Insight 2: Duplicate locations
insights.append(f"② 重複配置: {dup_count} 個のスキルが複数場所で重複 - {list(duplicates.keys())[:5]}...")

# Insight 3: Broken symlinks
insights.append(f"③ 壊れリンク: {broken_count} 個のシンボリックリンクが実体消失")

# Insight 4: UiPath dominance
uipath_count = c.execute("SELECT COUNT(*) FROM skills WHERE name LIKE 'uipath-%'").fetchone()[0]
insights.append(f"④ UiPath 集中: {uipath_count}/{total_skills} ({uipath_count/total_skills*100:.0f}%) のスキルが UiPath - 他分野のスキルが希薄")

# Insight 5: Average size
avg_lines = c.execute("SELECT AVG(line_count) FROM skills WHERE line_count > 0").fetchone()[0]
insights.append(f"⑤ 平均規模: {avg_lines:.0f} 行/SKILL.md - 簡潔な定義と冗長な定義の分散が目立つ")

for i in insights:
    print(f"    {i}")

# Save insights
insights_text = "\n".join(insights)
with open(f"{OUTPUT_DIR}/07_insights.txt", "w") as f:
    f.write(insights_text)

# Save full analysis
analysis = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "insights": insights,
    "category_distribution": dict(categorized_sorted),
    "statistics": {
        "total_skills": total_skills,
        "with_description": with_desc,
        "with_skill_md": with_md,
        "coverage_pct": round(coverage, 1),
        "avg_line_count": round(avg_lines, 1),
        "duplicates": dup_count,
        "broken_symlinks": broken_count,
        "uipath_count": uipath_count,
    },
}
with open(f"{OUTPUT_DIR}/08_analysis.json", "w") as f:
    json.dump(analysis, f, indent=2, ensure_ascii=False)

conn.close()

# Save records JSON
with open(f"{OUTPUT_DIR}/06_skill_records.json", "w") as f:
    json.dump(records, f, indent=2, ensure_ascii=False)

print("\n" + "=" * 60)
print(" 全工程完了!")
print("=" * 60)
print(f"\n出力ファイル一覧 ({OUTPUT_DIR}/):")
for fname in sorted(os.listdir(OUTPUT_DIR)):
    fpath = os.path.join(OUTPUT_DIR, fname)
    size = os.path.getsize(fpath)
    print(f"  {fname:35s} {size:>8d} bytes")