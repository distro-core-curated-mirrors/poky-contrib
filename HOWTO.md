# meta-zephyr-sdk

## How to build from scratch
```
mkdir zephyr-sandbox
cd zephyr-sandbox
wget "https://gerrit.zephyrproject.org/r/gitweb?p=meta-zephyr-sdk.git;a=blob_plain;f=scripts/meta-zephyr-sdk-clone-0.7.5.sh;hb=HEAD" -O meta-zephyr-sdk-clone-0.7.5.sh
./meta-zephyr-sdk-clone-0.7.5.sh
./poky/meta-zephyr-sdk/scripts/meta-zephyr-sdk-build.sh
```

In this branch, there is an optional ```SSTATE_MIRROR_URI``` env var that can be passed to the command line:
```
SSTATE_MIRROR_URI=http://my.example.com/ ./poky/meta-zephyr-sdk/scripts/meta-zephyr-sdk-build.sh
```

The ```SSTATE_MIRROR_URI``` env var is just the URI for an sstate mirror (the rest of the ```SSTATE_MIRRORS``` bitbake variable syntax is done by the script). This will set--not append to--the ```SSTATE_MIRRORS``` variable, since the existing build script does not provide the functionality to append, only set. This goal of this branch is to be as minimally invasive as possible.

### Fedora
To get to build on Fedora (23) needed to install ```perl-bignum```, ```readline-devel```, ```makeself```, and ```p7zip``` and create a symbolic link ```ln -s /usr/bin/7za /usr/bin/7z```
