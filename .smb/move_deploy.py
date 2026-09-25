import os

SKILLS_DIR = '/home/bons/.skills'

# Create dp/ directory
dp_dir = os.path.join(SKILLS_DIR, 'dp')
if not os.path.exists(dp_dir):
    os.makedirs(dp_dir)

# Deploy indicators: has html + .github/ (CI/CD) or public/ or just html app
deploy_items = [
    'emoji-shiritori',    # html, package.json, dist/, .github/, public/
    'owarai-live',        # html, package.json, dist/, .github/
    'progressive-life-v2',# package.json, .github/, public/
    'showa-covers',       # html, public/
    'yose-db',            # html, .github/, public/
    'idol-playlist',      # html, .github/
    'idol-lab',           # html
    'makaizou-init',      # html
]

moved = 0
for item in deploy_items:
    old_path = os.path.join(SKILLS_DIR, 'wp', item)
    new_path = os.path.join(dp_dir, item)
    if os.path.exists(old_path) and not os.path.exists(new_path):
        os.rename(old_path, new_path)
        moved += 1
        print(f'  wp/{item} -> dp/{item}')

print(f'\nDone: {moved} items moved to dp/')