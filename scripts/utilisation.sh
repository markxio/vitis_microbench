#!/bin/bash

TARGET=hw

#FPGA=u280
#FPGA=vck5000

configs=(
    fadd_fabric      
    fadd_fulldsp     
    fadd_primitivedsp
    fsub_fabric      
    fsub_fulldsp     
    fsub_primitivedsp
    fdiv_fabric      
    fexp_fabric      
    fexp_meddsp      
    fexp_fulldsp     
    flog_fabric      
    flog_meddsp      
    flog_fulldsp     
    fmul_fabric      
    fmul_meddsp      
    fmul_fulldsp     
    fmul_maxdsp      
    fmul_primitivedsp
    fsqrt_fabric     
    frsqrt_fabric    
    frsqrt_fulldsp   
    frecip_fabric    
    frecip_fulldsp   
    dadd_fabric      
    dadd_fulldsp     
    dsub_fabric      
    dsub_fulldsp     
    ddiv_fabric      
    dexp_fabric      
    dexp_meddsp      
    dexp_fulldsp     
    dlog_fabric      
    dlog_meddsp      
    dlog_fulldsp     
    dmul_fabric      
    dmul_meddsp      
    dmul_fulldsp     
    dmul_maxdsp      
    dsqrt_fabric     
    drsqrt_fulldsp   
    drecip_fulldsp   
    hadd_fabric      
    hadd_meddsp      
    hadd_fulldsp     
    hsub_fabric      
    hsub_meddsp      
    hsub_fulldsp     
    hdiv_fabric      
    hmul_fabric      
    hmul_fulldsp     
    hmul_maxdsp      
    hsqrt_fabric     
)

work_dir=/home/nx08/nx08/markkfpga/vitis_microbench
vitis_data=/home/nx08/nx08/markkfpga/vitis-data
num_configs=${#configs[@]}

# compile
for config in "${configs[@]}"; do
    #root_dir=/home/nx08/nx08/markkfpga/stac-a3-V10-hacc-events-4/reference_files_bcast_hw
    root_dir=${work_dir}/reference_files_hw_${config}
    #root_dir=${work_dir}/reference_files_vck5000_hw_${config}
    bin_name=${config}
    kernel_name=krnl_bench
    python3 ${vitis_data}/main.py $root_dir $bin_name $kernel_name >> ${work_dir}/scripts/utilisation_u280.txt    
done

