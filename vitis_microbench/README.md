# Building the kernels

This directory contains three stages that should be executed in the following order:
1. Generate the benchmark kernels
2. Compile and link the kernels with Vitis HLS and v++
3. Run the kernels which generates FPGA runtime, power draw and energy profiles
4. Plot the run profiles

## Generate the benchmark kernels


```
cd vitis-microbench/scripts/generate
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements
``` 

## Compile and link

Vitis and v++ must be available. On the [ExCALIBUR H&ES FPGA testbed](https://fpga.epcc.ed.ac.uk/index.html), load vitis:
```
source /home/nx08/shared/fpga/fpga_modules.sh
module load vitis/2021.2
```

Compile and link the device kernels with Vitis HLS and v++, for which we provide build scripts in the [build/](build/) directory.
- build_u280_floating_point.sh
- build_u280_fixed_point.sh
- build_vck5000_floating_point.sh
- build_vck5000_fixed_point.sh

The [build.sh](../build.sh) scripts will save temporary files in a directory named `reference_files_${FPGA}_${TARGET}_${config}_${KERNEL_TYPE}`, where
- `FPGA`: (u280|vck)
- `TARGET`: (hw|hw_emu|sw_emu)
- `config`: fixed-point or floating-point configurations of the arithmetic operations, for example `add_16_6_fabric` or `fadd_fabric`
- `KERNEL_TYPE`: single or multi-CU (single|multi) 

We also have to build the host code. For the host code, we require the git submodule `vitis-power` to read FPGA power draw in cpp on the host:
```
# in the root directory of this project (/vitis-microbench)
# init and update the submodules
git submodule init
git subomdule update

# now build the host code using the Makefile
make host
```

More information are provided in [build/README.md](build/README.md).

## Run

Once the kernels have been successfully built and linked, the resulting bitstreams are available in the bin/ directory.
