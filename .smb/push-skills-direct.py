import subprocess, os

skills_dir = '/home/bons/.skills/skill'

def run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)

for name in sorted(os.listdir(skills_dir)):
    if name.startswith('.'):
        continue
    
    skill_path = os.path.join(skills_dir, name)
    if not os.path.isdir(skill_path):
        continue
    
    print(f'Pushing: {name}...', end=' ')
    
    # skill ディレクトリ内で直接git init & push
    # .git がある場合は submodule なのでスキップ
    
    # まずリモート追加（もし既存のリモートがあれば削除）
    r = run(['git', 'remote', 'get-url', 'origin'], cwd=skill_path)
    
    # 既存のorigin URLを確認
    r = run(['git', 'config', 'remote.origin.url'], cwd=skill_path)
    if r.returncode == 0 and r.stdout.strip():
        current_url = r.stdout.strip()
        expected_url = f'https://github.com/bonsai/{name}.git'
        if current_url != expected_url:
            run(['git', 'remote', 'set-url', 'origin', expected_url], cwd=skill_path)
    else:
        run(['git', 'remote', 'add', 'origin', f'https://github.com/bonsai/{name}.git'], cwd=skill_path)
    
    # push --force
    r = run(['git', 'push', '-u', 'origin', 'main', '--force'], cwd=skill_path)
    if r.returncode == 0:
        print('OK')
    else:
        err = r.stderr.strip()[:120]
        if 'not found' in err.lower() or '404' in err:
            # リポジトリが存在しない → 作成してpush
            print('Creating...', end=' ')
            r2 = run(['gh', 'repo', 'create', f'bonsai/{name}', '--private'], capture_output=True, text=True)
            if r2.returncode == 0:
                r3 = run(['git', 'push', '-u', 'origin', 'main', '--force'], cwd=skill_path)
                if r3.returncode == 0:
                    print('Created+Pushed')
                else:
                    print(f'Push fail: {r3.stderr[:80]}')
            else:
                print(f'Create fail: {r2.stderr[:80]}')
        else:
            print(f'FAIL: {err}')