import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import os
import re
import json

def pprint(mydict: dict):
    print(json.dumps(mydict, sort_keys=True, indent=4))

def diff_int_vs_frac_bits(op: str, impl: str, bits: int, input_in_percent: bool, col: str, df: pd.DataFrame):
    filtered = df[df["op"]==op]
    filtered = filtered[filtered["impl"]==impl]
    filtered = filtered[filtered["datatype"].str.startswith(bits)]
    metric = filtered[col]
    metric_min = metric.astype("float").min()
    metric_max = metric.astype("float").max()
    if input_in_percent:
        diff = metric_max-metric_min
    else:
        diff = (metric_max-metric_min)/metric_min
        diff = diff*100
    if metric_min == 0:
        return 0.00
    return diff

def diff_across_impls(op: str, dtype: str, input_in_percent: bool, col: str, df: pd.DataFrame):
    filtered = df[df["op"]==op]
    filtered = filtered[filtered["datatype"]==dtype]
    metric = filtered[col]
    metric_min = metric.astype("float").min()
    metric_max = metric.astype("float").max()
    diff = 0.0
    if input_in_percent:
        diff = metric_max-metric_min
    else:
        diff = (metric_max-metric_min)/metric_min
        diff = diff*100
    if metric_min == 0:
        return 0.00
    return diff

def norm_bits_scaling(op: str, impl: str, base_dtype: str, col: str, val: float, df: pd.DataFrame):
    filtered = df[df["op"]==op]
    filtered = filtered[filtered["impl"]==impl]
    filtered = filtered[filtered["datatype"]==base_dtype]
    base_val = filtered[col].astype("float").max() # only one val in series
    if float(base_val) == 0.0:
        return 0.0
    return val / float(base_val)

def gen_kernel_type(bitstream: str) -> str:
    kernel_type = "single-kernel"
    if "_multi" in bitstream:
        kernel_type = "multi-kernel"
    return kernel_type

def gen_op(bitstream: str) -> str:
    # mydir/fadd_fulldsp.hw.xclbin
    # mydir/add_64_12_dsp.hw.xclbin
    splits = bitstream.split("/")
    lastpart = splits[len(splits)-1] 
    splits = lastpart.split("_")

    if re.search("\d", lastpart):
        # fixed point
        return splits[0]
    else:
        # floating-point
        return splits[0][1:]

def gen_dtype(bitstream: str) -> str:
    # div_8_4_fabric.hw.xclbin
    regex_fixed_point="[a-z]+_\d{1,2}_\d{1,2}_[a-z]+(\.hw\.xclbin|_single)"
    # dadd_fabric.hw.xclbin
    regex_floating_point="[a-z]+_[a-z]+(\.hw\.xclbin|_single)"
    
    matches_fixed_point = re.findall(regex_fixed_point, bitstream)
    matches_floating_point = re.findall(regex_floating_point, bitstream)
    
    isFixedPoint=False
    isFloatingPoint=False
    if len(matches_fixed_point) > 0:
        isFixedPoint=True
    elif len(matches_floating_point) > 0:
        isFloatingPoint=True
    else:
        raise ValueError('gen_dtype: Couldnt detect fixed-point or floating-point')

    splits = bitstream.split("/")
    c = splits[len(splits)-1][0]
    if isFloatingPoint:
        if c == "d":
            return "double"
        elif c == "f":
            return "float"
        elif c == "h":
            return "half"
        else:
            raise ValueError('gen_dtype: Detected floating-point but couldnt detect dtype')
    
    if isFixedPoint:
        # add_64_12_dsp.hw.xclbin
        lastpart = splits[len(splits)-1]
    
        lastpart = lastpart.replace("8_3", "08_3")
        lastpart = lastpart.replace("8_4", "08_4")

        pattern = "[a-z]+_(\d{1,2}_\d{1,2})"
        matches = re.search(pattern, lastpart)
        if matches:
            dtype_found = matches.group(1)
            #if dtype_found[0]=="0":
            #    return dtype_found[1:]
            return dtype_found
        else:
            raise ValueError('gen_dtype: Detected fixed-point but couldnt detect dtype')

