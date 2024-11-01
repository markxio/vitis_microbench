#!/bin/bash

TARGET=hw

# remove tmp dirs
rm -rf reference_files_${TARGET}_fadd_fabric          
rm -rf reference_files_${TARGET}_fadd_fulldsp          
rm -rf reference_files_${TARGET}_fadd_primitivedsp          
rm -rf reference_files_${TARGET}_fsub_fabric          
rm -rf reference_files_${TARGET}_fsub_fulldsp          
rm -rf reference_files_${TARGET}_fsub_primitivedsp          
rm -rf reference_files_${TARGET}_fdiv_fabric          
rm -rf reference_files_${TARGET}_fexp_fabric          
rm -rf reference_files_${TARGET}_fexp_meddsp          
rm -rf reference_files_${TARGET}_fexp_fulldsp          
rm -rf reference_files_${TARGET}_flog_fabric          
rm -rf reference_files_${TARGET}_flog_meddsp          
rm -rf reference_files_${TARGET}_flog_fulldsp          
rm -rf reference_files_${TARGET}_fmul_fabric          
rm -rf reference_files_${TARGET}_fmul_meddsp          
rm -rf reference_files_${TARGET}_fmul_fulldsp          
rm -rf reference_files_${TARGET}_fmul_maxdsp          
rm -rf reference_files_${TARGET}_fmul_primitivedsp          
rm -rf reference_files_${TARGET}_fsqrt_fabric          
rm -rf reference_files_${TARGET}_frsqrt_fabric          
rm -rf reference_files_${TARGET}_frsqrt_fulldsp          
rm -rf reference_files_${TARGET}_frecip_fabric          
rm -rf reference_files_${TARGET}_frecip_fulldsp          
rm -rf reference_files_${TARGET}_dadd_fabric          
rm -rf reference_files_${TARGET}_dadd_fulldsp          
rm -rf reference_files_${TARGET}_dsub_fabric          
rm -rf reference_files_${TARGET}_dsub_fulldsp          
rm -rf reference_files_${TARGET}_ddiv_fabric          
rm -rf reference_files_${TARGET}_dexp_fabric          
rm -rf reference_files_${TARGET}_dexp_meddsp          
rm -rf reference_files_${TARGET}_dexp_fulldsp          
rm -rf reference_files_${TARGET}_dlog_fabric          
rm -rf reference_files_${TARGET}_dlog_meddsp          
rm -rf reference_files_${TARGET}_dlog_fulldsp          
rm -rf reference_files_${TARGET}_dmul_fabric          
rm -rf reference_files_${TARGET}_dmul_meddsp          
rm -rf reference_files_${TARGET}_dmul_fulldsp          
rm -rf reference_files_${TARGET}_dmul_maxdsp          
rm -rf reference_files_${TARGET}_dsqrt_fabric          
rm -rf reference_files_${TARGET}_drsqrt_fulldsp          
rm -rf reference_files_${TARGET}_drecip_fulldsp          
rm -rf reference_files_${TARGET}_hadd_fabric          
rm -rf reference_files_${TARGET}_hadd_meddsp          
rm -rf reference_files_${TARGET}_hadd_fulldsp          
rm -rf reference_files_${TARGET}_hsub_fabric          
rm -rf reference_files_${TARGET}_hsub_meddsp          
rm -rf reference_files_${TARGET}_hsub_fulldsp          
rm -rf reference_files_${TARGET}_hdiv_fabric          
rm -rf reference_files_${TARGET}_hmul_fabric          
rm -rf reference_files_${TARGET}_hmul_fulldsp          
rm -rf reference_files_${TARGET}_hmul_maxdsp          
rm -rf reference_files_${TARGET}_hsqrt_fabric          

