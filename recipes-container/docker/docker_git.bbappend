FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}:"

SRC_URI += "file://http-proxy.conf"

do_install_append() {
    echo http_proxy = ${http_proxy}
    if [ -n "${http_proxy}" ]; then
        docker_config_dir=${sysconfdir}/systemd/system/docker.service.d
        install -d ${D}/$docker_config_dir
        sed -e s_{URL}_${http_proxy}_ ${WORKDIR}/http-proxy.conf > ${D}/$docker_config_dir/http-proxy.conf
    fi
}
