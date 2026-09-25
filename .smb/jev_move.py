import os, json

wp_dir = '/home/bons/.skills/wp'

# Jev分類結果をロード
with open('/home/bons/.skills/.smb/jev_classification.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

moved = []
for r in results:
    name = r['name']
    from_dir = r['from'].rstrip('/')
    to_dir = r['category']
    
    # 現在のパス
    src = os.path.join(wp_dir, from_dir, name) if from_dir != 'root' else os.path.join(wp_dir, name)
    # 新しいパス
    dst = os.path.join(wp_dir, to_dir, name)
    
    if os.path.exists(src) and not os.path.exists(dst):
        os.rename(src, dst)
        moved.append({
            'name': name,
            'from': from_dir,
            'to': to_dir,
            'files': r['files'],
        })

# 空ディレクトリを削除
for subdir in ['agt', 'txt', 'data', 'tool']:
    subdir_path = os.path.join(wp_dir, subdir)
    if os.path.exists(subdir_path) and not os.listdir(subdir_path):
        os.rmdir(subdir_path)
        print(f"Removed empty: {subdir}/")

print(f"Moved {len(moved)} items:\n")
for m in sorted(moved, key=lambda x: (x['to'], x['name'])):
    print(f"  {m['from']}/{m['name']} -> {m['to']}/ ({m['files']} files)")