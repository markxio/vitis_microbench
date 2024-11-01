#!/bin/bash

TARGET=hw

cd reference_files_${TARGET}_fadd_fabric       ; v++ -t ${TARGET} --config ../link.cfg -O3 -l -o"fadd_fabric.${TARGET}.xclbin" fadd_fabric.xo                 &     
cd ../reference_files_${TARGET}_fadd_fulldsp      ; v++ -t ${TARGET} --config ../link_arithmetic.cfg -j 8 -O3 -l -o"fadd_fulldsp.${TARGET}.xclbin" fadd_fulldsp.xo            &          
cd ../reference_files_${TARGET}_fadd_primitivedsp ; v++ -t ${TARGET} --config ../link_arithmetic.cfg -j 8 -O3 -l -o"fadd_primitivedsp.${TARGET}.xclbin" fadd_primitivedsp.xo  &                    
cd ../reference_files_${TARGET}_fsub_fabric       ; v++ -t ${TARGET} --config ../link_arithmetic.cfg -j 8 -O3 -l -o"fsub_fabric.${TARGET}.xclbin" fsub_fabric.xo              &        
cd ../reference_files_${TARGET}_fsub_fulldsp      ; v++ -t ${TARGET} --config ../link_arithmetic.cfg -j 8 -O3 -l -o"fsub_fulldsp.${TARGET}.xclbin" fsub_fulldsp.xo            &          
cd ../reference_files_${TARGET}_fsub_primitivedsp ; v++ -t ${TARGET} --config ../link_arithmetic.cfg -j 8 -O3 -l -o"fsub_primitivedsp.${TARGET}.xclbin" fsub_primitivedsp.xo  &                    
cd ../reference_files_${TARGET}_fdiv_fabric       ; v++ -t ${TARGET} --config ../link_arithmetic.cfg -j 8 -O3 -l -o"fdiv_fabric.${TARGET}.xclbin" fdiv_fabric.xo              &        
cd ../reference_files_${TARGET}_fexp_fabric       ; v++ -t ${TARGET} --config ../link_algebraic.cfg -j 8 -O3 -l -o"fexp_fabric.${TARGET}.xclbin" fexp_fabric.xo              &        

wait

cd ../reference_files_${TARGET}_fexp_meddsp       ; v++ -t ${TARGET} --config ../link_algebraic.cfg -j 8 -O3 -l -o"fexp_meddsp.${TARGET}.xclbin" fexp_meddsp.xo              &        
cd ../reference_files_${TARGET}_fexp_fulldsp      ; v++ -t ${TARGET} --config ../link_algebraic.cfg -j 8 -O3 -l -o"fexp_fulldsp.${TARGET}.xclbin" fexp_fulldsp.xo            &          
cd ../reference_files_${TARGET}_flog_fabric       ; v++ -t ${TARGET} --config ../link_algebraic.cfg -j 8 -O3 -l -o"flog_fabric.${TARGET}.xclbin" flog_fabric.xo              &        
cd ../reference_files_${TARGET}_flog_meddsp       ; v++ -t ${TARGET} --config ../link_algebraic.cfg -j 8 -O3 -l -o"flog_meddsp.${TARGET}.xclbin" flog_meddsp.xo              &        
cd ../reference_files_${TARGET}_flog_fulldsp      ; v++ -t ${TARGET} --config ../link_algebraic.cfg -j 8 -O3 -l -o"flog_fulldsp.${TARGET}.xclbin" flog_fulldsp.xo            &          
cd ../reference_files_${TARGET}_fmul_fabric       ; v++ -t ${TARGET} --config ../link_arithmetic.cfg -j 8 -O3 -l -o"fmul_fabric.${TARGET}.xclbin" fmul_fabric.xo              &        
cd ../reference_files_${TARGET}_fmul_meddsp       ; v++ -t ${TARGET} --config ../link_arithmetic.cfg -j 8 -O3 -l -o"fmul_meddsp.${TARGET}.xclbin" fmul_meddsp.xo              &        
cd ../reference_files_${TARGET}_fmul_fulldsp      ; v++ -t ${TARGET} --config ../link_arithmetic.cfg -j 8 -O3 -l -o"fmul_fulldsp.${TARGET}.xclbin" fmul_fulldsp.xo            &          

