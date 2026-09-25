import os, shutil

skills_dir = '/home/bons/.skills'

# 移動先マッピング
moves = {
    # uipath/ へ (残りの4)
    'uipath-admin': 'uipath',
    'uipath-governance': 'uipath',
    'uipath-platform': 'uipath',
    'uipath-insights': 'uipath',
    'uipath-solution': 'uipath',
    'uipath-coded-apps': 'uipath',
    
    # skill/ 内の残りスキル
    'ax': 'ax',
    'bqmlite': 'bqmlite',
    'char-distribution': 'learning',
    'footer': 'footer',
    'lx': 'lx',
    'mimic-me': 'mimic-me',
    'mx': 'mx',
    'pain-sense': 'pain-sense',
    'pi-config-memo': 'pi-config-memo',
    'recap': 'recap',
    'tsumete': 'tools',
    'win-tips': 'win-tips',
    'writing': 'writing',
    'wx': 'wx',
    'genkou': 'writing',
    'ds-insighter': 'ds',
    'ds-view': 'ds',
    'ext-install-skill': 'tools',
    'kenja': 'ds',
    'supervised-delegation': 'tools',
    'sync-db': 'tools',
    'check-repos': 'tools',
    'lm-hex-eval': 'tools',
}

# 移動先ディレクトリを作成
for genre in set(moves.values()):
    if not os.path.exists(os.path.join(skills_dir, genre)):
        os.makedirs(os.path.join(skills_dir, genre))
        print('CREATED: %s/' % genre)

# skill/ 内から移動
skill_dir = os.path.join(skills_dir, 'skill')
moved = 0
for item in os.listdir(skill_dir):
    item_path = os.path.join(skill_dir, item)
    if not os.path.isdir(item_path):
        continue
    
    target = moves.get(item)
    if target:
        dst = os.path.join(skills_dir, target, item)
        shutil.move(item_path, dst)
        print('MOVED: skill/%s -> %s/' % (item, target))
        moved += 1

# ループ直下から移動（残ってるもの）
for item in os.listdir(skills_dir):
    if item.startswith('.'):
        continue
    item_path = os.path.join(skills_dir, item)
    if not os.path.isdir(item_path) or item in moves:
        continue
    
    target = moves.get(item)
    if target:
        dst = os.path.join(skills_dir, target, item)
        shutil.move(item_path, dst)
        print('MOVED: %s -> %s/' % (item, target))
        moved += 1

# 結果表示
print('\n=== RESULT ===')
for item in sorted(os.listdir(skills_dir)):
    if item.startswith('.'):
        continue
    item_path = os.path.join(skills_dir, item)
    if os.path.isdir(item_path):
        count = len(os.listdir(item_path))
        print('  %s/ (%d items)' % (item, count))
    else:
        print('  %s' % item)

# skill/ 残りを表示
remaining = [i for i in os.listdir(skill_dir) if os.path.isdir(os.path.join(skill_dir, i))]
if remaining:
    print('\n=== Remaining in skill/ ===')
    for r in remaining:
        print('  %s' % r)