import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re

def plot_grouped_boxplots_dtype_ops(df: pd.DataFrame, fpga: str, y_key: str, title: str, y_label: str):
    # Create a grouped boxplot
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='dtype_op', y=y_key, hue='impl', data=df, showmeans=True)

    # Set plot title and labels
    plt.title(title)
    plt.xlabel('Operation Implementation (dtype_op)')
    plt.ylabel(y_label)

    # Display the legend
    plt.legend(title='Implementation (impl)')

    # Show the plot
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(f"boxplots_{fpga}_dtype_op_{y_key}.pdf", format='pdf')

def plot_grouped_boxplots(df: pd.DataFrame, fpga: str):
    # Create a grouped boxplot
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='op_impl', y='execute_ms', hue='dtype', data=df, showmeans=True)

    # Set plot title and labels
    plt.title('Execution Time Boxplots Grouped by "dtype" with "op_impl" as X-axis')
    plt.xlabel('Operation Implementation (op_impl)')
    plt.ylabel('Execution Time (ms)')

    # Display the legend
    plt.legend(title='Data Type (dtype)')

    # Show the plot
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(f"boxplots_{fpga}.pdf", format='pdf')


def plot_grouped_bars(pivot_data: pd.DataFrame, ylabel: str, title: str, ylim: list, output_file: str):
    # Pivot data to format suitable for grouped bar chart
    #pivot_data = data.pivot(index='op_impl', columns='dtype', values='execute_ms')

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))

    # Number of groups and number of bars per group
    n_groups = len(pivot_data)
    bar_width = 0.2  # Width of individual bars
    index = np.arange(n_groups)  # Position of groups on x-axis

    # Plot bars for each dtype
    for i, dtype in enumerate(pivot_data.columns):
        ax.bar(index + i * bar_width, pivot_data[dtype], bar_width, label=dtype)

    # Add labels, title, and legend
    ax.set_xlabel('Operation (op)')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(index + bar_width * (len(pivot_data.columns) - 1) / 2)
    ax.set_xticklabels(pivot_data.index)
    ax.legend(title="Data Type")
    #ax.set_ylim()
    if 0 != len(ylim):
        ax.set_ylim(ylim)
    
    #pivot_power = data.pivot(index='op_impl', columns='dtype', values='power_w')
    #print(pivot_power.head(50))
    #ax2 = plt.twinx()
    #ax2.plot(data["op_impl"], data["power_w"], label="Power (W)")
    #ax2.set_ylim(24,25)
    #ax2.set_ylabel("Power (W)")
    
    # Display the plot
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(output_file, format='pdf')
    #plt.show()
    
def gen_bitstream(bitstream:str):
    #vck5000/dadd_fabric.hw.xclbin
    pattern="([a-z]*_[a-z]*)(?:.hw.xclbin)"
    match=re.search(pattern, bitstream)
    if match is None:
        exit(f"No bitstream found in string: {bitstream}")
    return match.group(0)

def gen_dtype(bitstream: str):
    first_char = bitstream[0]
    if first_char == "h":
        return "half"
    elif first_char == "d":
        return "double"
    elif first_char == "f":
        return "float"
    else:
        exit(f"data type could not be found in bitstream {bitstream}")

def gen_impl(bitstream: str):
    return bitstream.split("_")[1][:-10]

def gen_op(bitstream: str):
    return bitstream.split("_")[0][1:]

def gen_dtype_op(dtype: str, op: str):
    return dtype[0] + op

def add_cols(df: pd.DataFrame) -> pd.DataFrame:
    df["bitstream"] = df.apply(lambda row: gen_bitstream(row.bitstream), axis=1)
    df["dtype"] = df.apply(lambda row: gen_dtype(row.bitstream), axis=1)
    df["impl"] = df.apply(lambda row: gen_impl(row.bitstream), axis=1)
    df["op"] = df.apply(lambda row: gen_op(row.bitstream), axis=1)
    df["op_impl"] = df["op"] + "_" + df["impl"]
    df["dtype_op"] = df.apply(lambda row: gen_dtype_op(row.bitstream, row.op), axis=1)
    return df

def average(df: pd.DataFrame) -> pd.DataFrame:
    cols = list(df.columns.values)
    df_avg = pd.DataFrame(columns=cols)

    for bitstream in df["bitstream"].unique():
        df_per_bitstream = df[df["bitstream"]==bitstream]
        bitstream_name_wo_dir = gen_bitstream(bitstream)

        run_stats_power = df_per_bitstream["power_w"].describe()
        run_stats_exec = df_per_bitstream["execute_ms"].describe()
        
        run_stats_power.to_csv(f"run_stats/power_{bitstream_name_wo_dir}", float_format='%.3f')
        run_stats_exec.to_csv(f"run_stats/exec_{bitstream_name_wo_dir}", float_format='%.3f')

        bitstream_avg = df_per_bitstream.mean(numeric_only=True, axis=0)
        bitstream_avg["bitstream"]=bitstream
        # concat series to new df
        df_avg = pd.concat([df_avg, bitstream_avg.to_frame().T])

    return df_avg

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", type=str, help="csv_file with x runs to average over")

    args = parser.parse_args()
    csv_file = args.csv_file

    df = pd.read_csv(csv_file)
    
    df_avg = average(df)
    df_avg = add_cols(df_avg)
    df_avg.to_csv("runtime_avg.csv", index=False, float_format='%.3f')
    
    pivot_data_exec = df_avg.pivot(index='op_impl', columns='dtype', values='execute_ms')
    pivot_data_power = df_avg.pivot(index='op_impl', columns='dtype', values='power_w')
   
    print("############### exec")
    print(pivot_data_exec)
    print("############### power")
    print(pivot_data_power)

    ylim_u280=[33.5,33.7]
    ylim_vck5000=[33.40,33.42]

    plot_grouped_bars(pivot_data_exec, ylabel='Runtime (ms)', title='Execution Time by Operation and Data Type', ylim=ylim_vck5000, output_file='plot_runtime.pdf')
    plot_grouped_bars(pivot_data_power, ylabel='Power (W)', title='Avg. Power by Operation and Data Type', ylim=[24,26], output_file='plot_power.pdf')

    df_raw=pd.read_csv("/home/nx08/nx08/markkfpga/vitis_microbench/output/runtime.csv")
    df_raw = add_cols(df_raw)
    
    df_raw_u280=pd.read_csv("/home/nx08/nx08/markkfpga/vitis_microbench/output/u280/runtime.csv")
    df=add_cols(df_raw_u280)

    plot_grouped_boxplots(df_raw_u280, fpga="u280")
    plot_grouped_boxplots(df_raw, fpga="vck5000")

    plot_grouped_boxplots_dtype_ops(df_raw_u280, fpga="u280", y_key="execute_ms", title='Execution Time Boxplots Grouped by "impl" with "dtype_op" as X-axis', y_label='Execution Time (ms)')
    plot_grouped_boxplots_dtype_ops(df_raw, fpga="vck5000", y_key="execute_ms", title='Execution Time Boxplots Grouped by "impl" with "dtype_op" as X-axis', y_label='Execution Time (ms)')

    plot_grouped_boxplots_dtype_ops(df_raw_u280, fpga="u280", y_key="power_w", title='Avg Power draw Boxplots Grouped by "impl" with "dtype_op" as X-axis', y_label='Avg power draw (W)')
    #plot_grouped_boxplots_dtype_ops(df_raw, fpga="vck5000", y_key="power_w", title='Execution Time Boxplots Grouped by "impl" with "dtype_op" as X-axis', y_label='Execution Time (ms)')
