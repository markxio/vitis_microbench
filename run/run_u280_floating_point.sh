#!/bin/bash

TARGET=hw
number_of_runs=100
KERNEL_TYPE=single

reps=10000000 # number of elements
FPGA=u280
number_cus=1
FP_TYPE=floating_point

# on u280, no primitivedsp

bitstreams=(
    "dadd_fabric.${TARGET}.xclbin"
    "dadd_fulldsp.${TARGET}.xclbin"
    "ddiv_fabric.${TARGET}.xclbin"
    "dexp_fabric.${TARGET}.xclbin"
    "dexp_fulldsp.${TARGET}.xclbin"
    "dexp_meddsp.${TARGET}.xclbin"
    "dlog_fabric.${TARGET}.xclbin"
    "dlog_fulldsp.${TARGET}.xclbin"
    "dlog_meddsp.${TARGET}.xclbin"
    "dmul_fabric.${TARGET}.xclbin"
    "dmul_fulldsp.${TARGET}.xclbin"
    "dmul_maxdsp.${TARGET}.xclbin"
    "dmul_meddsp.${TARGET}.xclbin"
    "drecip_fulldsp.${TARGET}.xclbin"
    "drsqrt_fulldsp.${TARGET}.xclbin"
    "dsqrt_fabric.${TARGET}.xclbin"
    "dsub_fabric.${TARGET}.xclbin"
    "dsub_fulldsp.${TARGET}.xclbin"
    "fadd_fabric.${TARGET}.xclbin"
    "fadd_fulldsp.${TARGET}.xclbin"
    "fdiv_fabric.${TARGET}.xclbin"
    "fexp_fabric.${TARGET}.xclbin"
    "fexp_fulldsp.${TARGET}.xclbin"
    "fexp_meddsp.${TARGET}.xclbin"
    "flog_fabric.${TARGET}.xclbin"
    "flog_fulldsp.${TARGET}.xclbin"
    "flog_meddsp.${TARGET}.xclbin"
    "fmul_fabric.${TARGET}.xclbin"
    "fmul_fulldsp.${TARGET}.xclbin"
    "fmul_maxdsp.${TARGET}.xclbin"
    "fmul_meddsp.${TARGET}.xclbin"
    "frecip_fabric.${TARGET}.xclbin"
    "frecip_fulldsp.${TARGET}.xclbin"
    "frsqrt_fabric.${TARGET}.xclbin"
    "frsqrt_fulldsp.${TARGET}.xclbin"
    "fsqrt_fabric.${TARGET}.xclbin"
    "fsub_fabric.${TARGET}.xclbin"
    "fsub_fulldsp.${TARGET}.xclbin"
    "hadd_fabric.${TARGET}.xclbin"
    "hadd_fulldsp.${TARGET}.xclbin"
    "hadd_meddsp.${TARGET}.xclbin"
    "hdiv_fabric.${TARGET}.xclbin"
    "hmul_fabric.${TARGET}.xclbin"
    "hmul_fulldsp.${TARGET}.xclbin"
    "hmul_maxdsp.${TARGET}.xclbin"
    "hsqrt_fabric.${TARGET}.xclbin"
    "hsub_fabric.${TARGET}.xclbin"
    "hsub_fulldsp.${TARGET}.xclbin"
    "hsub_meddsp.${TARGET}.xclbin"
)

cd ../
. ./run.sh
