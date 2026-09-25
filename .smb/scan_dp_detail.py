import os
import json

dp_dir = '/home/bons/.skills/dp'

for item in sorted(os.listdir(dp_dir)):
    item_path = os.path.join(dp_dir, item)
    if not os.path.isdir(item_path):
        continue
    
    files = os.listdir(item_path)
    subdirs = [d for d in os.listdir(item_path) if os.path.isdir(os.path.join(item_path, d))]
    
    has_app = any('app' in f.lower() for f in files)
    has_manifest = 'manifest.json' in files or 'appxmanifest.xml' in files
    has_package = 'package.json' in files
    has_readme = 'README.md' in files
    
    main_html = [f for f in files if f == 'index.html']
    readme = [f for f in files if 'readme' in f.lower() and f.endswith('.md')]
    
    print(f"\n{'='*50}")
    print(f"{item}")
    print(f"  files={len(files)}, dirs={len(subdirs)}")
    
    # Check for README description
    for r in readme:
        rpath = os.path.join(item_path, r)
        try:
            with open(rpath, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f):
                    if i < 10:
                        print(f"  {line.strip()}")
        except:
            pass
    
    # Check package.json for description/name
    if has_package:
        ppath = os.path.join(item_path, 'package.json')
        try:
            with open(ppath, 'r', encoding='utf-8') as f:
                pkg = json.load(f)
                print(f"  name: {pkg.get('name', 'N/A')}")
                print(f"  desc: {pkg.get('description', 'N/A')[:80]}")
        except:
            pass
    
    print(f"  has_app: {has_app}")
    print(f"  has_manifest: {has_manifest}")