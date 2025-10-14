#!/bin/bash

#TARGET=sw_emu
TARGET=hw

FPGA=vck

FP_TYPE=floating_point

KERNEL_TYPE=single
#KERNEL_TYPE=multi

IF_COMPILE=1
IF_LINK=1

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
    drsqrt_fabric
    drsqrt_fulldsp
    drecip_fabric  
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

cd ../../ ;
. ./build.sh
