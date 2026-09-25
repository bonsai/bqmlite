import os, json, hashlib
from pathlib import Path
from datetime import datetime, timezone

SKILLS_DIR = Path('/home/bons/.skills')

def scan_dir(path):
    result = {
        'name': path.name,
        'path': str(path),
        'file_count': 0,
        'dir_count': 0,
        'has_skill_md': False,
        'has_git': False,
        'has_github_action': False,
        'has_readme': False,
        'size_bytes': 0,
        'updated': None,
        'created': None,
        'is_symlink': path.is_symlink(),
    }
    
    if not path.exists():
        return result
    
    try:
        stat = path.stat()
        result['created'] = datetime.fromtimestamp(stat.st_ctime).isoformat()
        result['updated'] = datetime.fromtimestamp(stat.st_mtime).isoformat()
    except:
        pass
    
    for root, dirs, files in os.walk(path):
        if 'SKILL.md' in files:
            result['has_skill_md'] = True
        if 'README.md' in files:
            result['has_readme'] = True
        if '.github' in dirs:
            result['has_github_action'] = True
        if '.git' in dirs:
            result['has_git'] = True
        result['dir_count'] += len(dirs)
        result['file_count'] += len(files)
    
    total_size = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            try:
                total_size += os.path.getsize(os.path.join(root, f))
            except:
                pass
    result['size_bytes'] = total_size
    result['hash'] = hashlib.sha256(str(path).encode()).hexdigest()[:12]
    
    return result

def scan_tree(path, depth=0, results=None):
    if results is None:
        results = []
    if depth > 2:
        return results
    
    for item in sorted(path.iterdir()):
        if item.name.startswith('.'):
            continue
        
        entry = {
            'name': item.name,
            'type': 'directory' if item.is_dir() else 'file',
            'depth': depth,
            'path': str(item),
            'scan': None,
            'parent_path': str(item.parent),
        }
        
        if item.is_dir():
            entry['scan'] = scan_dir(item)
        
        results.append(entry)
        if item.is_dir():
            scan_tree(item, depth + 1, results)
    
    return results

print("Scanning...")
tree = scan_tree(SKILLS_DIR)

items = []
for entry in tree:
    if entry['type'] == 'directory' and entry.get('scan'):
        s = entry['scan']
        items.append({
            'name': entry['name'],
            'path': s['path'],
            'depth': entry['depth'],
            'file_count': s['file_count'],
            'dir_count': s['dir_count'],
            'has_skill_md': s['has_skill_md'],
            'has_git': s['has_git'],
            'has_github_action': s['has_github_action'],
            'has_readme': s['has_readme'],
            'size_bytes': s['size_bytes'],
            'updated': s['updated'],
            'created': s['created'],
            'hash': s['hash'],
            'is_symlink': s['is_symlink'],
        })

def categorize(item):
    name = item['name'].lower()
    if item['has_skill_md']:
        return 'already-skill'
    if item.get('has_github_action') or name in ['emoji-shiritori', 'owarai-live', 'progressive-life-v2', 'showa-covers', 'yose-db', 'idol-playlist', 'idol-lab', 'makaizou-init']:
        return 'deployed'
    if name in ['bx', 'ex', 'ix', 'ox', 'px', 'sx', 'tx', 'ux', 'torissetsu', 'shitagaki', 'xx', 'xX']:
        return 'system-data'
    if name in ['ai-feelings', 'bons.ai', 'pain']:
        return 'agent'
    if name in ['rakugo-generator', 'research-rakugo', 'talk-db', 'talkscripts']:
        return 'text-generation'
    if name in ['kankyou-hub']:
        return 'data-research'
    return 'tool'

for item in items:
    item['category'] = categorize(item)

from collections import Counter
cat_counts = Counter(item['category'] for item in items)

report = {
    'generated': datetime.now(timezone.utc).isoformat(),
    'root': str(SKILLS_DIR),
    'total_items': len(items),
    'categories': dict(cat_counts),
    'items': items,
}

json_path = SKILLS_DIR / '.smb' / 'report_meta.json'
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
print(f"JSON: {json_path}")

# HTML生成
css = """
<style>
body { font-family: 'Segoe UI', sans-serif; margin: 20px; background: #f5f5f5; }
h1 { color: #333; }
.stats { display: flex; gap: 10px; margin: 20px 0; flex-wrap: wrap; }
.card { background: #fff; padding: 15px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); min-width: 120px; }
.card h3 { margin: 0; font-size: 28px; }
.card p { margin: 5px 0 0; color: #666; font-size: 13px; }
table { width: 100%; border-collapse: collapse; background: #fff; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
th { background: #333; color: #fff; padding: 10px; text-align: left; }
td { padding: 8px 10px; border-bottom: 1px solid #eee; }
tr:hover { background: #f9f9f9; }
.badge { display: inline-block; padding: 2px 10px; border-radius: 4px; font-size: 12px; font-weight: 600; color: #fff; }
.b-skill { background: #28a745; }
.b-deploy { background: #007bff; }
.b-agent { background: #6f42c1; }
.b-text { background: #fd7e14; }
.b-data { background: #20c997; }
.b-tool { background: #6c757d; }
.b-system { background: #dc3545; }
.meta { font-size: 11px; color: #999; }
</style>
"""

html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>.skills Report</title>
{css}
</head>
<body>
<div style="max-width: 1200px; margin: 0 auto;">
<h1>.skills Directory Report</h1>
<p>Generated: {report['generated']}</p>
<p>Total items: {report['total_items']}</p>

<div class="stats">
"""

for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
    badge_cls = f"b-{cat.split('-')[0]}" if cat != 'system-data' else 'b-system'
    html += f'<div class="card"><h3>{count}</h3><p>{cat}</p></div>\n'

html += """</div>
<h2>Items</h2>
<table>
<tr><th>Name</th><th>Category</th><th>Files</th><th>Size</th><th>SKILL.md</th><th>Git</th><th>GitHub</th><th>Updated</th></tr>
"""

for item in sorted(items, key=lambda x: (x['category'], x['name'])):
    cat = item['category']
    badge_cls = f"b-{cat.split('-')[0]}" if cat != 'system-data' else 'b-system'
    size_mb = item['size_bytes'] / (1024*1024)
    
    html += f"""<tr>
<td>{item['name']}</td>
<td><span class="badge {badge_cls}">{cat}</span></td>
<td>{item['file_count']}</td>
<td>{size_mb:.1f} MB</td>
<td>{"✓" if item["has_skill_md"] else "✗"}</td>
<td>{"✓" if item["has_git"] else "✗"}</td>
<td>{"✓" if item["has_github_action"] else "✗"}</td>
<td class="meta">{item['updated'] or ''}</td>
</tr>\n"""

html += """</table>
</div>
</body>
</html>"""

html_path = SKILLS_DIR / '.smb' / 'report.html'
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"HTML: {html_path}")