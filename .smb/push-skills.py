import subprocess, os

skills_dir = '/home/bons/.skills/skill'
main_dir = '/home/bons/.skills'

for name in sorted(os.listdir(skills_dir)):
    skill_path = os.path.join(skills_dir, name)
    if not os.path.isdir(skill_path) or name.startswith('.'):
        continue
    
    print(f'Pushing: {name}...')
    
    result = subprocess.run(
        ['git', 'subtree', 'push', '--prefix=skill/' + name, 'origin', 'main'],
        cwd=main_dir, capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f'  OK: {name}')
    else:
        err = result.stderr.strip()[:200]
        if 'already exists' in err.lower():
            print(f'  Already exists: {name}')
        else:
            print(f'  ERROR: {err}')