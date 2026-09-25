import subprocess, os

skills_dir = '/home/bons/.skills/skill'
missing = [
    'footer', 'pain-sense',
    'uipath-admin', 'uipath-agents', 'uipath-api-workflow',
    'uipath-automation-discovery', 'uipath-automationhub',
    'uipath-coded-apps', 'uipath-connector-builder',
    'uipath-feedback', 'uipath-functions',
    'uipath-governance', 'uipath-human-in-the-loop',
    'uipath-insights', 'uipath-ixp',
    'uipath-maestro-bpmn', 'uipath-maestro-case',
    'uipath-maestro-flow', 'uipath-mcp-servers',
    'uipath-planner', 'uipath-platform',
    'uipath-process-mining', 'uipath-review',
    'uipath-rpa', 'uipath-skill-catalog',
    'uipath-solution', 'uipath-tasks',
    'uipath-test', 'uipath-troubleshoot',
]

# 既存リポジトリを作成して push
for name in missing:
    print(f'Creating: {name}...')
    
    # GitHub リポジトリを作成（private）
    result = subprocess.run(
        ['gh', 'repo', 'create', f'bonsai/{name}', '--private', '--description', f'opencode skill: {name}'],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        err = result.stderr.strip()
        if 'already exists' in err or 'Already exists' in err:
            print(f'  Already exists: {name}')
        else:
            print(f'  ERROR: {err[:200]}')
        continue
    
    # git subtree push で個別ディレクトリを push
    result = subprocess.run(
        ['git', 'subtree', 'push', '--prefix=skill/' + name, 'origin', 'main'],
        cwd='/home/bons/.skills',
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f'  Pushed: {name}')
    else:
        print(f'  Push ERROR: {result.stderr.strip()[:200]}')