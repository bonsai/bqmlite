import subprocess, os, json

skills_dir = '/home/bons/.skills/skill'
main_dir = '/home/bons/.skills'

def run(args, cwd=main_dir):
    r = subprocess.run(['git'] + args, cwd=cwd, capture_output=True, text=True)
    return r.returncode, r.stdout.strip(), r.stderr.strip()

# 既存の GitHub repos をチェック
rc, stdout, _ = run(['remote', 'update', '--dry-run'])
rc, stdout, stderr = run(['for-each-ref', '--format=%(refname:short)', 'refs/remotes/origin/'])
tracked = set(l.strip().split('/')[0] for l in stdout.split('\n') if l.strip())

# .skills/skill/ の中身
skills = sorted(os.listdir(skills_dir))

# GitHub に個別 repo が既にあるかチェック
def check_github(name):
    r = subprocess.run(['gh', 'repo', 'view', f'bonsai/{name}', '--json', 'name'], 
                       capture_output=True, text=True)
    return r.returncode == 0

already_on_gh = set()
new_to_create = []
for s in skills:
    if s in tracked:
        already_on_gh.add(s)
    elif check_github(s):
        already_on_gh.add(s)
    else:
        new_to_create.append(s)

print(f'In .skills/skill/: {len(skills)}')
print(f'Already on GitHub: {len(already_on_gh)}')
print(f'Need new repo: {len(new_to_create)}')
print(f'\nMissing from GitHub:')
for n in new_to_create:
    print(f'  {n}')

# 既存 repo に subtree push
print(f'\nPushing to GitHub for {len(already_on_gh)} skills...')
ok = 0
fail = 0
for name in sorted(already_on_gh):
    skill_path = os.path.join(skills_dir, name)
    if not os.path.isdir(skill_path):
        continue
    
    rc, stdout, stderr = run(['subtree', 'push', '--prefix=skill/' + name, 'origin', 'main', '--force'])
    if rc == 0:
        ok += 1
    else:
        fail += 1
        if 'unipath-skills' in stderr:
            print(f'  Wrong target: {name}')

print(f'\nOK: {ok}, Fail: {fail}')