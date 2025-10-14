#!/bin/bash

FPGA="u280" #[u280|vck]
TARGET="hw" #[sw_emu|hw_emu|hw]
KERNEL_TYPE="single" # [single|multi]
KERNEL_NAME="krnl_bench"

python3 main.py $FPGA $TARGET $KERNEL_TYPE $KERNEL_NAME
