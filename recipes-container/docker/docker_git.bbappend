FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}:"

# We're only supporting 64 bit Intel machines
COMPATIBLE_MACHINE = "intel-corei7-64"

do_install_append() {
    docker_config_dir=${sysconfdir}/systemd/system/docker.service.d
    install -d ${D}/$docker_config_dir
    echo '[Service]' > ${D}/$docker_config_dir/http-proxy.conf
    if [ -n "${http_proxy}" ]; then
        echo Environment=\"HTTP_PROXY=${http_proxy}\" >> ${D}/$docker_config_dir/http-proxy.conf
    fi
    if [ -n "${https_proxy}" ]; then
        echo Environment=\"HTTPS_PROXY=${https_proxy}\" >> ${D}/$docker_config_dir/http-proxy.conf
    fi
    if [ -n "${no_proxy}" ]; then
        echo Environment=\"NO_PROXY=${no_proxy}\" >> ${D}/$docker_config_dir/http-proxy.conf
    fi
}
