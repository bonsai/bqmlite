import subprocess, os, shutil, tempfile

skills_dir = '/home/bons/.skills/skill'

for name in sorted(os.listdir(skills_dir)):
    if name.startswith('.'):
        continue
    
    skill_path = os.path.join(skills_dir, name)
    if not os.path.isdir(skill_path):
        continue
    
    print(f'Pushing: {name}...', end=' ')
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # git init -b main
        subprocess.run(['git', 'init', '-b', 'main'], cwd=tmpdir, capture_output=True)
        subprocess.run(['git', 'config', 'user.email', 'bons@opencode'], cwd=tmpdir, capture_output=True)
        subprocess.run(['git', 'config', 'user.name', 'bons'], cwd=tmpdir, capture_output=True)
        
        # skill contents を直接コピー
        for f in os.listdir(skill_path):
            if f == '.git':
                continue
            src = os.path.join(skill_path, f)
            dst = os.path.join(tmpdir, f)
            if os.path.isdir(src):
                shutil.copytree(src, dst, symlinks=True)
            else:
                shutil.copy2(src, dst)
        
        # add + commit
        subprocess.run(['git', 'add', '-A'], cwd=tmpdir, capture_output=True)
        r = subprocess.run(['git', 'commit', '-m', 'initial'], cwd=tmpdir, capture_output=True, text=True)
        if r.returncode != 0:
            print(f'no commit: {r.stderr[:60]}')
            continue
        
        # add remote & push
        subprocess.run(['git', 'remote', 'add', 'origin', f'https://github.com/bonsai/{name}.git'],
                       cwd=tmpdir, capture_output=True)
        
        r = subprocess.run(['git', 'push', '-u', 'origin', 'main', '--force'],
                          cwd=tmpdir, capture_output=True, text=True)
        if r.returncode == 0:
            print('OK')
        else:
            err = r.stderr.strip()[:150]
            if 'already exists' in err.lower():
                # 既存リポジトリがある → fetchしてforce push
                subprocess.run(['git', 'fetch', 'origin'], cwd=tmpdir, capture_output=True)
                r2 = subprocess.run(['git', 'push', '-u', 'origin', 'main', '--force'],
                                   cwd=tmpdir, capture_output=True, text=True)
                if r2.returncode == 0:
                    print('OK (forced)')
                else:
                    print(f'force fail: {r2.stderr[:80]}')
            else:
                print(f'FAIL: {err}')