wait

cd ../reference_files_${TARGET}_fmul_maxdsp       ; v++ -t ${TARGET} --config ../link_arithmetic.cfg -j 8 -O3 -l -o"fmul_maxdsp.${TARGET}.xclbin" fmul_maxdsp.xo              &        
cd ../reference_files_${TARGET}_fmul_primitivedsp ; v++ -t ${TARGET} --config ../link_arithmetic.cfg -j 8 -O3 -l -o"fmul_primitivedsp.${TARGET}.xclbin" fmul_primitivedsp.xo  &                    
cd ../reference_files_${TARGET}_fsqrt_fabric      ; v++ -t ${TARGET} --config ../link_algebraic.cfg -j 8 -O3 -l -o"fsqrt_fabric.${TARGET}.xclbin" fsqrt_fabric.xo            &          
cd ../reference_files_${TARGET}_frsqrt_fabric     ; v++ -t ${TARGET} --config ../link_algebraic.cfg -j 8 -O3 -l -o"frsqrt_fabric.${TARGET}.xclbin" frsqrt_fabric.xo          &            
cd ../reference_files_${TARGET}_frsqrt_fulldsp    ; v++ -t ${TARGET} --config ../link_algebraic.cfg -j 8 -O3 -l -o"frsqrt_fulldsp.${TARGET}.xclbin" frsqrt_fulldsp.xo        &              
cd ../reference_files_${TARGET}_frecip_fabric     ; v++ -t ${TARGET} --config ../link_algebraic.cfg -j 8 -O3 -l -o"frecip_fabric.${TARGET}.xclbin" frecip_fabric.xo          &            
cd ../reference_files_${TARGET}_frecip_fulldsp    ; v++ -t ${TARGET} --config ../link_algebraic.cfg -j 8 -O3 -l -o"frecip_fulldsp.${TARGET}.xclbin" frecip_fulldsp.xo        &              
cd ../reference_files_${TARGET}_dadd_fabric       ; v++ -t ${TARGET} --config ../link_arithmetic.cfg -j 8 -O3 -l -o"dadd_fabric.${TARGET}.xclbin" dadd_fabric.xo              &        
cd ../reference_files_${TARGET}_dadd_fulldsp      ; v++ -t ${TARGET} --config ../link_arithmetic.cfg -j 8 -O3 -l -o"dadd_fulldsp.${TARGET}.xclbin" dadd_fulldsp.xo            &          

wait

cd ../reference_files_${TARGET}_dsub_fabric       ; v++ -t ${TARGET} --config ../link_arithmetic.cfg -j 8 -O3 -l -o"dsub_fabric.${TARGET}.xclbin" dsub_fabric.xo              &        
cd ../reference_files_${TARGET}_dsub_fulldsp      ; v++ -t ${TARGET} --config ../link_arithmetic.cfg -j 8 -O3 -l -o"dsub_fulldsp.${TARGET}.xclbin" dsub_fulldsp.xo            &          
cd ../reference_files_${TARGET}_ddiv_fabric       ; v++ -t ${TARGET} --config ../link_arithmetic.cfg -j 8 -O3 -l -o"ddiv_fabric.${TARGET}.xclbin" ddiv_fabric.xo              &        
cd ../reference_files_${TARGET}_dexp_fabric       ; v++ -t ${TARGET} --config ../link_algebraic.cfg -j 8 -O3 -l -o"dexp_fabric.${TARGET}.xclbin" dexp_fabric.xo              &        
cd ../reference_files_${TARGET}_dexp_meddsp       ; v++ -t ${TARGET} --config ../link_algebraic.cfg -j 8 -O3 -l -o"dexp_meddsp.${TARGET}.xclbin" dexp_meddsp.xo              &        
cd ../reference_files_${TARGET}_dexp_fulldsp      ; v++ -t ${TARGET} --config ../link_algebraic.cfg -j 8 -O3 -l -o"dexp_fulldsp.${TARGET}.xclbin" dexp_fulldsp.xo            &          
cd ../reference_files_${TARGET}_dlog_fabric       ; v++ -t ${TARGET} --config ../link_algebraic.cfg -j 8 -O3 -l -o"dlog_fabric.${TARGET}.xclbin" dlog_fabric.xo              &        
cd ../reference_files_${TARGET}_dlog_meddsp       ; v++ -t ${TARGET} --config ../link_algebraic.cfg -j 8 -O3 -l -o"dlog_meddsp.${TARGET}.xclbin" dlog_meddsp.xo              &        

