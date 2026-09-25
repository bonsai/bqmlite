import os

wp_dir = '/home/bons/.skills/wp'

# Create subdirectories
for subdir in ['agt', 'txt', 'data', 'tool']:
    subdir_path = os.path.join(wp_dir, subdir)
    if not os.path.exists(subdir_path):
        os.makedirs(subdir_path)

# Classification
classifications = {
    'agt': [
        'bons.ai',
    ],
    'txt': [
        'rakugo-generator',
        'research-rakugo',
        'talkscripts',
    ],
    'data': [
        'ai-feelings',
        'kankyou-hub',
        'pain',
        'output',
        'talk-db',
    ],
    'tool': [
        'TORISETSU',
        'bqmlite-go',
        'gen-favicon',
        'genkou',
        'hakkutu',
        'leanvj',
        'progressive-life-temp',
        'chatgpt-ext',
        'wf-errors',
        'android-ftp-sync',
        'check-repos',
        'exercise-automation',
        'issue-md2wf',
        'lm-hex-eval',
        'outlook-draft',
        'pi-config',
        'portmanager',
        'python-status',
        'scoop-java-kotlin-clj',
        'serve-html',
        'svn-skill',
        'wsl-migrate',
        'wt-startdir',
    ],
}

moved = []
for subdir, items in classifications.items():
    for item in items:
        src = os.path.join(wp_dir, item)
        dst = os.path.join(wp_dir, subdir, item)
        if os.path.exists(src) and not os.path.exists(dst):
            os.rename(src, dst)
            moved.append((item, subdir))

print(f"Moved {len(moved)} items into wp/ subdirectories:")
for item, subdir in sorted(moved):
    print(f"  wp/{subdir}/{item}")