# create tmp dirs
mkdir -p reference_files_${TARGET}_fadd_fabric          
mkdir -p reference_files_${TARGET}_fadd_fulldsp          
mkdir -p reference_files_${TARGET}_fadd_primitivedsp          
mkdir -p reference_files_${TARGET}_fsub_fabric          
mkdir -p reference_files_${TARGET}_fsub_fulldsp          
mkdir -p reference_files_${TARGET}_fsub_primitivedsp          
mkdir -p reference_files_${TARGET}_fdiv_fabric          
mkdir -p reference_files_${TARGET}_fexp_fabric          
mkdir -p reference_files_${TARGET}_fexp_meddsp          
mkdir -p reference_files_${TARGET}_fexp_fulldsp          
mkdir -p reference_files_${TARGET}_flog_fabric          
mkdir -p reference_files_${TARGET}_flog_meddsp          
mkdir -p reference_files_${TARGET}_flog_fulldsp          
mkdir -p reference_files_${TARGET}_fmul_fabric          
mkdir -p reference_files_${TARGET}_fmul_meddsp          
mkdir -p reference_files_${TARGET}_fmul_fulldsp          
mkdir -p reference_files_${TARGET}_fmul_maxdsp          
mkdir -p reference_files_${TARGET}_fmul_primitivedsp          
mkdir -p reference_files_${TARGET}_fsqrt_fabric          
mkdir -p reference_files_${TARGET}_frsqrt_fabric          
mkdir -p reference_files_${TARGET}_frsqrt_fulldsp          
mkdir -p reference_files_${TARGET}_frecip_fabric          
mkdir -p reference_files_${TARGET}_frecip_fulldsp          
mkdir -p reference_files_${TARGET}_dadd_fabric          
mkdir -p reference_files_${TARGET}_dadd_fulldsp          
mkdir -p reference_files_${TARGET}_dsub_fabric          
mkdir -p reference_files_${TARGET}_dsub_fulldsp          
mkdir -p reference_files_${TARGET}_ddiv_fabric          
mkdir -p reference_files_${TARGET}_dexp_fabric          
mkdir -p reference_files_${TARGET}_dexp_meddsp          
mkdir -p reference_files_${TARGET}_dexp_fulldsp          
mkdir -p reference_files_${TARGET}_dlog_fabric          
mkdir -p reference_files_${TARGET}_dlog_meddsp          
mkdir -p reference_files_${TARGET}_dlog_fulldsp          
mkdir -p reference_files_${TARGET}_dmul_fabric          
mkdir -p reference_files_${TARGET}_dmul_meddsp          
mkdir -p reference_files_${TARGET}_dmul_fulldsp          
mkdir -p reference_files_${TARGET}_dmul_maxdsp          
mkdir -p reference_files_${TARGET}_dsqrt_fabric          
mkdir -p reference_files_${TARGET}_drsqrt_fulldsp          
mkdir -p reference_files_${TARGET}_drecip_fulldsp          
mkdir -p reference_files_${TARGET}_hadd_fabric          
mkdir -p reference_files_${TARGET}_hadd_meddsp          
mkdir -p reference_files_${TARGET}_hadd_fulldsp          
mkdir -p reference_files_${TARGET}_hsub_fabric          
mkdir -p reference_files_${TARGET}_hsub_meddsp          
mkdir -p reference_files_${TARGET}_hsub_fulldsp          
mkdir -p reference_files_${TARGET}_hdiv_fabric          
mkdir -p reference_files_${TARGET}_hmul_fabric          
mkdir -p reference_files_${TARGET}_hmul_fulldsp          
mkdir -p reference_files_${TARGET}_hmul_maxdsp          
mkdir -p reference_files_${TARGET}_hsqrt_fabric          

mkdir -p bin

