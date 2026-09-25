import os
import json

wp_dir = '/home/bons/.skills/wp'

# 各フォルダのメタデータを構築
items = []
for subdir in ['agt', 'txt', 'data', 'tool']:
    subdir_path = f'{wp_dir}/{subdir}'
    if not os.path.exists(subdir_path):
        continue
    for item in os.listdir(subdir_path):
        item_path = f'{subdir_path}/{item}'
        if os.path.isdir(item_path):
            # ファイル数と主なファイルを確認
            try:
                files = os.listdir(item_path)
                py_files = [f for f in files if f.endswith('.py')]
                ts_files = [f for f in files if f.endswith('.ts')]
                json_files = [f for f in files if f.endswith('.json')]
                md_files = [f for f in files if f.endswith('.md')]
            except:
                files = []
                py_files = []
                ts_files = []
                json_files = []
                md_files = []
            
            items.append({
                'name': item,
                'current': f'{subdir}/',
                'path': item_path,
                'file_count': len(files),
                'py_count': len(py_files),
                'ts_count': len(ts_files),
                'json_count': len(json_files),
                'md_count': len(md_files),
                'key_files': py_files[:3] + ts_files[:3],
            })

# root直下も追加
for item in os.listdir(wp_dir):
    if os.path.isdir(f'{wp_dir}/{item}') and item not in ['agt', 'txt', 'data', 'tool', '.', '_']:
        try:
            files = os.listdir(f'{wp_dir}/{item}')
        except:
            files = []
        items.append({
            'name': item,
            'current': 'root/',
            'path': f'{wp_dir}/{item}',
            'file_count': len(files),
            'py_count': 0,
            'ts_count': 0,
            'json_count': 0,
            'md_count': 0,
            'key_files': [],
        })

print(f"判定対象: {len(items)}個\n")

# 判定結果を保存
results = []
for item in items:
    # 単純なルールベース分類
    name = item['name'].lower()
    
    # エージェント
    if any(k in name for k in ['agent', 'ai', 'bot']):
        cat = 'agt'
    # テキスト生成
    elif any(k in name for k in ['rakugo', 'talk', 'script', 'literature', 'writing']):
        cat = 'txt'
    # データ・研究
    elif any(k in name for k in ['db', 'data', 'research', 'kankyou', 'pain', 'feeling']):
        cat = 'data'
    # 空フォルダ
    elif item['file_count'] == 0:
        cat = 'tool'
    # ツール
    else:
        cat = 'tool'
    
    results.append({
        'name': item['name'],
        'from': item['current'],
        'category': cat,
        'files': item['file_count'],
    })

# カテゴリ別表示
cats = {'agt': [], 'txt': [], 'data': [], 'tool': []}
for r in results:
    cats[r['category']].append(r)

print("=== Jev判定結果 ===\n")
for cat, label in [('agt', 'エージェント'), ('txt', 'テキスト生成'), ('data', 'データ・研究'), ('tool', 'ツール')]:
    print(f"[{cat}] {label} ({len(cats[cat])}個)")
    for r in sorted(cats[cat], key=lambda x: x['name']):
        print(f"  {r['from']}{r['name']} (files={r['files']})")
    print()

# JSONに保存
with open('/home/bons/.skills/.smb/jev_classification.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print("保存済み: /home/bons/.skills/.smb/jev_classification.json")