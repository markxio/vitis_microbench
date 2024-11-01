import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_grouped_bars(data: pd.DataFrame):
    # Pivot data to format suitable for grouped bar chart
    #pivot_data = data.pivot(index='op_impl', columns='dtype', values='execute_ms')
    pivot_data = data.pivot(index='op_impl', columns='dtype', values='power_w')
    print(pivot_data.head(50))
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
    #ax.set_ylabel('Execution Time (ms)')
    ax.set_ylabel('Power (W)')
    #ax.set_title('Execution Time by Operation and Data Type')
    ax.set_title('Avg. Power by Operation and Data Type')
    ax.set_xticks(index + bar_width * (len(pivot_data.columns) - 1) / 2)
    ax.set_xticklabels(pivot_data.index)
    ax.legend(title="Data Type")
    #ax.set_ylim([33.5,33.7])
    ax.set_ylim([24,26])
    
    #pivot_power = data.pivot(index='op_impl', columns='dtype', values='power_w')
    #print(pivot_power.head(50))
    #ax2 = plt.twinx()
    #ax2.plot(data["op_impl"], data["power_w"], label="Power (W)")
    #ax2.set_ylim(24,25)
    #ax2.set_ylabel("Power (W)")
    
    # Display the plot
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('plot_power.pdf', format='pdf')
    #plt.show()
    
def gen_bitstream(bitstream:str):
    return bitstream[4:]

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

def add_cols(df: pd.DataFrame) -> pd.DataFrame:
    df["bitstream"] = df.apply(lambda row: gen_bitstream(row.bitstream), axis=1)
    df["dtype"] = df.apply(lambda row: gen_dtype(row.bitstream), axis=1)
    df["impl"] = df.apply(lambda row: gen_impl(row.bitstream), axis=1)
    df["op"] = df.apply(lambda row: gen_op(row.bitstream), axis=1)
    df["op_impl"] = df["op"] + "_" + df["impl"]
    return df

def average(df: pd.DataFrame) -> pd.DataFrame:
    cols = list(df.columns.values)
    df_avg = pd.DataFrame(columns=cols)

    for bitstream in df["bitstream"].unique():
        df_per_bitstream = df[df["bitstream"]==bitstream]
        bitstream_name_wo_dir = bitstream[4:]
        print(bitstream_name_wo_dir)

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
    
    plot_grouped_bars(df_avg)
