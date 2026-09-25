import os

SKILLS_DIR = '/home/bons/.skills'

# リネームマッピング（略称 → 完全名称）
rename_map = {
    'sk': 'skill',
    'dp': 'deployed',
    'agt': 'agent',
    'txt': 'text-generation',
    'data': 'data-research',
    'tool': 'tool',
    'x': 'system-data',
}

moved = []

for old_name, new_name in rename_map.items():
    src = os.path.join(SKILLS_DIR, old_name)
    dst = os.path.join(SKILLS_DIR, new_name)
    
    if os.path.exists(src) and not os.path.exists(dst):
        os.rename(src, dst)
        moved.append(f'{old_name} -> {new_name}')
        print(f'  {old_name}/ -> {new_name}/')
    elif os.path.exists(dst):
        print(f'  Skip (already exists): {old_name} -> {new_name}')

# wp/ 配下のサブディレクトリも再帰的にリネーム
wp_dir = os.path.join(SKILLS_DIR, 'wp')
if os.path.exists(wp_dir):
    for old_name, new_name in rename_map.items():
        if old_name == 'tool':  # tool は wp/tool/ のまま
            continue
        src = os.path.join(wp_dir, old_name)
        dst = os.path.join(wp_dir, new_name)
        
        if os.path.exists(src) and not os.path.exists(dst):
            os.rename(src, dst)
            moved.append(f'wp/{old_name} -> wp/{new_name}')
            print(f'  wp/{old_name}/ -> wp/{new_name}/')

print(f'\nDone: {len(moved)} renames')
for m in moved:
    print(f'  {m}')