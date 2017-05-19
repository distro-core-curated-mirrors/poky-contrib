# meta-intel-docker
Yocto layer for adding docker to Intel platforms

If target will be behind a network proxy make sure http_proxy enviorment variable is set. Then build basic docker image as follows:

    mkdir docker-image
    cd docker-image
    repo init -u https://github.intel.com/hbruce/repo-manifests.git -m docker.xml
    repo sync
    export TEMPLATECONF=../meta-intel-docker/conf
    source poky/oe-init-build-env
    bitbake intel-docker-image