def gen_impl(bitstream: str) -> str:
    # mydir/fadd_fulldsp.hw.xclbin
    # mydir/add_64_12_dsp.hw.xclbin
    splits = bitstream.split("/")
    lastpart = splits[len(splits)-1] 
    splits = lastpart.split("_")

    if re.search("\d", lastpart):
        # fixed point
        return splits[len(splits)-1].split(".")[0]
    else:
        # floating-point
        return bitstream.split("_")[1].split(".")[0]

def gen_ylim(df: pd.DataFrame, col: str) -> list:
    #print(df)
    ymin = df[f"avg_{col}"].min()
    ymax = df[f"avg_{col}"].max()

    yerr_max = df[f"std_{col}"].max()
   
    #print(f"ymin {ymin}, ymax {ymax}, yerr_max {yerr_max}")
    # would be 0.5*yerr but to add padding we use 1.0*yerr
    factor=10.0
    if ymax<2.0:
        factor=1.0
        return [round(ymin-yerr_max, 2), round(ymax+yerr_max, 2)]
    return [math.floor((ymin-0.5*yerr_max)*int(factor)/factor), math.ceil((ymax+0.5*yerr_max)*int(factor)/factor)]

def average_with_std(df: pd.DataFrame, col: str) -> pd.DataFrame:
     # Group by 'impl', 'op', and 'dtype' and compute mean & std
    df_grouped = df.groupby(["impl", "op", "dtype"])[col].agg(['mean', 'std']).reset_index()
    # Rename columns
    df_grouped.columns = ['impl', 'op', 'dtype', f"avg_{col}", f"std_{col}"]
    return df_grouped

def rename_fixed_point_names(mystr):
    if "_" in mystr:
        mystr = "<" + mystr.replace("_", ",") + ">"
    return mystr

def plot_subfigs(df: pd.DataFrame, target_dir: str, col: str, yerr: str, ylabel: str, ylim=list()):
    # Get unique operations
    unique_ops = df["op"].unique()
    num_ops = len(unique_ops)

    #cols=3
    cols=1
    rows=int(num_ops/3)
    # Determine grid size (3x3)
    if 0 != num_ops % 3:
        rows+=1
   
    figsize=(cols*5,rows*4)
    fig, ax = plt.subplots(nrows=rows, ncols=cols, figsize=figsize)  # Adjust size as needed

    # Filter data for the specific operation
    df_op = df[df["op"] == unique_ops[0]]

    if "half" not in df_op["dtype"].unique():
        df_data_half = { 
                    "impl": "fabric",
                    "op": unique_ops[0],
                    "dtype": "half",
                    f"{yerr}": 0.0,
                    f"{col}": 0.0
                }
        df_op = df_op._append(df_data_half, ignore_index=True)

    # rename dtypes with underscore (_) to comma (,) separated integers
    # eg. from 64_12 to 64,12
    df_op["dtype"] = df_op["dtype"].apply(lambda x: rename_fixed_point_names(x))

    # Pivot the data for grouped bar chart
    df_pivot = df_op.pivot_table(index=['dtype'], values=[col, yerr], columns='impl')
    
    # Plot the grouped bar chart with error bars
    df_pivot[col].plot(kind='bar', yerr=df_pivot[yerr], sharey=True, capsize=0, ax=ax, width=0.8)
    #plt.text(.01, .99, 'matplotlib', ha='left', va='top', transform=ax.transAxes)
    ax.set_title(f"{unique_ops[0]}")
    ax.set_ylabel(ylabel)
    ax.set_xlabel("")
    if unique_ops[0] == "mul" and col == "avg_execute_ms":
        ax.legend(loc="upper left")
    else:
        ax.legend()
    ax.tick_params(axis='x', rotation=45)
    ax.grid(axis="y")
    #for j, bar in enumerate(ax.patches):
    #    height = bar.get_height()
    #    error = df_pivot[yerr].values  # Get the standard error for this bar
    #    label_position = height + error / 2  # Add half of the error to the bar height for label position

    #    ax.text(bar.get_x() + bar.get_width() / 2, label_position, f'{height:.2f}', ha='center', va='bottom', fontsize=10)
         
    #ylim=[y_mini-2,y_max+2]
    op_has_ylim_map = ["add", "mul", "sub", "div"] # others just use gen_ylim() function 
    col_has_ylim_map = ["avg_execute_ms", "avg_energy_j"] # "avg_power_w"
    ylim_map = {
            "avg_execute_ms": {
                    "add": [4.0,8.0],
                    "mul": [4.0,8.0],
                    "sub": [4.0,8.0],
                    "div": [4.0,8.0] # others just use the gen_ylim() function
                },
            "avg_energy_j": {
                    "add": [0.11,0.20],
                    "mul": [0.11,0.20],
                    "sub": [0.11,0.20],
                    "div": [0.11,0.20] # others just use the gen_ylim() function
                }
            }
    
    if len(ylim) > 0:
        if col in col_has_ylim_map and unique_ops[0] in op_has_ylim_map:
            ylim = ylim_map[col][unique_ops[0]]
        ax.set_ylim(ylim)

    ops_str = "_".join(unique_ops)
    plt.tight_layout()
    plt.savefig(f"{target_dir}/{col}_subfigs_{ops_str}.pdf", format='pdf')

