#!/usr/bin/env python3
"""
.skills/ 内のフォルダ名にプレフィックスを付けて、状態が一目でわかるようにする。

分類:
  [sk/ ] - SKILL.mdがある = すでにスキル
  [wp/ ] - SKILL.mdがない = これからなるもの
  [x/ ]  - システムファイル = なれないもの
"""
import os
import sys

SKILLS_DIR = '/home/bons/.skills'

SYSTEM_PATTERNS = [
    'bx', 'ex', 'ix', 'ox', 'px', 'sx', 'tx', 'ux',
    'torissetsu', 'shitagaki', 'xx',
]

# プレフィックス定義
PREFIX_SKILL = 'sk/'    # スキル化済み (SKILL.mdあり)
PREFIX_WAIT = 'wp/'     # これからなる (SKILL.mdなし)
PREFIX_NO = 'x/'        # スキル化不可 (システム/データ)

def classify(dir_name):
    """フォルダ名を分類してプレフィックスを返す"""
    d_lower = dir_name.lower()
    
    # SKILL.mdがある = すでにスキル（最優先）
    skill_md = os.path.join(SKILLS_DIR, dir_name, 'SKILL.md')
    if os.path.exists(skill_md):
        return PREFIX_SKILL, 'スキル化済み'
    
    # システムファイル
    if d_lower in SYSTEM_PATTERNS or d_lower.startswith('x'):
        return PREFIX_NO, 'スキル化不可'
    
    # SKILL.mdがない = これからなる
    return PREFIX_WAIT, 'スキル化待ち'

def list_dirs():
    """全ディレクトリを分類して表示"""
    categorized = {PREFIX_SKILL: [], PREFIX_WAIT: [], PREFIX_NO: []}
    
    for item in sorted(os.listdir(SKILLS_DIR)):
        item_path = os.path.join(SKILLS_DIR, item)
        if not os.path.isdir(item_path):
            continue
        if item.startswith('.'):
            continue
        
        prefix, desc = classify(item)
        categorized[prefix].append((item, desc))
    
    return categorized

if __name__ == '__main__':
    categorized = list_dirs()
    
    print(f'=== .skills/ 分類結果 ===')
    print()
    print(f'[sk/ ] スキル化済み (SKILL.mdあり) {len(categorized[PREFIX_SKILL])}個')
    print(f'[wp/ ] これからなる (SKILL.mdなし) {len(categorized[PREFIX_WAIT])}個')
    print(f'[x/ ]  なれない (システム/データ)   {len(categorized[PREFIX_NO])}個')
    print()
    
    for label, items in [
        ('[sk/ ] スキル化済み', categorized[PREFIX_SKILL]),
        ('[wp/ ] これからなる', categorized[PREFIX_WAIT]),
        ('[x/ ]  なれない', categorized[PREFIX_NO]),
    ]:
        if items:
            print(f'{label} ({len(items)}個)')
            for item, desc in items:
                new_name = label.split(' ', 1)[0].strip('[]') + item
                print(f'    {new_name}  ← {item}')
            print()
    
    # リネーム確認
    print('--- リネーム実行には --exec を付けてください ---')
    if '--exec' in sys.argv:
        rename_map = []
        for items in categorized.values():
            for item, desc in items:
                prefix = classify(item)[0]
                new_name = prefix + item
                if new_name != item:
                    rename_map.append((item, new_name))
        
        print(f'\n{len(rename_map)}個のリネームを行います (y/N): ', end='')
        if input().strip().lower() in ['y', 'yes', 'はい']:
            for old, new in rename_map:
                old_path = os.path.join(SKILLS_DIR, old)
                new_path = os.path.join(SKILLS_DIR, new)
                if os.path.exists(new_path):
                    print(f'Skip (exists): {old}')
                    continue
                os.rename(old_path, new_path)
                print(f'  {old} -> {new}')
            print('\n完了!')
        else:
            print('キャンセルされました。')