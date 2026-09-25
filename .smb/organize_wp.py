import os

wp_dir = '/home/bons/.skills/wp'

# Categories
CAT_AGENTIC = 'agt/'    # エージェント
CAT_TEXT = 'txt/'       # テキスト生成
CAT_TOOL = 'tool/'      # ツール
CAT_DATA = 'data/'      # データ・研究

# Classification rules
classifications = {
    # エージェント
    'bons.ai': CAT_AGENTIC,
    
    # テキスト生成
    'rakugo-generator': CAT_TEXT,
    'research-rakugo': CAT_TEXT,
    'talk-db': CAT_DATA,  # 索引DBだがテキスト生成の元ネタ
    'talkscripts': CAT_TEXT,
    'yimoto-theater': CAT_TEXT,
    
    # データ・研究
    'ai-feelings': CAT_DATA,
    'kankyou-hub': CAT_DATA,
    'pain': CAT_DATA,
    'output': CAT_DATA,
    'yose-db': CAT_DATA,  # wpからdpに移動済みだがデータ系
    
    # ツール（デフォルト）
    'bqmlite-go': CAT_TOOL,
    'gen-favicon': CAT_TOOL,
    'hakkutu': CAT_TOOL,
    'leanvj': CAT_TOOL,
    'progressive-life-temp': CAT_TOOL,
    'chatgpt-ext': CAT_TOOL,
    'wf-errors': CAT_TOOL,
    'TORISETSU': CAT_TOOL,
    'genkou': CAT_TOOL,
    
    # 空or不明
    'android-ftp-sync': CAT_TOOL,
    'check-repos': CAT_TOOL,
    'exercise-automation': CAT_TOOL,
    'issue-md2wf': CAT_TOOL,
    'lm-hex-eval': CAT_TOOL,
    'outlook-draft': CAT_TOOL,
    'pi-config': CAT_TOOL,
    'portmanager': CAT_TOOL,
    'python-status': CAT_TOOL,
    'scoop-java-kotlin-clj': CAT_TOOL,
    'serve-html': CAT_TOOL,
    'svn-skill': CAT_TOOL,
    'wsl-migrate': CAT_TOOL,
    'wt-startdir': CAT_TOOL,
    'progressive-life-v2': CAT_TOOL,  # dpから元に戻す
}

# Create category dirs
for cat in [CAT_AGENTIC, CAT_TEXT, CAT_TOOL, CAT_DATA]:
    cat_path = os.path.join(wp_dir, '..', cat)
    if not os.path.exists(cat_path):
        os.makedirs(cat_path)

# Move items
moved = []
for item, cat in classifications.items():
    old_path = os.path.join(wp_dir, item)
    new_path = os.path.join(wp_dir, '..', cat, item)
    
    # Check if item exists in wp
    if os.path.exists(old_path):
        if not os.path.exists(new_path):
            os.rename(old_path, new_path)
            moved.append((item, cat))
    # Check if item is in root (e.g. progressive-life-v2 was in dp)
    elif os.path.exists(os.path.join('/home/bons/.skills', item)):
        old_root = os.path.join('/home/bons/.skills', item)
        new_path = os.path.join(wp_dir, '..', cat, item)
        if not os.path.exists(new_path):
            os.rename(old_root, new_path)
            moved.append((item, cat))

print(f"Moved {len(moved)} items:")
for item, cat in sorted(moved):
    print(f"  {item} -> {cat}")