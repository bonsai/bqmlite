import os
import json

wp_dir = '/home/bons/.skills/wp'

results = []

for item in sorted(os.listdir(wp_dir)):
    item_path = os.path.join(wp_dir, item)
    if not os.path.isdir(item_path):
        continue
    
    files = os.listdir(item_path)
    
    # Key indicators
    has_main = 'main.py' in files or 'index.ts' in files
    has_agent = 'agent.json' in files or 'agents' in [d for d in os.listdir(item_path) if os.path.isdir(os.path.join(item_path, d))]
    has_script = any(f.endswith('.py') or f.endswith('.sh') for f in files)
    has_ts = any(f.endswith('.ts') for f in files)
    has_readme = 'README.md' in files
    
    desc = ''
    # Read README for description
    if has_readme:
        try:
            with open(os.path.join(item_path, 'README.md'), 'r', encoding='utf-8') as f:
                desc = f.read()[:200]
        except:
            pass
    
    # Read package.json
    if 'package.json' in files:
        try:
            with open(os.path.join(item_path, 'package.json'), 'r', encoding='utf-8') as f:
                pkg = json.load(f)
                desc += f"\nname: {pkg.get('name', '')}"
                desc += f"\nversion: {pkg.get('version', '')}"
        except:
            pass
    
    results.append({
        'name': item,
        'files': len(files),
        'desc': desc[:150],
        'has_agent': has_agent,
        'has_script': has_script,
        'has_main': has_main,
        'has_ts': has_ts,
    })

# Print all
for r in results:
    print(f"\n{'='*50}")
    print(f"{r['name']} (files={r['files']})")
    print(f"  agent: {r['has_agent']}, script: {r['has_script']}, main: {r['has_main']}, ts: {r['has_ts']}")
    print(f"  desc: {r['desc'][:100]}")