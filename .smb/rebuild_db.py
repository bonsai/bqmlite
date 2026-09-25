import os, json, hashlib, csv, sqlite3
from datetime import datetime

smb_dir = '/home/bons/.skills/.smb'
db_path = os.path.join(smb_dir, 'skills.db')
skills_meta_jsonl = os.path.join(smb_dir, 'skills_meta.jsonl')

# Load JSONL metadata
skills_by_dir = {}
with open(skills_meta_jsonl, 'r', encoding='utf-8') as f:
    for line in f:
        skill = json.loads(line)
        skills_by_dir[skill['dir']] = skill

# Load _skills_log.jsonl for sid/hash8
log_entries = {}
log_path = os.path.join(smb_dir, '_skills_log.jsonl')
if os.path.exists(log_path):
    with open(log_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                entry = json.loads(line)
                name = entry.get('name') or entry.get('sid')
                log_entries[name] = entry
            except:
                pass

# Define categories
CATEGORIES = {
    'ai': 'AI/LLM',
    'data': 'データ処理',
    'editor': 'エディタ/生成',
    'footer': 'フッター/文体',
    'inventory': '棚卸し/台帳',
    'opencode': 'opencode関連',
    'rpa': 'UiPath RPA',
    'research': '調査/研究',
    'skill': 'スキル開発',
    'sync': '同期/設定',
    'system': 'システム/環境',
    'ui': 'UI/UX',
    'vocab': '語彙/言語',
    'web': 'Web/HTML',
    'writing': '文章生成',
    'other': 'その他'
}

def classify_skill(name, desc, md_files):
    name_lower = name.lower()
    desc_lower = (desc or '').lower()
    text = f'{name_lower} {desc_lower}'
    
    if any(k in text for k in ['uipath', 'rpa', 'maestro', 'flow']):
        return 'rpa'
    if any(k in text for k in ['jeva', 'bqmlite', 'ds-insighter', 'kenja', 'ai-feelings']):
        return 'ai'
    if any(k in text for k in ['genkou', 'rakugo', 'owarai', 'mimic-me']):
        return 'editor'
    if any(k in text for k in ['footer', 'meigen', 'eigo', 'tips-word', 'vocab-highlight']):
        return 'vocab'
    if any(k in text for k in ['ax', 'mx', 'wx', 'rx']):
        return 'ai'
    if any(k in text for k in ['skill-crawler', 'skill-consolidator', 'inventory', 'soubi', 'index']):
        return 'inventory'
    if any(k in text for k in ['pain-sense', 'pain']):
        return 'research'
    if any(k in text for k in ['opencode', 'pi-config', 'lm-hex']):
        return 'opencode'
    if any(k in text for k in ['writing', 'writing']):
        return 'writing'
    if any(k in text for k in ['lx']):
        return 'vocab'
    if any(k in text for k in ['sync-repos', 'check-repos', 'push']):
        return 'sync'
    if any(k in text for k in ['gen-favicon', 'emoji-shiritori', 'serve-html']):
        return 'web'
    if any(k in text for k in ['talkscripts', 'talk-db', 'yoshi', 'yose-db']):
        return 'data'
    return 'other'

# Build unified records
records = []
now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')

for dir_name, meta in sorted(skills_by_dir.items()):
    log = log_entries.get(dir_name, {})
    sha = hashlib.sha256(dir_name.encode()).hexdigest()[:8]
    
    record = {
        'sid': log.get('sid', f's{len(records)+1:03d}'),
        'hash8': log.get('hash8', sha),
        'name': dir_name,
        'frontmatter_name': meta.get('name', dir_name),
        'description': meta.get('description', ''),
        'source': log.get('source', 'unknown'),
        'path': log.get('path', ''),
        'categories': [classify_skill(dir_name, meta.get('description', ''), meta.get('md_files', []))],
        'tags': [],
        'status': 'OK' if meta['skill_md'] else 'NO_SKILL_MD',
        'has_skill_md': 1 if meta['skill_md'] else 0,
        'has_description': 1 if meta['description'] else 0,
        'line_count': 0,
        'desc_length': len(meta.get('description', '')),
        'file_count': meta['file_count'],
        'total_bytes': meta['total_bytes'],
        'plugins': log.get('plugins', []),
        'toplevel_files': {
            'tsv': len(meta['tsv_files']),
            'json': len(meta['json_files']),
            'md': len(meta['md_files']),
            'py': len(meta['py_files'])
        },
        'locations': ['wsl/.skills'],
        'is_symlink': 0,
        'crawled_at': now
    }
    records.append(record)

# Write CSV
csv_path = os.path.join(smb_dir, 'skills_index.csv')
with open(csv_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['sid','hash8','name','description','categories','status','file_count','total_bytes','plugins','locations','crawled_at'])
    for r in records:
        writer.writerow([
            r['sid'], r['hash8'], r['name'], r['description'][:100],
            ','.join(r['categories']), r['status'], r['file_count'],
            r['total_bytes'], '|'.join(r['plugins']),
            '|'.join(r['locations']), r['crawled_at']
        ])

print(f'Generated {len(records)} records')
print(f'CSV: {csv_path}')

from collections import Counter
cats = Counter()
for r in records:
    for c in r['categories']:
        cats[c] += 1
print('Categories:')
for k, v in sorted(cats.items()):
    print(f'  {k}: {v}')

# Now build proper SQLite DB
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Create new schema
c.execute('DROP TABLE IF EXISTS skills')
c.execute('DROP TABLE IF EXISTS skill_issues')
c.execute('DROP TABLE IF EXISTS categories')
c.execute('DROP TABLE IF EXISTS skill_categories')
c.execute('DROP TABLE IF EXISTS skill_files')

# Skills table
c.execute('''
CREATE TABLE skills (
    sid TEXT PRIMARY KEY,
    hash8 TEXT NOT NULL,
    name TEXT NOT NULL UNIQUE,
    frontmatter_name TEXT,
    description TEXT,
    source TEXT,
    path TEXT,
    status TEXT,
    has_skill_md INTEGER DEFAULT 0,
    has_description INTEGER DEFAULT 0,
    desc_length INTEGER DEFAULT 0,
    file_count INTEGER DEFAULT 0,
    total_bytes INTEGER DEFAULT 0,
    line_count INTEGER DEFAULT 0,
    is_symlink INTEGER DEFAULT 0,
    crawled_at TEXT,
    updated_at TEXT
)
''')

# Categories table
c.execute('''
CREATE TABLE categories (
    key TEXT PRIMARY KEY,
    label TEXT NOT NULL
)
''')

# Skill-categories junction table
c.execute('''
CREATE TABLE skill_categories (
    skill_sid TEXT NOT NULL,
    category_key TEXT NOT NULL,
    FOREIGN KEY (skill_sid) REFERENCES skills(sid),
    FOREIGN KEY (category_key) REFERENCES categories(key),
    PRIMARY KEY (skill_sid, category_key)
)
''')

# Skill-files table (top-level file inventory)
c.execute('''
CREATE TABLE skill_files (
    skill_sid TEXT NOT NULL,
    file_type TEXT NOT NULL,  -- 'tsv', 'json', 'md', 'py', 'skill_md', etc.
    file_path TEXT NOT NULL,
    file_count INTEGER DEFAULT 1,
    FOREIGN KEY (skill_sid) REFERENCES skills(sid)
)
''')

# Skill issues table
c.execute('''
CREATE TABLE skill_issues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_sid TEXT,
    skill_name TEXT,
    issue_type TEXT NOT NULL,
    detail TEXT,
    severity TEXT DEFAULT 'info',
    crawled_at TEXT
)
''')

# FTS5 virtual table for full-text search
c.execute('''
CREATE VIRTUAL TABLE skills_fts USING fts5(
    name, description,
    content='skills',
    content_rowid='rowid'
)
''')

# Insert categories
cat_data = [(k, v) for k, v in CATEGORIES.items()]
c.executemany('INSERT INTO categories VALUES (?, ?)', cat_data)

# Insert skills
for r in records:
    c.execute('''
        INSERT OR REPLACE INTO skills (sid, hash8, name, frontmatter_name, description, source, path, 
            status, has_skill_md, has_description, desc_length, file_count, total_bytes, line_count, 
            is_symlink, crawled_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        r['sid'], r['hash8'], r['name'], r['frontmatter_name'], r['description'],
        r['source'], r['path'], r['status'], r['has_skill_md'], r['has_description'],
        r['desc_length'], r['file_count'], r['total_bytes'], r['line_count'],
        r['is_symlink'], r['crawled_at'], r['crawled_at']
    ))

# Insert skill-categories
for r in records:
    for cat in r['categories']:
        c.execute('INSERT INTO skill_categories VALUES (?, ?)', (r['sid'], cat))

# Insert skill_files
for r in records:
    tf = r['toplevel_files']
    if tf['tsv'] > 0:
        c.execute('INSERT INTO skill_files VALUES (?, ?, ?, ?)', (r['sid'], 'tsv', f'{r["name"]}/*.tsv', tf['tsv']))
    if tf['json'] > 0:
        c.execute('INSERT INTO skill_files VALUES (?, ?, ?, ?)', (r['sid'], 'json', f'{r["name"]}/**/*.json', tf['json']))
    if tf['md'] > 0:
        c.execute('INSERT INTO skill_files VALUES (?, ?, ?, ?)', (r['sid'], 'md', f'{r["name"]}/**/*.md', tf['md']))
    if tf['py'] > 0:
        c.execute('INSERT INTO skill_files VALUES (?, ?, ?, ?)', (r['sid'], 'py', f'{r["name"]}/**/*.py', tf['py']))
    if r['has_skill_md']:
        c.execute('INSERT INTO skill_files VALUES (?, ?, ?, ?)', (r['sid'], 'SKILL.md', f'{r["name"]}/SKILL.md', 1))

# Insert FTS
for r in records:
    c.execute('INSERT INTO skills_fts (rowid, name, description) VALUES (?, ?, ?)',
              (records.index(r), r['name'], r['description'][:200]))

# Create indexes
c.execute('CREATE INDEX idx_skills_status ON skills(status)')
c.execute('CREATE INDEX idx_skills_hash8 ON skills(hash8)')
c.execute('CREATE INDEX idx_skills_categories ON skills(sid)')
c.execute('CREATE INDEX idx_skill_files_type ON skill_files(file_type)')

conn.commit()

# Verify
print('\n=== DB Verification ===')
c.execute('SELECT COUNT(*) FROM skills')
print(f'Skills: {c.fetchone()[0]}')
c.execute('SELECT COUNT(*) FROM categories')
print(f'Categories: {c.fetchone()[0]}')
c.execute('SELECT COUNT(*) FROM skill_categories')
print(f'Skill-Categories: {c.fetchone()[0]}')
c.execute('SELECT COUNT(*) FROM skill_files')
print(f'Skill-Files: {c.fetchone()[0]}')
c.execute('SELECT COUNT(*) FROM skills_fts')
print(f'FTS records: {c.fetchone()[0]}')

# Sample query
print('\n=== Category Distribution ===')
c.execute('''
    SELECT c.key, c.label, COUNT(sc.skill_sid) as cnt
    FROM categories c
    LEFT JOIN skill_categories sc ON c.key = sc.category_key
    GROUP BY c.key
    ORDER BY cnt DESC
''')
for row in c.fetchall():
    print(f'  {row[1]} ({row[0]}): {row[2]}')

# Sample query
print('\n=== Sample Skills ===')
c.execute('SELECT sid, name, frontmatter_name, status, categories FROM skills LIMIT 5')
for row in c.fetchall():
    print(f'  {row[0]} | {row[1]} | {row[2]} | {row[3]}')

conn.close()
print(f'\nDB rebuilt: {db_path}')