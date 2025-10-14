#!/bin/bash

# same host for fixed- and floating-point
# same host for u280 and vck
# arithmetic requires two inputs
# algebraic requires one input

# bin/host_arithmetic bin/u280/multi/dadd_fabric.hw.xclbin reps=10000 run_number=1 fpga=u280 cus=10 fp_type=floating-point

if [[ $TARGET == "hw_emu" ]]; then
    export XCL_EMULATION_MODE=hw_emu
elif [[ $TARGET == "sw_emu" ]]; then
    export XCL_EMULATION_MODE=sw_emu
else
    unset XCL_EMULATION_MODE
fi

for bitstream in "${bitstreams[@]}"; do
    if [[ $bitstream == *"add"* ]] || [[ $bitstream == *"sub"* ]] || [[ $bitstream == *"mul"* ]] || [[ $bitstream == *"div"* ]]; then
        if [[ $FPGA == "u280" ]]; then
            #host=host_arithmetic
            number_cus=10
        else
            # vck
            #number_cus=28 # out of device resources
            number_cus=16
        fi
    else
        if [[ $FPGA == "u280" ]]; then
            #host=host_algebraic 
            number_cus=16
        else
            # vck
            #number_cus=30 # out of device resources
            number_cus=25
        fi
    fi

    if [[ $KERNEL_TYPE == "single" ]]; then
        number_cus=1
    fi

    for run_id in $(seq 1 $(($number_of_runs))); do
        echo $bitstream;
        bin/host bin/${FPGA}/${KERNEL_TYPE}/${bitstream} ${reps} ${run_id} ${FPGA} ${number_cus} ${FP_TYPE}
        sleep 2
    done
done

