# libstdc++-v3 (upto 4.2.x)
===========================

## What is this?

A clone of libstdc++-v3 in genuine GCC tree.

## Why?

Apple GCC (maintained until 4.2.x) separated libstdc++-v3
from their GCC tarball, and provided as another tarball
customized for Xcode. It is hard to build without Xcode 3,
because autoconf-related files are removed.  Considering
that Apple GCC tarball kept autoconf-related files and
it is possible to rebuild original libstdc++-v3, if it
is placed in gcc tree.

Unfortunately, genuine GCC does not provide a git repository
only for libstdc++ which can be placed in gcc tree as a
submodule.

## How this repository was made?

This repository is made by `reduce-repo.sh`, doing like below:
```
$ git for-each-ref refs/remotes/origin/ --format='%(refname:short)' \
  | sed -n 's#origin/##;/gcc-[23]/p;/gcc-4.[0-2]/p;/egcs/p;/power/p' \
  | xargs -n 1 -I {} echo git branch {} origin/{}  | sh -x
$ git checkout -f releases/gcc-4.2
$ git branch -D master
$ git filter-repo \
  --path libstdc++-v3 \
  --path COPYING \
  --path COPYING.LIB \
  --path COPYING.RUNTIME \
  --path COPYING3 \
  --path COPYING3.RUNTIME \
  --path-rename libstdc++-v3/: --force
$ git branch | sed '/power/d;/gcc-[2-3]\./d;/gcc-4\.[0-2]/d' \
  | xargs -n 1 echo git branch -D  | sh -x
$ git tag | sed '/egcs/d;/gcc-[1-3]\./d;/gcc-4\.[0-2]/d;/libstdc++/d' \
  | xargs -n 1 echo git tag --delete | sh -x
$ git reflog expire --expire=now --all
$ git gc --prune=now --aggressive
```

## How can I relate a commit in original GCC git repository and this?

Here is commit-map.txt, which has an original commit hash
and a commit has in this repository like:

```
old                                      new
0000fd8cfd4ec4d053a003dc72d50dc8db553d09 bd73ec067dc5d48fa5d7751f2bd16890ca187ded
0002d5d2bc68f9381ec990ea94307bafa700b0ad 607f8f802016bd9b366eb5c828e72463e487c736
00035ba5e2104263fc55d2888d2852fc66902715 72e7ae4ed786eede646b16f9756f5ea2a5d75462
00082ff88cf4e25fc1041e9effd1c92fbaaa8d62 cf7bb9ac7d7618a0f74883175625d03431e20e91
...
```

This list was originally made by git filter-repo `.git/filter-repo/commit-map`,
but reduced by `reduce-commit-map.py` like this.

```
$ ./reduce-commit-map.py  < .git/filter-repo/commit-map > commit-map.txt
```
