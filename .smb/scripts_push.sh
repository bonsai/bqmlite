#!/bin/bash
cd /home/bons/.skills || exit 1

# 1) cleanup temp scripts
rm -f scripts_survey.sh scripts_check_links.sh scripts_diffs.sh scripts_inspect.sh scripts_inspect2.sh scripts_stage.sh

# 2) top repo: commit dead-link removal only (nothing untracked added)
git add -u
echo "########## TOP .skills ##########"
git diff --cached --stat | tail -5
git commit -m "chore: remove dead empty skill placeholders" 2>&1 | tail -2
git push -u origin main 2>&1 | tail -3

# 3) per-repo commit + push
commit_push() {
  local dir=$1 msg=$2
  echo "########## $dir ##########"
  ( cd "$dir" || exit 1
    if git diff --cached --check | grep -q .; then echo "  !! whitespace errors"; fi
    n=$(git diff --cached | grep -c '^new file mode 160000')
    if [ "$n" != "0" ]; then echo "  !! gitlink detected ($n) — abort add"; exit 1; fi
    git commit -m "$msg" 2>&1 | tail -2
    git push origin HEAD 2>&1 | tail -3
  )
}

commit_push chatgpt-ext "rm: pain.md (migrated to bonsai/pain)"
commit_push kankyou-hub "chore: sync dashboard.db + add sync_data_ingest and bin/ds; ignore .env"
commit_push showa-covers "chore: ignore mp3 and Zone.Identifier files"
commit_push talkscripts "chore: restructure notes to STAGE/STOCK/skip + add repo2rakugo skill"
commit_push wf-errors "chore: add go deps and decision log; ignore build artifacts"
commit_push yose-db "chore: ignore gh aw runtime logs"