wait

cd ../reference_files_${TARGET}_dlog_fulldsp      ; v++ -t ${TARGET} --config ../link_algebraic.cfg -j 8 -O3 -l -o"dlog_fulldsp.${TARGET}.xclbin" dlog_fulldsp.xo            &          
cd ../reference_files_${TARGET}_dmul_fabric       ; v++ -t ${TARGET} --config ../link_arithmetic.cfg -j 8 -O3 -l -o"dmul_fabric.${TARGET}.xclbin" dmul_fabric.xo              &        
cd ../reference_files_${TARGET}_dmul_meddsp       ; v++ -t ${TARGET} --config ../link_arithmetic.cfg -j 8 -O3 -l -o"dmul_meddsp.${TARGET}.xclbin" dmul_meddsp.xo              &        
cd ../reference_files_${TARGET}_dmul_fulldsp      ; v++ -t ${TARGET} --config ../link_arithmetic.cfg -j 8 -O3 -l -o"dmul_fulldsp.${TARGET}.xclbin" dmul_fulldsp.xo            &          
cd ../reference_files_${TARGET}_dmul_maxdsp       ; v++ -t ${TARGET} --config ../link_arithmetic.cfg -j 8 -O3 -l -o"dmul_maxdsp.${TARGET}.xclbin" dmul_maxdsp.xo              &        
cd ../reference_files_${TARGET}_dsqrt_fabric      ; v++ -t ${TARGET} --config ../link_algebraic.cfg -j 8 -O3 -l -o"dsqrt_fabric.${TARGET}.xclbin" dsqrt_fabric.xo            &          
cd ../reference_files_${TARGET}_drsqrt_fulldsp    ; v++ -t ${TARGET} --config ../link_algebraic.cfg -j 8 -O3 -l -o"drsqrt_fulldsp.${TARGET}.xclbin" drsqrt_fulldsp.xo        &              
cd ../reference_files_${TARGET}_drecip_fulldsp    ; v++ -t ${TARGET} --config ../link_algebraic.cfg -j 8 -O3 -l -o"drecip_fulldsp.${TARGET}.xclbin" drecip_fulldsp.xo        &              

wait

cd ../reference_files_${TARGET}_hadd_fabric       ; v++ -t ${TARGET} --config ../link_arithmetic.cfg -j 8 -O3 -l -o"hadd_fabric.${TARGET}.xclbin" hadd_fabric.xo              &        
cd ../reference_files_${TARGET}_hadd_meddsp       ; v++ -t ${TARGET} --config ../link_arithmetic.cfg -j 8 -O3 -l -o"hadd_meddsp.${TARGET}.xclbin" hadd_meddsp.xo              &        
cd ../reference_files_${TARGET}_hadd_fulldsp      ; v++ -t ${TARGET} --config ../link_arithmetic.cfg -j 8 -O3 -l -o"hadd_fulldsp.${TARGET}.xclbin" hadd_fulldsp.xo            &          
cd ../reference_files_${TARGET}_hsub_fabric       ; v++ -t ${TARGET} --config ../link_arithmetic.cfg -j 8 -O3 -l -o"hsub_fabric.${TARGET}.xclbin" hsub_fabric.xo              &        
cd ../reference_files_${TARGET}_hsub_meddsp       ; v++ -t ${TARGET} --config ../link_arithmetic.cfg -j 8 -O3 -l -o"hsub_meddsp.${TARGET}.xclbin" hsub_meddsp.xo              &        
cd ../reference_files_${TARGET}_hsub_fulldsp      ; v++ -t ${TARGET} --config ../link_arithmetic.cfg -j 8 -O3 -l -o"hsub_fulldsp.${TARGET}.xclbin" hsub_fulldsp.xo            &          
cd ../reference_files_${TARGET}_hdiv_fabric       ; v++ -t ${TARGET} --config ../link_arithmetic.cfg -j 8 -O3 -l -o"hdiv_fabric.${TARGET}.xclbin" hdiv_fabric.xo              &        
cd ../reference_files_${TARGET}_hmul_fabric       ; v++ -t ${TARGET} --config ../link_arithmetic.cfg -j 8 -O3 -l -o"hmul_fabric.${TARGET}.xclbin" hmul_fabric.xo              &        
cd ../reference_files_${TARGET}_hmul_fulldsp      ; v++ -t ${TARGET} --config ../link_arithmetic.cfg -j 8 -O3 -l -o"hmul_fulldsp.${TARGET}.xclbin" hmul_fulldsp.xo            &          
cd ../reference_files_${TARGET}_hmul_maxdsp       ; v++ -t ${TARGET} --config ../link_arithmetic.cfg -j 8 -O3 -l -o"hmul_maxdsp.${TARGET}.xclbin" hmul_maxdsp.xo              &        
cd ../reference_files_${TARGET}_hsqrt_fabric      ; v++ -t ${TARGET} --config ../link_algebraic.cfg -j 8 -O3 -l -o"hsqrt_fabric.${TARGET}.xclbin" hsqrt_fabric.xo            &          

