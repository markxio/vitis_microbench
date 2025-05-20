import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import os
import re
import json

def pprint(mydict: dict):
    print(json.dumps(mydict, sort_keys=True, indent=4))

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
    regex_fixed_point="[a-z]+_\d{1,2}_\d{1,2}_[a-z]+\.hw\.xclbin"
    # dadd_fabric.hw.xclbin
    regex_floating_point="[a-z]+_[a-z]+\.hw\.xclbin"
    
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

def plot(df: pd.DataFrame, target_dir: str, target_filename_prefix: str, col: str, yerr: str, ylabel: str):
    # Pivot the data for grouped bar chart
    df_pivot = df.pivot_table(index=['op', 'dtype'], values=[col, yerr], columns='impl')

    # Plot the grouped bar chart with error bars
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = df_pivot[col].plot(kind='bar', yerr=df_pivot[yerr], capsize=5, ax=ax, width=0.8)

    plt.xlabel("DType and Operation")
    plt.ylabel(ylabel)
    #plt.title("Grouped Bar Chart of avg_power_w by dtype and op with Standard Deviation")
    plt.xticks(rotation=45, ha='right')
    #plt.legend(title="Implementation")
    plt.legend()
    ax.set_ylim([33.4,33.9])
    plt.tight_layout()
    plt.savefig(f"{target_dir}/{target_filename_prefix}_{col}.pdf", format='pdf')
    #plt.show()

def plot_subfigs(df: pd.DataFrame, target_dir: str, target_filename_prefix: str, col: str, yerr: str, ylabel: str, ylim=list()):
    # Get unique operations
    unique_ops = df["op"].unique()
    num_ops = len(unique_ops)

    cols=3
    rows=int(num_ops/3);
    # Determine grid size (3x3)
    if 0 != num_ops % 3:
        rows+=1
   
    figsize=(cols*5,rows*4)

    fig, axes = plt.subplots(nrows=rows, ncols=cols, figsize=figsize)  # Adjust size as needed

    # Flatten the 3x3 grid of axes
    axes = axes.flatten()

    for i, (ax, op) in enumerate(zip(axes, unique_ops)):
        # Filter data for the specific operation
        df_op = df[df["op"] == op]

        # Pivot the data for grouped bar chart
        df_pivot = df_op.pivot_table(index=['dtype'], values=[col, yerr], columns='impl')
         
        # Plot the grouped bar chart with error bars
        df_pivot[col].plot(kind='bar', yerr=df_pivot[yerr], sharey=True, capsize=0, ax=ax, width=0.8)
        #plt.text(.01, .99, 'matplotlib', ha='left', va='top', transform=ax.transAxes)
        ax.set_title(f"{op}")
        ax.set_ylabel(ylabel)
        ax.set_xlabel("")
        ax.legend()
        ax.tick_params(axis='x', rotation=0)
        ax.grid(axis="y")
        #print(df_pivot[yerr].values)
        #for j, bar in enumerate(ax.patches):
        #    height = bar.get_height()
        #    error = df_pivot[yerr].values  # Get the standard error for this bar
        #    label_position = height + error / 2  # Add half of the error to the bar height for label position
    
        #    ax.text(bar.get_x() + bar.get_width() / 2, label_position, f'{height:.2f}', ha='center', va='bottom', fontsize=10)
         
    #ylim=[y_mini-2,y_max+2]
    for i, (ax, op) in enumerate(zip(axes, unique_ops)):
        #ax.bar_label(, fmt='%.2f')
        if len(ylim) > 0:
            ax.set_ylim(ylim)

    # Hide any unused subplots (if fewer than 9 ops exist)
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    ops_str = "_".join(unique_ops)
    #print(ops_str)
    #print(df)
    plt.tight_layout()
    plt.savefig(f"{target_dir}/{target_filename_prefix}_{col}_subfigs_{ops_str}.pdf", format='pdf')

