ifndef CPU_NUM
CPU_NUM = $(shell cat /proc/cpuinfo | grep processor | wc | cut -f7 -d' ')
endif

.PHONY: common network script application plum mtplum

all: common network script application plum mtplum

common: $(libs)
	cd $@; make -j$(CPU_NUM)

network: $(libs)
	cd $@; make -j$(CPU_NUM)

script: $(libs)
	cd $@; make -j$(CPU_NUM)

application: $(libs)
	cd $@; make -j$(CPU_NUM)

plum: $(libs)
	cd $@; make -j$(CPU_NUM)

mtplum: $(libs)
	cd $@; make -j$(CPU_NUM)

.PHONY: clean
clean:
	cd common; make clean
	cd network; make clean
	cd script; make clean
	cd application; make clean
	cd plum; make clean
	cd mtplum; make clean


