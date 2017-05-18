# meta-intel-aero-docker
Yocto layer for adding docker to Intel Aero platform

For details on getting setup to build see the [Intel Aero wiki](https://github.com/intel-aero/meta-intel-aero/wiki).

Build basic docker image as follows

    mkdir intel_aero
    cd intel_aero
    repo init -u https://github.com/intel-aero/intel-aero-manifest.git -b pyro -m docker.xml
    repo sync -j4
    export TEMPLATECONF=../meta-intel-aero-docker/conf
    source poky/oe-init-build-env
    bitbake aero-docker-image


License
=======
http://www.gnu.org/licenses/gpl-2.0.html

