import subprocess, os

skills_dir = '/home/bons/.skills/skill'
main_dir = '/home/bons/.skills'

def run(args, cwd=main_dir):
    r = subprocess.run(['git'] + args, cwd=cwd, capture_output=True, text=True)
    return r.returncode, r.stdout.strip(), r.stderr.strip()

# git remote update で最新の remote tracking を取得
run(['remote', 'update'])

# skills と GitHub repos を比較
existing, missing = [], []
for name in sorted(os.listdir(skills_dir)):
    skill_path = os.path.join(skills_dir, name)
    if not os.path.isdir(skill_path) or name.startswith('.'):
        continue
    
    # remote tracking をチェック
    rc, stdout, stderr = run(['show-ref', f'refs/remotes/origin/{name}'])
    if rc == 0:
        existing.append(name)
    else:
        missing.append(name)

print(f'Existing repos: {len(existing)}')
for n in existing[:5]:
    print(f'  {n}')
print(f'... (+{len(existing)-5})')

print(f'\nNew repos to create: {len(missing)}')
for n in missing[:5]:
    print(f'  {n}')
print(f'... (+{len(missing)-5})')

# 既存の repo に push する
print('\n=== Pushing to existing repos ===')
for name in existing:
    print(f'{name}...', end=' ')
    rc, stdout, stderr = run(['subtree', 'push', '--prefix=skill/' + name, 'origin', 'main', '--force'])
    if rc == 0:
        print('OK')
    else:
        print(f'ERROR: {stderr[:100]}')