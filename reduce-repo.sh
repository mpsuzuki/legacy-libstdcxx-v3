#!/bin/sh
git for-each-ref refs/remotes/origin/ --format='%(refname:short)' \
  | sed -n 's#origin/##;/gcc-[23]/p;/gcc-4.[0-2]/p;/egcs/p;/power/p' \
  | xargs -n 1 -I {} echo git branch {} origin/{}  | sh -x
git checkout -f releases/gcc-4.2
git branch -D master
git filter-repo \
  --path libstdc++-v3 \
  --path COPYING \
  --path COPYING.LIB \
  --path COPYING.RUNTIME \
  --path COPYING3 \
  --path COPYING3.RUNTIME \
  --path-rename libstdc++-v3/: --force
git branch | sed '/power/d;/gcc-[2-3]\./d;/gcc-4\.[0-2]/d' \
  | xargs -n 1 echo git branch -D  | sh -x
git tag | sed '/egcs/d;/gcc-[1-3]\./d;/gcc-4\.[0-2]/d;/libstdc++/d' \
  | xargs -n 1 echo git tag --delete | sh -x
git reflog expire --expire=now --all
git gc --prune=now --aggressive
