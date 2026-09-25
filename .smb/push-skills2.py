import subprocess, os

skills_dir = '/home/bons/.skills/skill'
main_dir = '/home/bons/.skills'

def run_git(args, cwd):
    result = subprocess.run(['git'] + args, cwd=cwd, capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()

for name in sorted(os.listdir(skills_dir)):
    skill_path = os.path.join(skills_dir, name)
    if not os.path.isdir(skill_path) or name.startswith('.'):
        continue
    
    print(f'Updating: {name}...')
    
    # git subtree push with force
    rc, stdout, stderr = run_git(
        ['subtree', 'push', '--prefix=skill/' + name, 'origin', 'main', '--force'],
        main_dir
    )
    if rc == 0:
        print(f'  OK: {name}')
    else:
        # Check if the remote URL is wrong
        if 'unipath-skills' in stderr:
            print(f'  Wrong repo (unipath-skills): {name}')
        else:
            print(f'  ERROR: {stderr[:150]}')