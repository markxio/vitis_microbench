#!/bin/python

import argparse
import os
from get_resource_utilisation import write_csv_stats
from plot_resource_utilisation import plot_resource_utilisation
from plot_profile import plot_profile

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fpga", type=str, help="FPGA target (u280|vck)")
    parser.add_argument("target", type=str, help="Build target (hw|hw_emu|sw_emu)")
    parser.add_argument("kernel_type", type=str, help="Single or multi CU (single|multi)")
    parser.add_argument("kernel_name", type=str, help="Name of the kernel e.g. krnl_bench")
  
    args = parser.parse_args()
    fpga = args.fpga
    target = args.target
    kernel_type = args.kernel_type
    kernel_name = args.kernel_name
    
    # resource utilisation
    results_dir = f"results/resutil/{fpga}/{target}/{kernel_type}/{kernel_name}"
    os.system(f"mkdir -p {results_dir}")
    write_csv_stats(fpga, target, kernel_type, kernel_name, tdir=results_dir)
    plot_resource_utilisation(csv_file=f"{results_dir}/linked.csv", fpga=fpga, kernel_type=kernel_type)

    # profile: runtime, power, energy
    results_dir = f"results/profile/{fpga}/{target}/{kernel_type}/{kernel_name}"
    os.system(f"mkdir -p {results_dir}")
    plot_profile(csv_file=f"../output/runtime_{fpga}.csv", tdir=f"results/profile/{fpga}/{target}/{kernel_type}/{kernel_name}")