# TODO: this is with mean and stderr as labels at the top end of the chart
def plot_subfigs_gpt(df: pd.DataFrame, target_dir: str, target_filename_prefix: str, col: str, yerr: str, ylabel: str, ylim=list()):
    # Get unique operations
    unique_ops = df["op"].unique()
    num_ops = len(unique_ops)

    cols=3
    rows=int(num_ops/3);
    # Determine grid size (3x3)
    if 0 != num_ops % 3:
        rows+=1

    fig, axes = plt.subplots(nrows=rows, ncols=cols, figsize=(16, 12))  # Adjust size as needed

    # Flatten the 3x3 grid of axes
    axes = axes.flatten()

    for i, (ax, op) in enumerate(zip(axes, unique_ops)):
        # Filter data for the specific operation
        df_op = df[df["op"] == op]

        # Pivot the data for grouped bar chart
        df_pivot = df_op.pivot_table(index=['dtype'], values=[col, yerr], columns='impl')

        # Plot the grouped bar chart with error bars
        bars = df_pivot[col].plot(kind='bar', yerr=df_pivot[yerr], sharey=True, capsize=0, ax=ax, width=0.8)
       
        #print(df_pivot[yerr])
        myerrors=[]
        bars_per_group=[]
        for implementation in df_op["impl"].unique():
            bars_per_group_count=0
            for datatype in df_op["dtype"].unique():
                myerr = df_pivot[yerr].loc[datatype, implementation]
                if myerr > 0.00:
                    myerrors.append(myerr) 
                    bars_per_group_count+=1
            bars_per_group.append(bars_per_group_count)

        # Add value labels above each bar
        counter=0
        height_current=36.1
        for patch in bars.patches:
            height = patch.get_height()
            if height > 0.0:
                   
                ax.text(patch.get_x() + patch.get_width() / 2, height, f'{height:.2f}±{myerrors[counter]:.2f}', ha='center', fontsize="medium")#, va='bottom')
                #ax.text(patch.get_x() + patch.get_width() / 2, 36.1, f'±{myerrors[counter]:.2f}', ha='center', fontsize="x-small")#, va='bottom')
                counter+=1
        #print(counter)
        exit()
        # Add yerr labels below each bar label
        #bar_index = 0  # Track which bar (dtype/impl combination) we are processing
        #for col_idx, col in enumerate(df_pivot.columns.levels[0]):  # Loop through the implementations (impl)
        #    for dtype_index, dtype in enumerate(df_pivot.index):  # Loop through the data types (dtype)
        #        # Get the corresponding yerr value for the bar
        #        yerr_value = df_pivot[yerr].iloc[dtype_index, col_idx]
        #        
        #        # Get the position of the current bar in the plot
        #        bar = bars[bar_index]
        #        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() - yerr_value - 0.05, 
        #                f'±{yerr_value:.2f}', ha='center', va='top', fontsize=9)

        #        bar_index += 1

        ax.set_title(f"{op}", y=1.0, pad=-14)
        ax.set_ylabel(ylabel)
        ax.set_xlabel("")
        ax.legend()
        ax.tick_params(axis='x', rotation=0)
        ax.grid(axis="y")

    for i, (ax, op) in enumerate(zip(axes, unique_ops)):
        if len(ylim) > 0:
            ax.set_ylim(ylim)

    # Hide any unused subplots (if fewer than 9 ops exist)
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.savefig(f"{target_dir}/{target_filename_prefix}_{col}_subfigs.pdf", format='pdf')

def map_min(tab: pd.DataFrame):
    min_map = {}
    op_datatype_unique = tab[["op", "datatype"]].drop_duplicates()
    for idx, row in op_datatype_unique.iterrows():
        impls = tab[tab["op"]==row["op"]]
        impls = impls[impls["datatype"]==row["datatype"]]
        min_map[f"{row['op']}_{row['datatype']}_runtime"] = impls["runtime"].min()
        min_map[f"{row['op']}_{row['datatype']}_power"] = impls["power"].min()
        min_map[f"{row['op']}_{row['datatype']}_energy"] = impls["energy"].min()
    #pprint(min_map)
    return min_map

