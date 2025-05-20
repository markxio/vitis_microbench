import pandas as pd
import matplotlib.cm as cm
import numpy as np
import matplotlib.pyplot as plt

import re
from plot import gen_kernel_type, gen_ylim, gen_dtype

def format_digits(dtypes: list) -> list:
    old = dtypes.copy()
    for dtype in dtypes:
        if len(dtype) < 4:
            # it's 8_3 or 8_4
            old.remove(dtype)
            old.append(str(0) + dtype)
    return old

def gen_bitstream_prefix(mypath: str) -> str:
    #example = "/home/nx08/nx08/markkfpga/vitis_microbench/reference_files_u280_hw_dmul_fabric_multi/_x/"
    pattern = "reference_files_(u280_|vck_|vck5000_)?hw_(\w+)"
    bitstream_prefix = re.search(pattern, mypath)
    return bitstream_prefix.group(2)

def gen_bitstream_path(mypath: str) -> str:
    #example = "/home/nx08/nx08/markkfpga/vitis_microbench/reference_files_u280_hw_dmul_fabric_multi/_x/"
    pattern = "^.+\/reference_files_(u280_|vck_|vck5000_)?hw_(\w+)"
    matchobj = re.match(pattern, mypath)
    #fpga = matchobj.groups(1)
    #dtype_op_impl_multi = matchobj.groups(2)
    #bitstream = matchobj.groups(1) 
    return matchobj.group(0)

def gen_op(bitstream_prefix: str) -> str:
    # fadd_fulldsp
    # add_64_12_dsp

    splits = bitstream_prefix.split("_")
    if re.search("\d", bitstream_prefix):
        # fixed point
        return splits[0] 
    else:
        # floating-point
        return splits[0][1:]

def gen_fp_type(bitstream_prefix: str) -> str:
    splits = bitstream_prefix.split("_")
    if re.search("\d", bitstream_prefix):
        # fixed point
        return 0 
    else:
        # floating-point
        return 1 



def gen_impl(bitstream_prefix: str) -> str:
    # fadd_fulldsp
    # add_64_12_dsp
    bitstream_prefix = bitstream_prefix.strip("_multi")
    bitstream_prefix = bitstream_prefix.strip("_single")

    splits = bitstream_prefix.split("_")
    return splits[len(splits)-1]
  
def gen_dtype_old(bitstream_prefix: str) -> str:
    c = bitstream_prefix[0]
    if c == "d":
        return "double"
    elif c == "f":
        return "float"
    elif c == "h":
        return "half"
    else:
        # add_64_12_dsp.hw.xclbin
        pattern = "[a-z]+_(\d{1,2}_\d{1,2})"
        matches = re.search(pattern, bitstream_prefix)
        if matches:
            dtype_found = matches.group(1)
            #if dtype_found[0]=="0":
            #    return dtype_found[1:]
            return dtype_found
        else:
            raise ValueError('gen_dtype: Couldnt detect dtype')
        
def plot_clustered_stacked_stackoverflow(dfall, op: str, filename_prefix: str, ylim: list, labels=None, H="/", **kwargs):
    """Given a list of dataframes, with identical columns and index, create a clustered stacked bar plot. 
labels is a list of the names of the dataframe, used for the legend
title is a string for the title of the plot
H is the hatch used for identification of the different dataframe"""
    
    #ops_with_y_axis=["add", "recip", "div"]
    ops_with_y_axis=["add", "mul", "sub", "div", "exp", "log", "recip", "rsqrt", "sqrt"]

    hatches = ['', '//', '\\\\', '||', '--', '++', 'xx', 'oo', 'OO', '..', '**']
    #hatches = ['', '--', '++', 'xx', 'oo', '//', '\\\\', '||', 'OO', '..', '**']
    n_df = len(dfall)
    n_col = len(dfall[0].columns) 
    n_ind = len(dfall[0].index)
    axe = plt.subplot(111)

    for df in dfall : # for each data frame
        axe = df.plot(kind="bar",
                      linewidth=0,
                      stacked=True,
                      ax=axe,
                      legend=False,
                      grid=False,
                      figsize=(5,4),
                      **kwargs)  # make bar plots

    h,l = axe.get_legend_handles_labels() # get the handles we want to modify
    for i in range(0, n_df * n_col, n_col): # len(h) = n_col * n_df
        for j, pa in enumerate(h[i:i+n_col]):
            for rect in pa.patches: # for each index
                rect.set_x(rect.get_x() + 1 / float(n_df + 1) * i / float(n_col))
                #rect.set_hatch(H * int(i / n_col)) #edited part     
                rect.set_hatch(hatches[int(i / n_col)]) #edited part     
                rect.set_width(1 / float(n_df + 1))
                rect.set_alpha(.99)

    axe.set_xticks((np.arange(0, 2 * n_ind, 2) + 1 / float(n_df + 1)) / 2.) 
    axe.set_xticklabels(df.index, rotation = 45)
    axe.set_title(op)
    axe.set_ylim(ylim)
    if op in ops_with_y_axis:
        axe.set_ylabel("Resource Utilisation (%)")
    else:
        axe.set_ylabel("")
        axe.set_yticklabels([])

    axe.grid(axis="y")
    # Add invisible data to add another legend
    n=[]    
    for i in range(n_df):
        #n.append(axe.bar(0, 0, color="gray", hatch=H * i, alpha=.99)) 
        n.append(axe.bar(0, 0, color="gray", hatch=hatches[i], alpha=.99)) 

    #l1 = axe.legend(h[:n_col], l[:n_col], loc=[1.01, 0.5])

    # for floating_point:
    myloc = "upper right"
    if "fixed" in filename_prefix:
        myloc = "upper left"
    l1 = axe.legend(h[:n_col], l[:n_col], loc=myloc)

    myloc = "upper left"
    if "fixed" in filename_prefix:
        myloc = "upper right"

    if labels is not None:
        #l2 = plt.legend(n, labels, loc=[1.01, 0.1]) 
        l2 = plt.legend(n, labels, loc=myloc) 
    axe.add_artist(l1)
    plt.tight_layout()
    plt.savefig(f"{filename_prefix}_resutil_{op}.pdf", format="pdf")
    plt.close()
    #return axe

