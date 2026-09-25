import subprocess, os, shutil, tempfile

skills_dir = '/home/bons/.skills/skill'
main_dir = '/home/bons/.skills'

for name in sorted(os.listdir(skills_dir)):
    if name.startswith('.'):
        continue
    
    skill_path = os.path.join(skills_dir, name)
    if not os.path.isdir(skill_path):
        continue
    
    print(f'Pushing: {name}...', end=' ')
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # git init
        subprocess.run(['git', 'init', '-b', 'main'], cwd=tmpdir, capture_output=True)
        subprocess.run(['git', 'config', 'user.email', 'bons@opencode'], cwd=tmpdir, capture_output=True)
        subprocess.run(['git', 'config', 'user.name', 'bons'], cwd=tmpdir, capture_output=True)
        
        # skill files をコピー（.git は除く）
        for f in os.listdir(skill_path):
            if f == '.git':
                continue
            src = os.path.join(skill_path, f)
            dst = os.path.join(tmpdir, f)
            if os.path.isdir(src):
                shutil.copytree(src, dst, symlinks=True)
            else:
                shutil.copy2(src, dst)
        
        # commit
        subprocess.run(['git', 'add', '-A'], cwd=tmpdir, capture_output=True)
        r = subprocess.run(['git', 'commit', '-m', 'initial'], cwd=tmpdir, capture_output=True)
        if r.returncode != 0:
            print(f'commit fail: {r.stderr.decode()[:80]}')
            continue
        
        # remote 追加 & push
        subprocess.run(['git', 'remote', 'add', 'origin', f'https://github.com/bonsai/{name}.git'],
                       cwd=tmpdir, capture_output=True)
        
        r = subprocess.run(['git', 'push', '-u', 'origin', 'main', '--force'],
                          cwd=tmpdir, capture_output=True, text=True)
        if r.returncode == 0:
            print('OK')
        else:
            err = r.stderr.strip()[:150]
            if 'already exists' in err.lower():
                r2 = subprocess.run(['git', 'fetch', 'origin'], cwd=tmpdir, capture_output=True)
                subprocess.run(['git', 'checkout', 'main'], cwd=tmpdir, capture_output=True)
                r3 = subprocess.run(['git', 'reset', '--hard', 'origin/main'], cwd=tmpdir, capture_output=True)
                r4 = subprocess.run(['git', 'pull', 'origin', 'main', '--allow-unrelated-histories', '--strategy-option=theirs'],
                                   cwd=tmpdir, capture_output=True, text=True)
                if r4.returncode == 0:
                    # merge した後に skill contents を置き換え
                    subprocess.run(['git', 'rm', '-rf', '.'], cwd=tmpdir, capture_output=True)
                    for f in os.listdir(skill_path):
                        if f == '.git':
                            continue
                        src = os.path.join(skill_path, f)
                        dst = os.path.join(tmpdir, f)
                        if os.path.isdir(src):
                            shutil.copytree(src, dst, symlinks=True)
                        else:
                            shutil.copy2(src, dst)
                    subprocess.run(['git', 'add', '-A'], cwd=tmpdir, capture_output=True)
                    subprocess.run(['git', 'commit', '-m', 'update from .skills'], cwd=tmpdir, capture_output=True)
                    r5 = subprocess.run(['git', 'push', 'origin', 'main', '--force'],
                                       cwd=tmpdir, capture_output=True, text=True)
                    if r5.returncode == 0:
                        print('OK (merged)')
                    else:
                        print(f'push fail: {r5.stderr[:80]}')
                else:
                    print(f'pull fail: {r4.stderr[:80]}')
            else:
                print(f'FAIL: {err}')