import os, json
from datetime import datetime, timezone

SKILLS_DIR = '/home/bons/.skills'

# wp → workspace にリネーム
wp_old = os.path.join(SKILLS_DIR, 'wp')
wp_new = os.path.join(SKILLS_DIR, 'workspace')
if os.path.exists(wp_old) and not os.path.exists(wp_new):
    os.rename(wp_old, wp_new)
    print('wp/ → workspace/')

# スキャン
items = []
for subdir in sorted(os.listdir(SKILLS_DIR)):
    subdir_path = os.path.join(SKILLS_DIR, subdir)
    if not os.path.isdir(subdir_path) or subdir.startswith('.'):
        continue
    
    for item in sorted(os.listdir(subdir_path)):
        item_path = os.path.join(subdir_path, item)
        if not os.path.isdir(item_path):
            continue
        
        has_skill_md = os.path.exists(os.path.join(item_path, 'SKILL.md'))
        has_git = os.path.isdir(os.path.join(item_path, '.git'))
        has_github = os.path.isdir(os.path.join(item_path, '.github'))
        has_deploy = 'index.html' in os.listdir(item_path) or any(f.endswith('.html') for f in os.listdir(item_path))
        
        is_deployed = (subdir == 'deployed') or (has_github and has_deploy)
        is_synced = has_github
        is_skill = has_skill_md
        
        try:
            file_count = sum(len(files) for _, _, files in os.walk(item_path))
        except:
            file_count = 0
        
        items.append({
            'parent': subdir,
            'name': item,
            'path': item_path,
            'is_skill': is_skill,
            'is_deployed': is_deployed,
            'is_synced': is_synced,
            'has_git': has_git,
            'has_github': has_github,
            'has_skill_md': has_skill_md,
            'has_deploy': has_deploy,
            'file_count': file_count,
        })

# カテゴリ分類
def classify(item):
    if item['is_skill']:
        return 'already-skill'
    if item['is_deployed']:
        return 'deployed'
    if item['parent'] in ['agent', 'text-generation']:
        return 'agent'
    if item['parent'] == 'data-research':
        return 'data-research'
    if item['parent'] == 'tool':
        return 'tool'
    if item['parent'] == 'system-data':
        return 'system-data'
    return 'tool'

for item in items:
    item['category'] = classify(item)

# JSONレポート
report = {
    'generated': datetime.now(timezone.utc).isoformat(),
    'total': len(items),
    'items': items,
}

json_path = os.path.join(SKILLS_DIR, '.smb', 'report.json')
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
print(f'JSON: {json_path}')

# HTMLレポート
cat_counts = {}
for item in items:
    cat = item['category']
    cat_counts[cat] = cat_counts.get(cat, 0) + 1

html = '''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>.skills Report</title>
<style>
body { font-family: 'Segoe UI', sans-serif; margin: 0; padding: 20px; background: #f8f9fa; }
.container { max-width: 1200px; margin: 0 auto; }
h1 { color: #333; }
.stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 10px; margin: 20px 0; }
.card { background: #fff; padding: 15px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.card h3 { margin: 0; font-size: 24px; color: #0066cc; }
.card p { margin: 5px 0 0; color: #666; font-size: 12px; }
table { width: 100%; border-collapse: collapse; background: #fff; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
th { background: #343a40; color: #fff; padding: 10px; text-align: left; }
td { padding: 8px 10px; border-bottom: 1px solid #dee2e6; }
tr:hover { background: #f8f9fa; }
.badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; color: #fff; }
.b-skill { background: #28a745; }
.b-deploy { background: #007bff; }
.b-agent { background: #6f42c1; }
.b-data { background: #20c997; }
.b-tool { background: #6c757d; }
.b-system { background: #dc3545; }
.icon { font-size: 14px; }
</style>
</head>
<body>
<div class="container">
<h1>.skills Report</h1>
<p>Generated: ''' + report['generated'] + '''</p>

<div class="stats">
'''

for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
    badge_class = f'b-{cat.split("-")[0]}' if cat != 'system-data' else 'b-system'
    html += f'<div class="card"><h3>{count}</h3><p>{cat}</p></div>\n'

html += '''</div>
<h2>Items</h2>
<table>
<tr>
<th>Name</th>
<th>Category</th>
<th>Skill</th>
<th>Deployed</th>
<th>GH Sync</th>
<th>Files</th>
</tr>
'''

for item in sorted(items, key=lambda x: (x['category'], x['name'])):
    badge_class = f'b-{item["category"].split("-")[0]}' if item['category'] != 'system-data' else 'b-system'
    icon = {'already-skill': '✅', 'deployed': '🚀', 'agent': '🤖', 'data-research': '📊', 'tool': '🔧', 'system-data': '❌'}
    
    html += f'''<tr>
<td>{icon.get(item['category'], '❓')} {item['name']}</td>
<td><span class="badge {badge_class}">{item['category']}</span></td>
<td class="icon">{'✅' if item['is_skill'] else '❌'}</td>
<td class="icon">{'✅' if item['is_deployed'] else '❌'}</td>
<td class="icon">{'✅' if item['is_synced'] else '❌'}</td>
<td>{item['file_count']}</td>
</tr>
'''

html += '''</table>
</div>
</body>
</html>'''

html_path = os.path.join(SKILLS_DIR, '.smb', 'report.html')
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'HTML: {html_path}')