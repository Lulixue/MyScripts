#!/bin/sh 

PROJECT_NAME="my_project"
TAG="my_tag"

source build/envsetup.sh

#lunch $PROJECT_NAME-userdebug
lunch $PROJECT_NAME-eng

mv build.log build.log_old
if [ "$1" == "config" ]; then
	if [ "$2" == "cover" ]; then
		echo cover as default config
		cp kernel-3.18/arch/arm64/configs/$PROJECT_NAME_debug_defconfig out/target/product/$PROJECT_NAME/obj/KERNEL_OBJ/.config
	else
		mmm kernel-3.18:menuconfig-kernel
	fi
elif [ "$1" == "clean" ]; then
	make clobber
elif [ "$1" == "mmm" ]; then
	# make packages 
	# ./mkimage mmm packages/apps/Laucher
	# ./mkimage mmm frameworks/base/policy
	mmm $2
elif [ "$1" == "snod" ]; then
	if [ "$2" != "" ]; then
		mmm $2
	fi
	make snod
	cp out/target/product/$PROJECT_NAME/system.img .
elif [ "$1" == "fp" ]; then
	rm fingerprint.default.ko
	rm libftalg.ko
	rm fingerprintd
	
	echo --- make fingerprint.default.ko ---
	cd hardware/libhardware/modules/focal_fp_hal
	mm -B
	cd ~/heliox20droid

	echo --- make fingerprintd ---
	mmm ./system/core/fingerprintd
	
	cp out/target/product/$PROJECT_NAME/system/lib64/libftalg.so .
	cp out/target/product/$PROJECT_NAME/system/lib64/hw/fingerprint.default.so .
	cp out/target/product/$PROJECT_NAME/system/bin/fingerprintd .

		
elif [ "$1" == "lk" ]; then
	rm lk.bin
	make lk -j4  2>&1 | tee build.log
	if  [ $? -ne 0 ]; then
		exit 1
	fi

	cp out/target/product/$PROJECT_NAME/lk.bin .
	if [ "$2" == "boot" ]; then
		rm -rf out/target/product/$PROJECT_NAME/obj/KERNEL_OBJ/drivers/input/touchscreen/mediatek/
		rm boot.img
		#cp .config out/target/product/amt6797_64_m/obj/KERNEL_OBJ/
		make bootimage -j4 2>&1 | tee build.log
		if [ $? -ne 0 ]; then
			exit 1
		fi
		cp out/target/product/$PROJECT_NAME/boot.img .
	fi
elif [ "$1" == "all" ]; then
	rm boot.img
	rm lk.bin 
	rm -rf out/target/product/$PROJECT_NAME/obj/KERNEL_OBJ/drivers/input/touchscreen/mediatek/
	make -j4 2>&1 | tee build.log
#	make snod
	cp out/target/product/$PROJECT_NAME/boot.img .
	cp out/target/product/$PROJECT_NAME/lk.bin .
elif [ "$1" == "test" ]; then
	for no in $( seq $2 $3 )
	do
		echo ""
		echo "Test compile: ${no}"
		rm -rf out/target/product/$PROJECT_NAME/obj/KERNEL_OBJ/drivers/input/touchscreen/mediatek/
		make CONFIG_DIR_NO=${no} CONFIG_TEST_DRIVER=y bootimage -j4 2>&1 | grep $TAG
		# judge last operation result
		if [ $? -ne 0 ]; then
			break
		fi
	done
	
else
	rm -rf out/target/product/$PROJECT_NAME/obj/KERNEL_OBJ/drivers/input/fingerprint/
	rm -rf out/target/product/$PROJECT_NAME/obj/KERNEL_OBJ/drivers/input/touchscreen/mediatek/
	rm boot.img
	
	make bootimage -j4 2>&1 | tee build.log
	cp out/target/product/$PROJECT_NAME/boot.img .
fi
date
