SRC := $(shell pwd)

obj-m := slave.o
# $src is a Kbuild variable. Using $SRC doesn't work.
ccflags-y := -I$(src)/recipe-sysroot/usr/include/kernel-module-master/

all:
	$(MAKE) -C $(KERNEL_SRC) M=$(SRC)

modules_install:
	$(MAKE) -C $(KERNEL_SRC) M=$(SRC) modules_install

clean:
	rm -f *.o *~ core .depend .*.cmd *.ko *.mod.c
	rm -f Module.markers Module.symvers modules.order
	rm -rf .tmp_versions Modules.symvers
