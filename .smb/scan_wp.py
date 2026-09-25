import os

wp_dir = '/home/bons/.skills/wp'

for item in sorted(os.listdir(wp_dir)):
    item_path = os.path.join(wp_dir, item)
    if not os.path.isdir(item_path):
        continue
    
    files = os.listdir(item_path)
    
    has_html = any(f.endswith('.html') for f in files)
    has_package = 'package.json' in files
    has_dist = any(d == 'dist' for d in os.listdir(item_path) if os.path.isdir(os.path.join(item_path, d)))
    has_build = any(d == 'build' for d in os.listdir(item_path) if os.path.isdir(os.path.join(item_path, d)))
    has_gh_pages = any(d == '.github' for d in os.listdir(item_path) if os.path.isdir(os.path.join(item_path, d)))
    has_public = any(d == 'public' for d in os.listdir(item_path) if os.path.isdir(os.path.join(item_path, d)))
    
    indicators = []
    if has_html: indicators.append('html')
    if has_package: indicators.append('package.json')
    if has_dist: indicators.append('dist/')
    if has_build: indicators.append('build/')
    if has_gh_pages: indicators.append('.github/')
    if has_public: indicators.append('public/')
    
    marker = ",".join(indicators) if indicators else "(tools)"
    print(f"{item:35s} files={len(files):4d}  {marker}")