#!/bin/sh -x

lxc-stop -k dpdk-demo
umount /mnt/hugepages
mkdir /mnt/hugepages
echo 2048 > /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages
mount -t hugetlbfs hugetlbfs /mnt/hugepages

dpdk-testpmd -l 0-1 -n 4 --socket-mem 1024 \
    --vdev='eth_vhost0,iface=/var/run/dpdk0' \
    --huge-dir=/mnt/hugepages --file-prefix=host --no-pci -- -i