def map_min(tab: pd.DataFrame):
    min_map = {}
    op_datatype_unique = tab[["op", "datatype"]].drop_duplicates()
    for idx, row in op_datatype_unique.iterrows():
        impls = tab[tab["op"]==row["op"]]
        impls = impls[impls["datatype"]==row["datatype"]]
        min_map[f"{row['op']}_{row['datatype']}_runtime"] = impls["runtime"].min()
        min_map[f"{row['op']}_{row['datatype']}_power"] = impls["power"].min()
        min_map[f"{row['op']}_{row['datatype']}_energy"] = impls["energy"].min()
    return min_map

def plot_profile(csv_file: str, target_dir: str):
    data = pd.read_csv(csv_file)
    data["op"] = data.apply(lambda row: gen_op(row.bitstream), axis=1)
    data["dtype"] = data.apply(lambda row: gen_dtype(row.bitstream), axis=1)
    data["impl"] = data.apply(lambda row: gen_impl(row.bitstream), axis=1)
   
    runtime = data[["op", "dtype", "impl", "execute_ms"]].copy(deep=True)
    power = data[["op", "dtype", "impl", "power_w"]].copy(deep=True)
    energy = data[["op", "dtype", "impl", "energy_j"]].copy(deep=True)
    
    runtime_grouped = average_with_std(runtime, col="execute_ms")
    power_grouped = average_with_std(power, col="power_w")
    energy_grouped = average_with_std(energy, col="energy_j")

    ylim_runtime = gen_ylim(runtime_grouped, col="execute_ms")
    ylim_power = gen_ylim(power_grouped, col="power_w")
    ylim_energy = gen_ylim(energy_grouped, col="energy_j")

    filters = [["add"], ["mul"], ["sub"], ["recip"], ["rsqrt"], ["sqrt"], ["div"], ["exp"], ["log"]]
    for myfilter in filters:
       df = data[data["op"].isin(myfilter)].copy(deep=True)

       runtime = df[["op", "dtype", "impl", "execute_ms"]]
       power = df[["op", "dtype", "impl", "power_w"]]
       energy = df[["op", "dtype", "impl", "energy_j"]]
       
       runtime_grouped = average_with_std(runtime, col="execute_ms")
       power_grouped = average_with_std(power, col="power_w")
       energy_grouped = average_with_std(energy, col="energy_j")

       plot_subfigs(runtime_grouped.copy(deep=True), target_dir, col='avg_execute_ms', yerr='std_execute_ms', ylabel="Kernel Runtime (ms)", ylim=ylim_runtime) #[33.4,33.9])
       plot_subfigs(power_grouped.copy(deep=True), target_dir, col='avg_power_w', yerr='std_power_w', ylabel="Average Power (W)", ylim=ylim_power) #ylim=[23.0, 26.5])
       plot_subfigs(energy_grouped.copy(deep=True), target_dir, col='avg_energy_j', yerr='std_energy_j', ylabel="Energy (J)", ylim=ylim_energy) #ylim=[0.79,0.86])