# compile
cd reference_files_${TARGET}_fadd_fabric          ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'fadd_fabric.xo'        ../src/device/fadd_fabric.cpp       &  
cd ../reference_files_${TARGET}_fadd_fulldsp      ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'fadd_fulldsp.xo'       ../src/device/fadd_fulldsp.cpp      &   
cd ../reference_files_${TARGET}_fadd_primitivedsp ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'fadd_primitivedsp.xo'  ../src/device/fadd_primitivedsp.cpp &        
cd ../reference_files_${TARGET}_fsub_fabric       ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'fsub_fabric.xo'        ../src/device/fsub_fabric.cpp       &  
cd ../reference_files_${TARGET}_fsub_fulldsp      ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'fsub_fulldsp.xo'       ../src/device/fsub_fulldsp.cpp      &   
cd ../reference_files_${TARGET}_fsub_primitivedsp ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'fsub_primitivedsp.xo'  ../src/device/fsub_primitivedsp.cpp &        
cd ../reference_files_${TARGET}_fdiv_fabric       ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'fdiv_fabric.xo'        ../src/device/fdiv_fabric.cpp       &  
cd ../reference_files_${TARGET}_fexp_fabric       ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'fexp_fabric.xo'        ../src/device/fexp_fabric.cpp       &  
cd ../reference_files_${TARGET}_fexp_meddsp       ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'fexp_meddsp.xo'        ../src/device/fexp_meddsp.cpp       &  
cd ../reference_files_${TARGET}_fexp_fulldsp      ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'fexp_fulldsp.xo'       ../src/device/fexp_fulldsp.cpp      &   
cd ../reference_files_${TARGET}_flog_fabric       ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'flog_fabric.xo'        ../src/device/flog_fabric.cpp       &  
cd ../reference_files_${TARGET}_flog_meddsp       ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'flog_meddsp.xo'        ../src/device/flog_meddsp.cpp       &  
cd ../reference_files_${TARGET}_flog_fulldsp      ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'flog_fulldsp.xo'       ../src/device/flog_fulldsp.cpp      &   
cd ../reference_files_${TARGET}_fmul_fabric       ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'fmul_fabric.xo'        ../src/device/fmul_fabric.cpp       &  
cd ../reference_files_${TARGET}_fmul_meddsp       ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'fmul_meddsp.xo'        ../src/device/fmul_meddsp.cpp       &  
cd ../reference_files_${TARGET}_fmul_fulldsp      ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'fmul_fulldsp.xo'       ../src/device/fmul_fulldsp.cpp      &   
cd ../reference_files_${TARGET}_fmul_maxdsp       ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'fmul_maxdsp.xo'        ../src/device/fmul_maxdsp.cpp       &  
cd ../reference_files_${TARGET}_fmul_primitivedsp ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'fmul_primitivedsp.xo'  ../src/device/fmul_primitivedsp.cpp &        
cd ../reference_files_${TARGET}_fsqrt_fabric      ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'fsqrt_fabric.xo'       ../src/device/fsqrt_fabric.cpp      &   
cd ../reference_files_${TARGET}_frsqrt_fabric     ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'frsqrt_fabric.xo'      ../src/device/frsqrt_fabric.cpp     &    
cd ../reference_files_${TARGET}_frsqrt_fulldsp    ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'frsqrt_fulldsp.xo'     ../src/device/frsqrt_fulldsp.cpp    &     
cd ../reference_files_${TARGET}_frecip_fabric     ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'frecip_fabric.xo'      ../src/device/frecip_fabric.cpp     &    
cd ../reference_files_${TARGET}_frecip_fulldsp    ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'frecip_fulldsp.xo'     ../src/device/frecip_fulldsp.cpp    &     
cd ../reference_files_${TARGET}_dadd_fabric       ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'dadd_fabric.xo'        ../src/device/dadd_fabric.cpp       &  
cd ../reference_files_${TARGET}_dadd_fulldsp      ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'dadd_fulldsp.xo'       ../src/device/dadd_fulldsp.cpp      &   

wait