def plot_clustered_stacked(dfall, filename, labels=None, title="multiple stacked bar plot",  H="//", **kwargs):
    """Given a list of dataframes, with identical columns and index, create a clustered stacked bar plot.
labels is a list of the names of the dataframe, used for the legend
title is a string for the title of the plot
H is the hatch used for identification of the different dataframe"""

    n_df = len(dfall)
    n_col = len(dfall[0].columns)
    n_ind = len(dfall[0].index)
    axe = plt.subplot(111)

    for df in dfall : # for each data frame
        axe = df.plot(kind="bar",
                      linewidth=0,
                      stacked=True,
                      ax=axe,
                      legend=False,
                      grid=False,
                      **kwargs)  # make bar plots

    h,l = axe.get_legend_handles_labels() # get the handles we want to modify
    for i in range(0, n_df * n_col, n_col): # len(h) = n_col * n_df
        for j, pa in enumerate(h[i:i+n_col]):
            for rect in pa.patches: # for each index
                rect.set_x(rect.get_x() + 1 / float(n_df + 1) * i / float(n_col))
                rect.set_hatch(H * int(i / n_col)) #edited part
                rect.set_width(1 / float(n_df + 1))

    axe.set_xticks((np.arange(0, 2 * n_ind, 2) + 1 / float(n_df + 1)) / 2.)
    axe.set_xticklabels(df.index, rotation = 0)
    #axe.set_title(title)

    # Add invisible data to add another legend
    n=[]
    for i in range(n_df):
        n.append(axe.bar(0, 0, color="gray", hatch=H * i))

    #loc=(0,1.02,1,0.2)
    # https://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot
    # (x0, y0, width, height) where (x0,y0) are the lower left corner coordinates of the bounding box.

    #original: # l1 = axe.legend(h[:n_col], l[:n_col], loc=[1.01, 0.5])
    l1 = axe.legend(h[:n_col], l[:n_col], bbox_to_anchor=(0,1.01,1,0.2), loc="lower left", mode="expand", borderaxespad=0, ncol=3)
    if labels is not None:
        #original # l2 = plt.legend(n, labels, loc=[1.01, 0.1])
        l2 = plt.legend(n, labels, bbox_to_anchor=(0,1.09,1,0.2), loc="lower left", mode="expand", borderaxespad=0, ncol=3)

    axe.add_artist(l1)
    # adjust padding so that both xlabel and ylabel are displayed
    #plt.subplots_adjust(bottom=0.2)
    #plt.setp(plt.xticks()[1], rotation=30, ha='right')
    plt.axes().xaxis.set_ticks_position('none')
    plt.ylabel('Resource Utilisation (%)')
    plt.tight_layout()
    # Place a legend above this subplot, expanding itself to
    # fully use the given bounding box.
    #axe.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
    #axe.axhline(3000, color="black", linestyle="--")
    plt.savefig(f"{filename}.pdf", format="pdf")
    #return axe

