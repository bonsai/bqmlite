import os, shutil

skills_dir = '/home/bons/.skills'

# ジャンル別マッピング
mapping = {
    # uipath/ (31)
    'uipath-admin': 'uipath',
    'uipath-agents': 'uipath',
    'uipath-api-workflow': 'uipath',
    'uipath-automation-discovery': 'uipath',
    'uipath-automationhub': 'uipath',
    'uipath-coded-apps': 'uipath',
    'uipath-connector-builder': 'uipath',
    'uipath-feedback': 'uipath',
    'uipath-functions': 'uipath',
    'uipath-governance': 'uipath',
    'uipath-human-in-the-loop': 'uipath',
    'uipath-insights': 'uipath',
    'uipath-ixp': 'uipath',
    'uipath-maestro-bpmn': 'uipath',
    'uipath-maestro-case': 'uipath',
    'uipath-maestro-flow': 'uipath',
    'uipath-mcp-servers': 'uipath',
    'uipath-planner': 'uipath',
    'uipath-platform': 'uipath',
    'uipath-process-mining': 'uipath',
    'uipath-review': 'uipath',
    'uipath-rpa': 'uipath',
    'uipath-skill-catalog': 'uipath',
    'uipath-solution': 'uipath',
    'uipath-tasks': 'uipath',
    'uipath-test': 'uipath',
    'uipath-troubleshoot': 'uipath',
    
    # dev-tools/ (4)
    'skill-crawler': 'dev-tools',
    'skill-consolidator': 'dev-tools',
    'check-repos': 'dev-tools',
    'lm-hex-eval': 'dev-tools',
    
    # learning/ (2)
    'vocab-highlight': 'learning',
    'tips-word': 'learning',
}

# 除外 (そのまま残す)
keep = {'aw', 'deploy', 'workspace', 'skill', '.git', '.smb',
        'INDEX.md', 'README.md', 'skills.catalog.json'}

# 移動するものリスト
to_move = []
for item in os.listdir(skills_dir):
    if item in keep or item.startswith('.'):
        continue
    item_path = os.path.join(skills_dir, item)
    if os.path.isdir(item_path):
        target_genre = mapping.get(item)
        if target_genre:
            to_move.append((item, target_genre))
        else:
            print('NOT MAPPED: %s' % item)

# 移動先ディレクトリ作成
for _, genre in to_move:
    if not os.path.exists(os.path.join(skills_dir, genre)):
        os.makedirs(os.path.join(skills_dir, genre))

# 移動実行
moved = 0
for src_name, genre in to_move:
    src = os.path.join(skills_dir, src_name)
    dst = os.path.join(skills_dir, genre, src_name)
    
    # writing/writing 問題はスキップ
    if src == dst:
        continue
    
    shutil.move(src, dst)
    print('MOVED: %s -> %s/' % (src_name, genre))
    moved += 1

# skill/ 内の重複を削除
skill_dir = os.path.join(skills_dir, 'skill')
if os.path.exists(skill_dir):
    deleted = 0
    for item in os.listdir(skill_dir):
        item_path = os.path.join(skill_dir, item)
        if os.path.isdir(item_path) and item in mapping:
            shutil.rmtree(item_path)
            print('DELETED: skill/%s (duplicate)' % item)
            deleted += 1
    print('\nCLEANED: %d duplicates removed from skill/' % deleted)

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