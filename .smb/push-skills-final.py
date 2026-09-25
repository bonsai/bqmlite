import subprocess, os, json, tempfile, shutil

skills_dir = '/home/bons/.skills/skill'
main_dir = '/home/bons/.skills'

# GitHub に既にあるかチェック
def gh_has(name):
    r = subprocess.run(['gh', 'repo', 'view', f'bonsai/{name}', '--json', 'name'],
                       capture_output=True, text=True)
    return r.returncode == 0

# .skills/skill/ の中身
skills = sorted(os.listdir(skills_dir))

# 個別に push
for name in skills:
    if name.startswith('.'):
        continue
    
    skill_path = os.path.join(skills_dir, name)
    if not os.path.isdir(skill_path):
        continue
    
    print(f'Pushing: {name}...')
    
    # temp repo を作って push
    with tempfile.TemporaryDirectory() as tmpdir:
        # git init + add files
        subprocess.run(['git', 'init'], cwd=tmpdir, capture_output=True)
        subprocess.run(['git', 'config', 'user.email', 'bons@opencode'], cwd=tmpdir, capture_output=True)
        subprocess.run(['git', 'config', 'user.name', 'bons'], cwd=tmpdir, capture_output=True)
        
        # skill files を temp にコピー
        for f in os.listdir(skill_path):
            src = os.path.join(skill_path, f)
            dst = os.path.join(tmpdir, f)
            if os.path.isdir(src):
                shutil.copytree(src, dst, symlinks=True)
            else:
                shutil.copy2(src, dst)
        
        # commit
        subprocess.run(['git', 'add', '-A'], cwd=tmpdir, capture_output=True)
        subprocess.run(['git', 'commit', '-m', 'initial commit'], cwd=tmpdir, capture_output=True)
        
        # remote 追加
        subprocess.run(['git', 'remote', 'add', 'origin', f'https://github.com/bonsai/{name}.git'],
                       cwd=tmpdir, capture_output=True)
        
        # push
        r = subprocess.run(['git', 'push', '-u', 'origin', 'main', '--force'],
                          cwd=tmpdir, capture_output=True, text=True)
        if r.returncode == 0:
            print(f'  OK: https://github.com/bonsai/{name}')
        else:
            err = r.stderr.strip()[:200]
            if 'already exists' in err or 'Repository already exists' in err:
                # repo があるけど空 → force push
                r2 = subprocess.run(['git', 'push', '-u', 'origin', 'main', '--force'],
                                   cwd=tmpdir, capture_output=True, text=True)
                if r2.returncode == 0:
                    print(f'  OK (force): https://github.com/bonsai/{name}')
                else:
                    print(f'  FAIL: {r2.stderr.strip()[:100]}')
            elif 'Authentication' in err or '403' in err:
                print(f'  Auth/perm error: {err[:100]}')
            else:
                print(f'  FAIL: {err[:100]}')