import os

skills_dir = '/home/bons/.skills'

items = []
for item in sorted(os.listdir(skills_dir)):
    if item.startswith('.'):
        continue
    item_path = os.path.join(skills_dir, item)
    if not os.path.isdir(item_path):
        continue
    
    has_skill_md = os.path.exists(os.path.join(item_path, 'SKILL.md'))
    has_git = os.path.isdir(os.path.join(item_path, '.git'))
    subdirs = [d for d in os.listdir(item_path) if os.path.isdir(os.path.join(item_path, d))]
    
    items.append({
        'name': item,
        'has_skill_md': has_skill_md,
        'has_git': has_git,
        'type': 'dir' if not subdirs else 'dir+%d sub' % len(subdirs),
    })

print('Total: %d items' % len(items))
print('With SKILL.md: %d' % sum(1 for i in items if i['has_skill_md']))
print('Without SKILL.md: %d' % sum(1 for i in items if not i['has_skill_md']))
print('Directories with subs: %d' % sum(1 for i in items if i['type'].startswith('dir+')))

print()
for i in items:
    mark = 'SKILL' if i['has_skill_md'] else '    '
    print('  %s  %s  %s' % (mark, i['name'].ljust(30), i['type']))