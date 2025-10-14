#!/bin/bash

#TARGET=sw_emu
TARGET=hw

FPGA=u280
#FPGA=vck5000

FP_TYPE=fixed_point

KERNEL_TYPE=single
#KERNEL_TYPE=multi

IF_COMPILE=1
IF_LINK=1

configs=(
    add_16_6_dsp
    add_16_6_fabric
    add_16_8_dsp
    add_16_8_fabric
    add_32_12_dsp
    add_32_12_fabric
    add_32_16_dsp
    add_32_16_fabric
    add_64_12_dsp
    add_64_12_fabric
    add_64_24_dsp
    add_64_24_fabric
    add_8_3_dsp
    add_8_3_fabric
    add_8_4_dsp
    add_8_4_fabric
    mul_16_6_dsp
    mul_16_6_fabric
    mul_16_8_dsp
    mul_16_8_fabric
    mul_32_12_dsp
    mul_32_12_fabric
    mul_32_16_dsp
    mul_32_16_fabric
    mul_64_12_dsp
    mul_64_12_fabric
    mul_64_24_dsp
    mul_64_24_fabric
    mul_8_3_dsp
    mul_8_3_fabric
    mul_8_4_dsp
    mul_8_4_fabric
    sub_16_6_dsp
    sub_16_6_fabric
    sub_16_8_dsp
    sub_16_8_fabric
    sub_32_12_dsp
    sub_32_12_fabric
    sub_32_16_dsp
    sub_32_16_fabric
    sub_64_12_dsp
    sub_64_12_fabric
    sub_64_24_dsp
    sub_64_24_fabric
    sub_8_3_dsp
    sub_8_3_fabric
    sub_8_4_dsp
    sub_8_4_fabric
)

cd ../../ ;
. ./build.sh
