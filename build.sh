#!/bin/bash

######################################
### requires the following params
###
### see the following files:
### build_floating_point.sh
### build_fixed_point.sh
######################################

### #TARGET=sw_emu
### TARGET=hw
### 
### #FPGA=u280
### FPGA=vck5000
### 
### FP_TYPE=fixed_point
### #FP_TYPE=floating_point
### 
### IF_COMPILE=1
### IF_LINK=1
###
### #KERNEL_TYPE=single
### KERNEL_TYPE=multi
### 
### configs=(
###     fadd_fabric      
###     fadd_fulldsp     
###     fadd_primitivedsp
###     fsub_fabric      
###     fsub_fulldsp     
###     fsub_primitivedsp
###     fdiv_fabric      
###     fexp_fabric      
###     fexp_meddsp      
###     fexp_fulldsp     
###     flog_fabric      
###     flog_meddsp      
###     flog_fulldsp     
###     fmul_fabric      
###     fmul_meddsp      
###     fmul_fulldsp     
###     fmul_maxdsp      
###     fmul_primitivedsp
###     fsqrt_fabric     
###     frsqrt_fabric    
###     frsqrt_fulldsp   
###     frecip_fabric    
###     frecip_fulldsp   
###     dadd_fabric      
###     dadd_fulldsp     
###     dsub_fabric      
###     dsub_fulldsp     
###     ddiv_fabric      
###     dexp_fabric      
###     dexp_meddsp      
###     dexp_fulldsp     
###     dlog_fabric      
###     dlog_meddsp      
###     dlog_fulldsp     
###     dmul_fabric      
###     dmul_meddsp      
###     dmul_fulldsp     
###     dmul_maxdsp      
###     dsqrt_fabric     
###     drsqrt_fulldsp   
###     drecip_fulldsp   
###     hadd_fabric      
###     hadd_meddsp      
###     hadd_fulldsp     
###     hsub_fabric      
###     hsub_meddsp      
###     hsub_fulldsp     
###     hdiv_fabric      
###     hmul_fabric      
###     hmul_fulldsp     
###     hmul_maxdsp      
###     hsqrt_fabric     
### )

mkdir -p bin/${FPGA}/${KERNEL_TYPE}
    
num_configs=${#configs[@]}
counter=0
batch_size=0

echo "CONFIG_STARTS"
echo "TARGET: ${TARGET}"
echo "FPGA: ${FPGA}"
echo "FP_TYPE: ${FP_TYPE}"
echo "KERNEL_TYPE: ${KERNEL_TYPE}"
echo "IF_COMPILE: ${IF_COMPILE}"
echo "IF_LINK: ${IF_LINK}"
echo "NUM_CONFIGS: ${num_configs}"
echo "CONFIG_ENDS"

# compile
if [ $IF_COMPILE -eq 1 ]; then
    for config in "${configs[@]}"; do
        if [ $counter -ne 0 ]; then
            cd ..;
        fi

        rm -rf reference_files_${FPGA}_${TARGET}_${config}_${KERNEL_TYPE} 
        mkdir -p reference_files_${FPGA}_${TARGET}_${config}_${KERNEL_TYPE} 

        cd reference_files_${FPGA}_${TARGET}_${config}_${KERNEL_TYPE}; v++ -t ${TARGET} --config ../design_${FPGA}.cfg -j 8 --save-temps -O3 -c -k krnl_bench -I'../include' -I"../src/device/${FP_TYPE}" -o"${config}.xo" ../src/device/${FP_TYPE}/${config}.cpp & 

        counter=$((counter+1))
        batch_size=$((batch_size+1))
        
        if [ $batch_size -eq 8 ]; then
            # run eight linking processes at a time
            # could keep a pool of eight running processes at all times
            # but processes are started at the same time
            # and will roughly finish at the same time too
            batch_size=0 
            wait
        fi
    done
    wait
fi

batch_size=0
output_format=xclbin

if [ "$FPGA" = "vck" ]; then
    output_format=xsa 
fi

# link u280 or vck5000
if [ $IF_LINK -eq 1 ]; then

    for config in "${configs[@]}"; do
        type=algebraic
        if [[ $config == *"add"* ]] || [[ $config == *"sub"* ]] || [[ $config == *"mul"* ]] || [[ $config == *"div"* ]]; then
            type=arithmetic
        fi

        cd ../reference_files_${FPGA}_${TARGET}_${config}_${KERNEL_TYPE}; v++ -t ${TARGET} --config ../link_${type}_${FPGA}_${KERNEL_TYPE}.cfg -j 8 --save-temps -O3 -l -o"${config}.${TARGET}.${output_format}" ${config}.xo &

        batch_size=$((batch_size+1))
        
        if [ $batch_size -eq 8 ]; then
            batch_size=0 
            wait
        fi
    done
    wait
fi

batch_size=0

# package if vck5000
if [ $IF_LINK -eq 1 ]; then
    if [ "$FPGA" = "vck" ]; then
        for config in "${configs[@]}"; do
            cd ../reference_files_${FPGA}_${TARGET}_${config}_${KERNEL_TYPE}; v++ -p -t ${TARGET} -f xilinx_vck5000_gen4x8_xdma_2_202210_1 ${config}.${TARGET}.xsa -o ${config}.${TARGET}.xclbin --package.boot_mode=ospi &

            batch_size=$((batch_size+1))

            # finish batch of eight builds before moving on to next            
            if [ $batch_size -eq 8 ]; then
                batch_size=0 
                wait
            fi
        done
    fi
fi

for config in "${configs[@]}"; do
    # copy bitstream to dir
    cd ../reference_files_${FPGA}_${TARGET}_${config}_${KERNEL_TYPE}; cp ${config}.${TARGET}.xclbin ../bin/${FPGA}/${KERNEL_TYPE}/
done
