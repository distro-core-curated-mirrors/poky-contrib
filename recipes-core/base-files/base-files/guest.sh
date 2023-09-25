#!/bin/sh -x

dpdk-testpmd -l 2-3 -n 4 -m 2048 --no-pci \
    --vdev=virtio_user0,path=/mnt/dpdk0 \
    --huge-dir=/var/dpdk/hugepages \
    --file-prefix=container -- -i

