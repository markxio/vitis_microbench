#!/bin/bash

TARGET=hw
number_of_runs=100
KERNEL_TYPE=single

reps=10000000 # number of elements
FPGA=vck
number_cus=1
FP_TYPE=fixed_point

bitstreams=(
    "add_16_6_dsp.${TARGET}.xclbin"
    "add_16_6_fabric.${TARGET}.xclbin"
    "add_16_8_dsp.${TARGET}.xclbin"
    "add_16_8_fabric.${TARGET}.xclbin"
    "add_32_12_dsp.${TARGET}.xclbin"
    "add_32_12_fabric.${TARGET}.xclbin"
    "add_32_16_dsp.${TARGET}.xclbin"
    "add_32_16_fabric.${TARGET}.xclbin"
    "add_64_12_dsp.${TARGET}.xclbin"
    "add_64_12_fabric.${TARGET}.xclbin"
    "add_64_24_dsp.${TARGET}.xclbin"
    "add_64_24_fabric.${TARGET}.xclbin"
    "add_8_3_dsp.${TARGET}.xclbin"
    "add_8_3_fabric.${TARGET}.xclbin"
    "add_8_4_dsp.${TARGET}.xclbin"
    "add_8_4_fabric.${TARGET}.xclbin"
    "mul_16_6_dsp.${TARGET}.xclbin"
    "mul_16_6_fabric.${TARGET}.xclbin"
    "mul_16_8_dsp.${TARGET}.xclbin"
    "mul_16_8_fabric.${TARGET}.xclbin"
    "mul_32_12_dsp.${TARGET}.xclbin"
    "mul_32_12_fabric.${TARGET}.xclbin"
    "mul_32_16_dsp.${TARGET}.xclbin"
    "mul_32_16_fabric.${TARGET}.xclbin"
    "mul_64_12_dsp.${TARGET}.xclbin"
    "mul_64_12_fabric.${TARGET}.xclbin"
    "mul_64_24_dsp.${TARGET}.xclbin"
    "mul_64_24_fabric.${TARGET}.xclbin"
    "mul_8_3_dsp.${TARGET}.xclbin"
    "mul_8_3_fabric.${TARGET}.xclbin"
    "mul_8_4_dsp.${TARGET}.xclbin"
    "mul_8_4_fabric.${TARGET}.xclbin"
    "sub_16_6_dsp.${TARGET}.xclbin"
    "sub_16_6_fabric.${TARGET}.xclbin"
    "sub_16_8_dsp.${TARGET}.xclbin"
    "sub_16_8_fabric.${TARGET}.xclbin"
    "sub_32_12_dsp.${TARGET}.xclbin"
    "sub_32_12_fabric.${TARGET}.xclbin"
    "sub_32_16_dsp.${TARGET}.xclbin"
    "sub_32_16_fabric.${TARGET}.xclbin"
    "sub_64_12_dsp.${TARGET}.xclbin"
    "sub_64_12_fabric.${TARGET}.xclbin"
    "sub_64_24_dsp.${TARGET}.xclbin"
    "sub_64_24_fabric.${TARGET}.xclbin"
    "sub_8_3_dsp.${TARGET}.xclbin"
    "sub_8_3_fabric.${TARGET}.xclbin"
    "sub_8_4_dsp.${TARGET}.xclbin"
    "sub_8_4_fabric.${TARGET}.xclbin"
)

cd ../
. ./run.sh