wait

cd ../reference_files_${TARGET}_fadd_fabric       ; cp fadd_fabric.${TARGET}.xclbin        ../bin/
cd ../reference_files_${TARGET}_fadd_fulldsp      ; cp fadd_fulldsp.${TARGET}.xclbin       ../bin/
cd ../reference_files_${TARGET}_fadd_primitivedsp ; cp fadd_primitivedsp.${TARGET}.xclbin  ../bin/
cd ../reference_files_${TARGET}_fsub_fabric       ; cp fsub_fabric.${TARGET}.xclbin        ../bin/
cd ../reference_files_${TARGET}_fsub_fulldsp      ; cp fsub_fulldsp.${TARGET}.xclbin       ../bin/
cd ../reference_files_${TARGET}_fsub_primitivedsp ; cp fsub_primitivedsp.${TARGET}.xclbin  ../bin/
cd ../reference_files_${TARGET}_fdiv_fabric       ; cp fdiv_fabric.${TARGET}.xclbin        ../bin/
cd ../reference_files_${TARGET}_fexp_fabric       ; cp fexp_fabric.${TARGET}.xclbin        ../bin/
cd ../reference_files_${TARGET}_fexp_meddsp       ; cp fexp_meddsp.${TARGET}.xclbin        ../bin/
cd ../reference_files_${TARGET}_fexp_fulldsp      ; cp fexp_fulldsp.${TARGET}.xclbin       ../bin/
cd ../reference_files_${TARGET}_flog_fabric       ; cp flog_fabric.${TARGET}.xclbin        ../bin/
cd ../reference_files_${TARGET}_flog_meddsp       ; cp flog_meddsp.${TARGET}.xclbin        ../bin/
cd ../reference_files_${TARGET}_flog_fulldsp      ; cp flog_fulldsp.${TARGET}.xclbin       ../bin/
cd ../reference_files_${TARGET}_fmul_fabric       ; cp fmul_fabric.${TARGET}.xclbin        ../bin/
cd ../reference_files_${TARGET}_fmul_meddsp       ; cp fmul_meddsp.${TARGET}.xclbin        ../bin/
cd ../reference_files_${TARGET}_fmul_fulldsp      ; cp fmul_fulldsp.${TARGET}.xclbin       ../bin/
cd ../reference_files_${TARGET}_fmul_maxdsp       ; cp fmul_maxdsp.${TARGET}.xclbin        ../bin/
cd ../reference_files_${TARGET}_fmul_primitivedsp ; cp fmul_primitivedsp.${TARGET}.xclbin  ../bin/
cd ../reference_files_${TARGET}_fsqrt_fabric      ; cp fsqrt_fabric.${TARGET}.xclbin       ../bin/
cd ../reference_files_${TARGET}_frsqrt_fabric     ; cp frsqrt_fabric.${TARGET}.xclbin      ../bin/
cd ../reference_files_${TARGET}_frsqrt_fulldsp    ; cp frsqrt_fulldsp.${TARGET}.xclbin     ../bin/
cd ../reference_files_${TARGET}_frecip_fabric     ; cp frecip_fabric.${TARGET}.xclbin      ../bin/
cd ../reference_files_${TARGET}_frecip_fulldsp    ; cp frecip_fulldsp.${TARGET}.xclbin     ../bin/
cd ../reference_files_${TARGET}_dadd_fabric       ; cp dadd_fabric.${TARGET}.xclbin        ../bin/
cd ../reference_files_${TARGET}_dadd_fulldsp      ; cp dadd_fulldsp.${TARGET}.xclbin       ../bin/
cd ../reference_files_${TARGET}_dsub_fabric       ; cp dsub_fabric.${TARGET}.xclbin        ../bin/
cd ../reference_files_${TARGET}_dsub_fulldsp      ; cp dsub_fulldsp.${TARGET}.xclbin       ../bin/
cd ../reference_files_${TARGET}_ddiv_fabric       ; cp ddiv_fabric.${TARGET}.xclbin        ../bin/
cd ../reference_files_${TARGET}_dexp_fabric       ; cp dexp_fabric.${TARGET}.xclbin        ../bin/
cd ../reference_files_${TARGET}_dexp_meddsp       ; cp dexp_meddsp.${TARGET}.xclbin        ../bin/
cd ../reference_files_${TARGET}_dexp_fulldsp      ; cp dexp_fulldsp.${TARGET}.xclbin       ../bin/
cd ../reference_files_${TARGET}_dlog_fabric       ; cp dlog_fabric.${TARGET}.xclbin        ../bin/
cd ../reference_files_${TARGET}_dlog_meddsp       ; cp dlog_meddsp.${TARGET}.xclbin        ../bin/
cd ../reference_files_${TARGET}_dlog_fulldsp      ; cp dlog_fulldsp.${TARGET}.xclbin       ../bin/
cd ../reference_files_${TARGET}_dmul_fabric       ; cp dmul_fabric.${TARGET}.xclbin        ../bin/
cd ../reference_files_${TARGET}_dmul_meddsp       ; cp dmul_meddsp.${TARGET}.xclbin        ../bin/
cd ../reference_files_${TARGET}_dmul_fulldsp      ; cp dmul_fulldsp.${TARGET}.xclbin       ../bin/
cd ../reference_files_${TARGET}_dmul_maxdsp       ; cp dmul_maxdsp.${TARGET}.xclbin        ../bin/
cd ../reference_files_${TARGET}_dsqrt_fabric      ; cp dsqrt_fabric.${TARGET}.xclbin       ../bin/
cd ../reference_files_${TARGET}_drsqrt_fulldsp    ; cp drsqrt_fulldsp.${TARGET}.xclbin     ../bin/
cd ../reference_files_${TARGET}_drecip_fulldsp    ; cp drecip_fulldsp.${TARGET}.xclbin     ../bin/
cd ../reference_files_${TARGET}_hadd_fabric       ; cp hadd_fabric.${TARGET}.xclbin        ../bin/
cd ../reference_files_${TARGET}_hadd_meddsp       ; cp hadd_meddsp.${TARGET}.xclbin        ../bin/
cd ../reference_files_${TARGET}_hadd_fulldsp      ; cp hadd_fulldsp.${TARGET}.xclbin       ../bin/
cd ../reference_files_${TARGET}_hsub_fabric       ; cp hsub_fabric.${TARGET}.xclbin        ../bin/
cd ../reference_files_${TARGET}_hsub_meddsp       ; cp hsub_meddsp.${TARGET}.xclbin        ../bin/
cd ../reference_files_${TARGET}_hsub_fulldsp      ; cp hsub_fulldsp.${TARGET}.xclbin       ../bin/
cd ../reference_files_${TARGET}_hdiv_fabric       ; cp hdiv_fabric.${TARGET}.xclbin        ../bin/
cd ../reference_files_${TARGET}_hmul_fabric       ; cp hmul_fabric.${TARGET}.xclbin        ../bin/
cd ../reference_files_${TARGET}_hmul_fulldsp      ; cp hmul_fulldsp.${TARGET}.xclbin       ../bin/
cd ../reference_files_${TARGET}_hmul_maxdsp       ; cp hmul_maxdsp.${TARGET}.xclbin        ../bin/
cd ../reference_files_${TARGET}_hsqrt_fabric      ; cp hsqrt_fabric.${TARGET}.xclbin       ../bin/