def plot_prep(csv_file: str, target_dir: str, target_filename_prefix: str):
    data = pd.read_csv(csv_file)
    data["op"] = data.apply(lambda row: gen_op(row.bitstream), axis=1)
    data["dtype"] = data.apply(lambda row: gen_dtype(row.bitstream), axis=1)
    data["impl"] = data.apply(lambda row: gen_impl(row.bitstream), axis=1)
   
    #runtime = df[["op", "dtype", "impl", "total_runtime_ms"]]
    runtime = data[["op", "dtype", "impl", "execute_ms"]].copy(deep=True)
    power = data[["op", "dtype", "impl", "power_w"]].copy(deep=True)
    energy = data[["op", "dtype", "impl", "energy_j"]].copy(deep=True)
    
    #print(runtime.head(100))

    #runtime_grouped = average_with_std(runtime, col="total_runtime_ms")
    runtime_grouped = average_with_std(runtime, col="execute_ms")
    power_grouped = average_with_std(power, col="power_w")
    energy_grouped = average_with_std(energy, col="energy_j")

    #runtime_grouped[["op", "dtype", "impl", "avg_execute_ms", "std_execute_ms"]].sort_values(["op", "dtype"], ascending=[True, True]).to_csv(f"{target_dir}/{target_filename_prefix}_runtime.csv", float_format="%.3f")
    #power_grouped[["op", "dtype", "impl", "avg_power_w", "std_power_w"]].sort_values(["op", "dtype"], ascending=[True, True]).to_csv(f"{target_dir}/{target_filename_prefix}_power.csv", float_format="%.3f")
    #energy_grouped[["op", "dtype", "impl", "avg_energy_j", "std_energy_j"]].sort_values(["op", "dtype"], ascending=[True, True]).to_csv(f"{target_dir}/{target_filename_prefix}_energy.csv", float_format="%.3f")

    ###############################################
    # generate latex overview table start
    # incl runtime, power, energy, resutil
    ###############################################
    # merge runtime, power, energy and resutil
    # per grouped df, join the two data columsn eg, avg_execute_ms + std_execute_ms => 33.333+-0.032
    tab = runtime_grouped[["op", "dtype", "impl"]].copy(deep=True)
    tab["runtime_str"] = runtime_grouped["avg_execute_ms"].apply(lambda x: '{0:.3f}'.format(x))
    tab["power_str"] = power_grouped["avg_power_w"].apply(lambda x: '{0:.3f}'.format(x))
    tab["energy_str"] = energy_grouped["avg_energy_j"].apply(lambda x: '{0:.3f}'.format(x))

    tab["runtime_std_str"] = runtime_grouped["std_execute_ms"].apply(lambda x: '{0:.3f}'.format(x))
    tab["power_std_str"] = power_grouped["std_power_w"].apply(lambda x: '{0:.3f}'.format(x))
    tab["energy_std_str"] = energy_grouped["std_energy_j"].apply(lambda x: '{0:.3f}'.format(x))

    #tab["runtime"] = runtime_grouped["avg_execute_ms"].round(3).astype(str) + "+-" + runtime_grouped["std_execute_ms"].round(3).astype(str) 
    #tab["power"] = power_grouped["avg_power_w"].round(3).astype(str) + "+-" + power_grouped["std_power_w"].round(3).astype(str) 
    #tab["energy"] = energy_grouped["avg_energy_j"].round(3).astype(str) + "+-" + energy_grouped["std_energy_j"].round(3).astype(str) 
   
    tab["runtime"] = tab["runtime_str"] + "+-" + tab["runtime_std_str"] 
    tab["power"] = tab["power_str"] + "+-" + tab["power_std_str"] 
    tab["energy"] = tab["energy_str"] + "+-" + tab["energy_std_str"] 
    
    tab = tab.drop(columns=["runtime_str", "runtime_std_str", "power_str", "power_std_str", "energy_str", "energy_std_str"])
    tab = tab.sort_values(["op", "dtype"], ascending=[True, True])

    fpga="vck"
    kernel_type="single_kernel"
    precision_type="floating_point"
    if "u280" in csv_file:
        fpga="u280"
    if "multi-kernel" in csv_file:
        kernel_type="multi_kernel"
    if "fixed_point" in csv_file:
        precision_type="fixed_point"
    
    resutil = pd.read_csv(f"{fpga}_resutil_{kernel_type}_{precision_type}.csv")
    #resutil = resutil.sort_values(["op", "dtype"], ascending=[True, True])
    # op,dtype,impl,LUT,LUTAsMem,REG,BRAM,URAM,DSP
    resutil["LUT"] = resutil["LUT"].round(3)
    resutil["LUTAsMem"] = resutil["LUTAsMem"].round(3)
    resutil["REG"] = resutil["REG"].round(3)
    resutil["BRAM"] = resutil["BRAM"].round(3)
    resutil["DSP"] = resutil["DSP"].round(3)
    tab = tab.join(resutil[["op","dtype","impl","LUT","LUTAsMem","REG","BRAM","DSP"]].set_index(["op", "impl", "dtype"]), on=["op", "impl", "dtype"])
    tab_csv = f"{target_dir}/total_data_{target_filename_prefix}.csv"
    print(f"tab_csv: {tab_csv}")
    tab.to_csv(tab_csv, index=False, float_format="%.3f")

    resutil_stats = tab.copy(deep=True)
    resutil_stats["total"] = tab["LUT"]+tab["LUTAsMem"]+tab["REG"]+tab["BRAM"]+tab["DSP"]
    resutil_stats.to_csv(f"{target_dir}/total_resutil_{target_filename_prefix}.csv", index=False, float_format="%.3f")

    ###############################################
    # generate speedup multi over single (if multi) 
    # incl runtime, power, energy, resutil
    ###############################################

    if "multi-kernel" in csv_file:
        # get single-kernel tab
        target_dir_single=target_dir.replace("multi-kernel", "single-kernel")
        target_filename_prefix_single=target_filename_prefix.replace("multi-kernel", "single-kernel")

        tab_single_csv = f"{target_dir_single}/total_data_{target_filename_prefix_single}.csv"
        print(f"tab_single_csv: {tab_single_csv}")
        tab_single = pd.read_csv(tab_single_csv)
        tab_single["runtime"] = tab_single["runtime"].apply(lambda x: float(x[:6]))
        tab_single["power"] = tab_single["power"].apply(lambda x: float(x[:6]))
        tab_single["energy"] = tab_single["energy"].apply(lambda x: float(x[:5]))

        #print(tab_single.head(100))
        #print("##########################")

        #tab_multi=tab.copy(deep=True)
        tab_multi = pd.read_csv(tab_csv)
        tab_multi["runtime"] = tab_multi["runtime"].apply(lambda x: float(x[:6]))
        tab_multi["power"] = tab_multi["power"].apply(lambda x: float(x[:6]))
        tab_multi["energy"] = tab_multi["energy"].apply(lambda x: float(x[:5]))

        #print(tab_multi.head(100))
        #print("##########################")
    
        tab_multi["runtime"] = tab_multi["runtime"] / tab_single["runtime"] -1
        tab_multi["power"] = tab_multi["power"] / tab_single["power"] -1
        tab_multi["energy"] = tab_multi["energy"] / tab_single["energy"] -1

        #print(tab_multi.head(100))
        #print("##########################")       

        tab_multi["total_multi"] = tab_multi["LUT"]+tab_multi["LUTAsMem"]+tab_multi["REG"]+tab_multi["BRAM"]+tab_multi["DSP"]
        tab_multi["total_single"] = tab_single["LUT"]+tab_single["LUTAsMem"]+tab_single["REG"]+tab_single["BRAM"]+tab_single["DSP"]
 
        tab_multi["LUT"] = tab_multi["LUT"] / tab_single["LUT"]
        tab_multi["LUTAsMem"] = tab_multi["LUTAsMem"] / tab_single["LUTAsMem"]
        tab_multi["REG"] = tab_multi["REG"] / tab_single["REG"]
        tab_multi["BRAM"] = tab_multi["BRAM"] / tab_single["BRAM"]
        tab_multi["DSP"] = tab_multi["DSP"] / tab_single["DSP"]
   
        tab_multi_csv = f"{target_dir}/total_speedup_{target_filename_prefix}.csv" 
        print(f"tab_multi_csv: {tab_multi_csv}")
        tab_multi.to_csv(tab_multi_csv, index=False, float_format="%.4f")
    ######

    tab2 = runtime_grouped[["op", "dtype", "impl"]].copy(deep=True) 
    tab2 = tab2.rename(columns={"dtype": "datatype"})
    
    tab2["runtime"] = runtime_grouped["avg_execute_ms"]
    tab2["power"] = power_grouped["avg_power_w"]
    tab2["energy"] = energy_grouped["avg_energy_j"]
    
    tab2["runtime_std"] = runtime_grouped["std_execute_ms"]
    tab2["power_std"] = power_grouped["std_power_w"]
    tab2["energy_std"] = energy_grouped["std_energy_j"]

    tab2["runtime_rsd"] = tab2["runtime_std"] / tab2["runtime"]
    tab2["power_rsd"] = tab2["power_std"] / tab2["power"]
    tab2["energy_rsd"] = tab2["energy_std"] / tab2["energy"]

    # 1) identify best performing impl (across op and datatype) - runtime, power, energy
    # 2) compare 1) across ops
    min_map = map_min(tab2)
    tab2["runtime_normed"] = tab2.apply(lambda x: (x.runtime / min_map[f"{x.op}_{x.datatype}_runtime"]), axis=1) 
    tab2["power_normed"] = tab2.apply(lambda x: (x.power / min_map[f"{x.op}_{x.datatype}_power"]), axis=1) 
    tab2["energy_normed"] = tab2.apply(lambda x: (x.energy / min_map[f"{x.op}_{x.datatype}_energy"]), axis=1)
    
    # now select from tab2 in right order of cols so we're ready to write to csv
    tab3 = tab2[["op", "datatype", "impl", "runtime", "runtime_normed", "runtime_std", "runtime_rsd", "power", "power_normed", "power_std", "power_rsd", "energy", "energy_normed", "energy_std", "energy_rsd"]]
    tab3 = tab3.sort_values(["op", "datatype"], ascending=[True, True])
    tab3.to_csv(f"{target_dir}/normalised_total_data_{target_filename_prefix}.csv", index=False, float_format="%.4f")

    ###############################################
    # 
    ###############################################

    ylim_runtime = gen_ylim(runtime_grouped, col="execute_ms")
    ylim_power = gen_ylim(power_grouped, col="power_w")
    ylim_energy = gen_ylim(energy_grouped, col="energy_j")

    #filters = [["add", "mul", "sub"]]
    #if "floating_point" in csv_file:
    filters = [["add", "mul", "sub"], ["recip", "rsqrt", "sqrt"], ["div", "exp", "log"]]
    #elif "fixed-point" in csv_file:
    #    filters = [["add", "mul", "sub"]]

    for myfilter in filters:
       #print(csv_file)
       df = data[data["op"].isin(myfilter)].copy(deep=True)

       #runtime = df[["op", "dtype", "impl", "total_runtime_ms"]]
       runtime = df[["op", "dtype", "impl", "execute_ms"]]
       power = df[["op", "dtype", "impl", "power_w"]]
       energy = df[["op", "dtype", "impl", "energy_j"]]
       
       #print(runtime.head(100))

       #runtime_grouped = average_with_std(runtime, col="total_runtime_ms")
       runtime_grouped = average_with_std(runtime, col="execute_ms")
       power_grouped = average_with_std(power, col="power_w")
       energy_grouped = average_with_std(energy, col="energy_j")

       #test = runtime[runtime["op"]=="mul"]
       #test = test[test["dtype"]=="float"]
       #test = test[test["impl"]=="maxdsp"]
       #print(test.sort_values("execute_ms", axis=0,ascending=False))
       
       #print(runtime_grouped)
       #print(power_grouped)
       #print(energy_grouped)

       #ylim_runtime = gen_ylim(runtime_grouped, col="execute_ms")
       #ylim_power = gen_ylim(power_grouped, col="power_w")
       #ylim_energy = gen_ylim(energy_grouped, col="energy_j")

       #print(ylim_runtime)
       #print(ylim_power)
       #print(ylim_energy)

       #plot(runtime_grouped, col='avg_total_runtime_ms', yerr='std_total_runtime_ms', ylabel="Total Runtime (ms)")
       plot_subfigs(runtime_grouped.copy(deep=True), target_dir, target_filename_prefix, col='avg_execute_ms', yerr='std_execute_ms', ylabel="Kernel Runtime (ms)", ylim=ylim_runtime) #[33.4,33.9])
       #plot(runtime_grouped, col='avg_execute_ms', yerr='std_execute_ms', ylabel="Kernel Runtime (ms)")
       
       plot_subfigs(power_grouped.copy(deep=True), target_dir, target_filename_prefix, col='avg_power_w', yerr='std_power_w', ylabel="Average Power (W)", ylim=ylim_power) #ylim=[23.0, 26.5])
       #plot(power_grouped, col='avg_power_w', yerr='std_power_w', ylabel="Average Power (W)")
       
       plot_subfigs(energy_grouped.copy(deep=True), target_dir, target_filename_prefix, col='avg_energy_j', yerr='std_energy_j', ylabel="Energy (J)", ylim=ylim_energy) #ylim=[0.79,0.86])
       #plot(energy_grouped, col='avg_energy_j', yerr='std_energy_j', ylabel="Energy (J)")

if __name__=="__main__":
    csv_files = [ 
            #"sleep_2_sec_between_runs/single-kernel/runtime_u280_floating_point.csv",
            #"sleep_2_sec_between_runs/single-kernel/runtime_u280_fixed_point.csv",
            #"sleep_2_sec_between_runs/multi-kernel/runtime_u280_floating_point.csv",
            #"sleep_2_sec_between_runs/multi-kernel/runtime_u280_fixed_point.csv"
            #"../output/runtime_u280_fixed_point.csv",
            #"../output/runtime_u280_floating_point.csv"
            "../output/runtime_u280_both.csv"
            ]

    for f in csv_files:
        fpga="vck"
        if "u280" in f:
            fpga="u280"
        splits=f.split("/")
        #kernel_type=splits[len(splits)-2] # single/multi
        kernel_type="single_kernel"
        csv_name=splits[len(splits)-1][:-4] # without .csv
        tdir=f"plotted/{fpga}/{kernel_type}"
        os.system(f"mkdir -p {tdir}")

        plot_prep(f, target_dir=tdir, target_filename_prefix=csv_name)