cd ../reference_files_${TARGET}_dsub_fabric       ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'dsub_fabric.xo'        ../src/device/dsub_fabric.cpp       &  
cd ../reference_files_${TARGET}_dsub_fulldsp      ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'dsub_fulldsp.xo'       ../src/device/dsub_fulldsp.cpp      &   
cd ../reference_files_${TARGET}_ddiv_fabric       ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'ddiv_fabric.xo'        ../src/device/ddiv_fabric.cpp       &  
cd ../reference_files_${TARGET}_dexp_fabric       ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'dexp_fabric.xo'        ../src/device/dexp_fabric.cpp       &  
cd ../reference_files_${TARGET}_dexp_meddsp       ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'dexp_meddsp.xo'        ../src/device/dexp_meddsp.cpp       &  
cd ../reference_files_${TARGET}_dexp_fulldsp      ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'dexp_fulldsp.xo'       ../src/device/dexp_fulldsp.cpp      &   
cd ../reference_files_${TARGET}_dlog_fabric       ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'dlog_fabric.xo'        ../src/device/dlog_fabric.cpp       &  
cd ../reference_files_${TARGET}_dlog_meddsp       ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'dlog_meddsp.xo'        ../src/device/dlog_meddsp.cpp       &  
cd ../reference_files_${TARGET}_dlog_fulldsp      ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'dlog_fulldsp.xo'       ../src/device/dlog_fulldsp.cpp      &   
cd ../reference_files_${TARGET}_dmul_fabric       ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'dmul_fabric.xo'        ../src/device/dmul_fabric.cpp       &  
cd ../reference_files_${TARGET}_dmul_meddsp       ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'dmul_meddsp.xo'        ../src/device/dmul_meddsp.cpp       &  
cd ../reference_files_${TARGET}_dmul_fulldsp      ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'dmul_fulldsp.xo'       ../src/device/dmul_fulldsp.cpp      &   
cd ../reference_files_${TARGET}_dmul_maxdsp       ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'dmul_maxdsp.xo'        ../src/device/dmul_maxdsp.cpp       &  
cd ../reference_files_${TARGET}_dsqrt_fabric      ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'dsqrt_fabric.xo'       ../src/device/dsqrt_fabric.cpp      &   
cd ../reference_files_${TARGET}_drsqrt_fulldsp    ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'drsqrt_fulldsp.xo'     ../src/device/drsqrt_fulldsp.cpp    &     
cd ../reference_files_${TARGET}_drecip_fulldsp    ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'drecip_fulldsp.xo'     ../src/device/drecip_fulldsp.cpp    &     
cd ../reference_files_${TARGET}_hadd_fabric       ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'hadd_fabric.xo'        ../src/device/hadd_fabric.cpp       &  
cd ../reference_files_${TARGET}_hadd_meddsp       ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'hadd_meddsp.xo'        ../src/device/hadd_meddsp.cpp       &  
cd ../reference_files_${TARGET}_hadd_fulldsp      ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'hadd_fulldsp.xo'       ../src/device/hadd_fulldsp.cpp      &   
cd ../reference_files_${TARGET}_hsub_fabric       ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'hsub_fabric.xo'        ../src/device/hsub_fabric.cpp       &  
cd ../reference_files_${TARGET}_hsub_meddsp       ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'hsub_meddsp.xo'        ../src/device/hsub_meddsp.cpp       &  
cd ../reference_files_${TARGET}_hsub_fulldsp      ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'hsub_fulldsp.xo'       ../src/device/hsub_fulldsp.cpp      &   
cd ../reference_files_${TARGET}_hdiv_fabric       ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'hdiv_fabric.xo'        ../src/device/hdiv_fabric.cpp       &  
cd ../reference_files_${TARGET}_hmul_fabric       ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'hmul_fabric.xo'        ../src/device/hmul_fabric.cpp       &  
cd ../reference_files_${TARGET}_hmul_fulldsp      ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'hmul_fulldsp.xo'       ../src/device/hmul_fulldsp.cpp      &   
cd ../reference_files_${TARGET}_hmul_maxdsp       ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'hmul_maxdsp.xo'        ../src/device/hmul_maxdsp.cpp       &  
cd ../reference_files_${TARGET}_hsqrt_fabric      ; v++ -t ${TARGET} --config ../design.cfg --save-temps -j 8 -O3 -c -k krnl_bench -I'../include' -I'../src/device' -o'hsqrt_fabric.xo'       ../src/device/hsqrt_fabric.cpp      &   

wait
