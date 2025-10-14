# Building the kernels

This directory contains three stages, each represented by a subdirectory, that should be executed in the following order:
1. Generate the benchmark kernels
2. Compile and link the kernels with Vitis HLS and v++
3. Run the kernels which generates FPGA runtime, power draw and energy profiles
4. Plot the run profiles

## Generate the benchmark kernels

Generates a .cpp file for each kernel by substituting placeholders in kernel templates. The scripts are provided in the [generate/](generate/) directory. The [data/](generate/data/) directory contains .csv files specifying the kernel configurations for fixed-point and floating-point kernels. For fixed-point, the configuration includes:
- `Operation`: mul, add, sub, div, exp, log, sqrt, rsqrt, recip
- `Implementation`: fabric or dsp
- Combinations of `WordLength` and `IntegerBits` (W,I): (8,3), (8,4), (16,6), (16,8), (32,12), (32,16), (64,12), (64,24)

The configs for floating-point:
- `Operation`: fadd, fsub, fdiv, fexp, flog, fmul, fsqrt, frsqrt, frecip, dadd, dsub, ddiv, dexp, dlog, dmul, dsqrt, drsqrt, drecip, hadd, hsub, hdiv, hmul, hsqrt
- `Implementation`: fabric, fulldsp, primitivedsp, meddsp, maxdsp

Install the requirements into a virtual environment, then generate the kernels:
```
cd vitis_microbench/scripts/generate
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements

# in the project root dir, install the package in editable mode
pip -e .

# generate the kernels
python3 -m vitis_microbench.generate.generate
``` 

The kernel generation will place the .cpp files in the the source directories for fixed-point and floating-point (/vitis_microbench/src/device/). Once the .cpp files are available, build the device kernels and host code.

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

These build scripts include the following options:
- `FPGA`: (u280|vck)
- `TARGET`: (hw|hw_emu|sw_emu)
- `FP_TYPE`: (fixed_point|floating_point)
- `KERNEL_TYPE`: single or multi-CU (single|multi) 
- `IF_COMPILE`: (1|0)
- `IF_LINK`: (1|0)
- `BATCH_MAX`: the number of parallel kernel builds
- `J_PROCESSES`: -j flag for v++ (parallel processes per build)
- `configs`: list of fixed-point or floating-point configurations of the arithmetic operations, for example `add_16_6_fabric` or `fadd_fabric`

Build floating-point kernels for the u280:
```
cd build/
nohup ./build_u280_floating_point.sh &> build_u280_floating_point.log001 &
```

The [build.sh](../build.sh) scripts will save otherwise temporary files in a directory named `reference_files_${FPGA}_${TARGET}_${config}_${KERNEL_TYPE}`.

### Host code

We also have to build the host code. For the host code, we require the git submodule `vitis_power` to read FPGA power draw in cpp on the host:
```
# in the root directory of this project (/vitis_microbench)
# init and update the submodules
git submodule init
git subomdule update

# now build the host code using the Makefile
make host
```

## Run

Once the kernels have been successfully built and linked, the resulting bitstreams are available in the bin/ subdirectory of the top-level project dir. To facilitate running, [run/](run/) provides four scripts:

- run_u280_floating_point.sh
- run_u280_fixed_point.sh
- run_vck5000_floating_point.sh
- run_vck5000_fixed_point.sh

with the following settings:
- `FPGA`: (u280|vck)
- `TARGET`: (hw|hw_emu|sw_emu)
- `FP_TYPE`: (fixed_point|floating_point)
- `KERNEL_TYPE`: single or multi-CU (single|multi)
- `reps`: number of elements e.g, `reps=10000000`
- `number_of_runs`: number of runs, to average runtime over
- `number_cus`: compute units, default is 1 if `KERNEL_TYPE=single`
- `bitstreams`: list of bitstreams to run

The kernels write run parameters and runtime, power draw and energy to a .csv file in the created output/ subdirectory in the top-level project dir. Run with:
```
cd run/
nohup ./run_u280_floating_point.sh &> run_u280_floating_point.log001 &
```

## Plot results

Combine the output/runtime_u280_fixed_point.csv and output/runtime_u280_floating_point.csv results into a single file. 
```
cd output/
cat runtime_u280_fixed_point.csv >> runtime_u280.csv
cat runtime_u280_floating_point.csv >> runtime_u280.csv
```

The plot/main.py will get the resource utilisation from csynth and linking reports in the reference_files_* directories created during kernel compilation and linking, using the submodule `vitis_data`, and writes the collected resource utilisation stats to a single location as .csv file before plots and visualisations are generated.

Call the plot.sh script in the [plot/](plot/) subdirectory to generate diagrams. Alternatively:
```
python -m vitis_microbench.plot.main $FPGA $TARGET $KERNEL_TYPE $KERNEL_NAME
```
