Installation
============

Requirements
------------

PatchTest (PT) requires `git-pw` (so far, used for posting results and polling
events), a tool which comes with [patchwork][pw] repository, so clone the repo, install requirements and create the symbolic
link as suggested, together with the PT scripts:

```
ln -s $PWD/pts ~/.local/bin/
ln -s $PWD/pte ~/.local/bin/
```

Usage
-----

Test a single series/revision by executing the main script:

```bash
pts  --pw-url X --test-dir X --pw-project X --repo-dir X --pw-no-post <SERIES> <REVISION>
```

the directory specifify on `--repo-dir` is created if not present. In case we want to post the results,
just remove the `--pw-no-post` argument. `test-dir`is the folder containing
all unit tests cases, where each module should start with `test_*`.

We can test new events using the 'Patch Test Event' script (`pte`):

```bash
git pw poll-events | pte
```

All results are stored under the folder defined on `--temp-base-dir`. In this
case, `pte` executes dummy tests located on the `tests` directory. To see
all options, type `pts --help`.

[pw]: https://github.com/dlespiau/patchwork "PW repo, maintained by D. Lespiau"
