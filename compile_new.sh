#!/bin/bash

TARGET=hw

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
    
num_configs=${#configs[@]}
counter=0
batch_size=0

rm -rf reference_files_${TARGET}_fadd_fabric
mkdir -p reference_files_${TARGET}_fadd_fabric

for config in "${configs[@]}"; do
    # link files
    if [ $counter -eq 0 ]; then    
        cd reference_files_${TARGET}_${config}; v++ -t ${TARGET} --config ../link.cfg -O3 -l -o"${config}.${TARGET}.xclbin" ${config}.xo &     
    else
        cd ../reference_files_${TARGET}_${config}; v++ -t ${TARGET} --config ../link.cfg -O3 -l -o"${config}.${TARGET}.xclbin" ${config}.xo &     
    fi

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

for config in "${configs[@]}"; do
    # copy bitstream to dir
    cd ../reference_files_${TARGET}_${config}; cp ${config}.${TARGET}.xclbin ../bin/
done