def gen_dfs(data: pd.DataFrame, filename_prefix: str) -> (list, list):
    ops = data["op"].unique()
    dtypes_global = data["dtype"].unique().tolist()
    #dtypes_global = format_digits(dtypes_global)
    #dtypes_global.sort()

    for op in ops:
        print("################################################")
        print(op)
        print("################################################")
        data_op = data[data["op"]==op]
        impls = data_op["impl"].unique()
        
        dfs = []
        for impl in impls:
            print("########################")
            print(f"{op} -- {impl}")
            print("########################")
            # mydata = [ [lut1, bram1, dsp1, uram1], [lut2, bram2, dsp2, uram2] ...]
            # index = [ dtype, dtype, dtype .. ]
            data_impl = data_op[data_op["impl"]==impl]
            cols = ['LUT', 'LUTAsMem', 'REG', 'BRAM', 'DSP']
            myseries = []
            for col in cols:
                myseries.append(data_impl[col].to_list())

            dtypes_local = data_impl["dtype"].unique().tolist()
            #dtypes_local = format_digits(dtypes_local)
            #dtypes_local.sort()
            mydata = []
            for j in range(0, len(dtypes_local)):
                vec = []
                for i in range(0, len(myseries)):
                    vec.append(myseries[i][j])
                mydata.append(vec)
          
            print(dtypes_local)
            # set the right position in the mydata array
            # order is DOUBLE, FLOAT, HALF
            # so if HALF is avail, and DOUBLE and FLOAT are missing,
            # need to insert at the start of array
            if len(dtypes_local) < len(dtypes_global):
                # fill up empty bars
                n_missing_dtypes = len(dtypes_global)-len(dtypes_local)
                target_positions=[]
                fixed_point_types=["8_3","8_4","16_6","16_8","32_12","32_16","64_12","64_24"]
                if "double" not in dtypes_local:
                    target_positions.append(0+8)
                if "float" not in dtypes_local:
                    target_positions.append(1+8)
                if "half" not in dtypes_local:
                    target_positions.append(2+8)
               
                print(target_positions)
                if impl not in ["fabric", "dsp"]:
                    # add all fixed point types
                    for idx, t in enumerate(fixed_point_types):
                        target_positions.append(idx)

                target_positions=sorted(target_positions)
                print(target_positions)

                for i in range(0, n_missing_dtypes):
                    vec = []
                    for j in range(0, len(cols)):
                        vec.append(0.0)
                    mydata.insert(target_positions[i], vec)
            else:
                print("No need to add target_positions or insert 0.0's")
            print(mydata)
            print(cols)
            print("#######")
            print(len(mydata))
            print(len(dtypes_local))
            print(len(cols))
            dfs.append(pd.DataFrame(mydata, index=dtypes_global, columns=cols))

        for df in dfs:
            print(df.head(100))

        # multi-kernel ylim
        ylim=[0,60]
        if "single_kernel" in filename_prefix:
            #ylim=[0,6.0] # single op
            #ylim=[0,10.0] # 8-way vec
            ylim=[0,30.0] # 8-way vec, across all fixed-point and floating-point

        #plot_clustered_stacked(dfs, f"plotted_util/{op}_{filename}", impls)
        plot_clustered_stacked_stackoverflow(dfs, op, filename_prefix, ylim=ylim, labels=impls, cmap=plt.cm.Pastel2) #cmap=plt.cm.viridis)

if __name__=="__main__":

    #kernel_types = ["single_kernel", "multi_kernel"]
    kernel_types = ["single_kernel"]
    for kernel_type in kernel_types:
        data = pd.read_csv(f"u280_resutil_{kernel_type}_both.csv")

        data["bitstream_path"] = data.apply(lambda row: gen_bitstream_path(row.bitstream), axis=1)
        data["bitstream_prefix"] = data.apply(lambda row: gen_bitstream_prefix(row.bitstream_path), axis=1)
        data["op"] = data.apply(lambda row: gen_op(row.bitstream_prefix), axis=1)
        data["dtype"] = data.apply(lambda row: gen_dtype(row.bitstream_prefix), axis=1)
        data["impl"] = data.apply(lambda row: gen_impl(row.bitstream_path), axis=1)
        data["kernel_type"] = data.apply(lambda row: gen_kernel_type(row.bitstream_path), axis=1)
        data["floating_point_type"] = data.apply(lambda row: gen_fp_type(row.bitstream_prefix), axis=1)
        data.replace("8_3", "08_3", inplace=True)
        data.replace("8_4", "08_4", inplace=True)
        data.sort_values(by=["dtype", "impl"], ascending=[True, True], inplace=True) 

        #floating_point = data[data["floating_point_type"]==1]
        #fixed_point = data[data["floating_point_type"]==0]
        #
        ## save as csv
        #floating_point[['bitstream', 'bitstream_prefix', 'op', 'dtype', 'impl', 'LUT', 'LUTAsMem', 'REG', 'BRAM', 'URAM', 'DSP']].to_csv(f"u280_resutil_{kernel_type}_floating_point.csv")
        #fixed_point[['bitstream', 'bitstream_prefix', 'op', 'dtype', 'impl', 'LUT', 'LUTAsMem', 'REG', 'BRAM', 'URAM', 'DSP']].to_csv(f"u280_resutil_{kernel_type}_fixed_point.csv")

        #gen_dfs(floating_point, f"u280_floating_point_{kernel_type}")
        #gen_dfs(fixed_point, f"u280_fixed_point_{kernel_type}")

        data[['bitstream', 'bitstream_prefix', 'op', 'dtype', 'impl', 'LUT', 'LUTAsMem', 'REG', 'BRAM', 'DSP']].to_csv(f"u280_resutil_{kernel_type}_both.csv")
        gen_dfs(data, f"u280_both_{kernel_type}")

