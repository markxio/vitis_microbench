import os
import sys
import re
import pandas as pd
sys.path.insert(0, '/home/nx08/nx08/markkfpga/vitis_microbench/vitis-data')
from resource_utilisation import ResourceUtilisation
from average import plot_grouped_bars

def get_all_dirs_by_name(dir_path: str, starts_with: str):  
    dirs = os.listdir(dir_path)
    dirs = [d for d in dirs if starts_with in d]
    return dirs

if __name__=="__main__":
    dir_starts_with = {
                        "u280": "reference_files_hw_",
                        "vck5000": "reference_files_vck5000_hw_", 
                      }
    patterns = {
                "u280": "(?:" + dir_starts_with['u280'] + ")([a-z]*_[a-z]*)",
                "vck5000": "(?:" + dir_starts_with['vck5000'] + ")([a-z]*_[a-z]*)",
             }

    work_dir="/home/nx08/nx08/markkfpga/vitis_microbench"

    for fpga, pattern in patterns.items():
        projects = get_all_dirs_by_name(work_dir, dir_starts_with[fpga])
        s = []
        for project in projects:
            match=re.search(pattern, project)
            config=match.group(1)
            project_dir=match.group(0)

            splits=config.split("_")
            dtype_op=splits[0]
            impl=splits[1]

            bitstream_exists = os.path.isfile(f"{work_dir}/{project_dir}/{config}.hw.xclbin")
            
            if not bitstream_exists:
                continue

            root_dir=f"{work_dir}/{dir_starts_with[fpga]}{config}"
            bin_name=f"{config}"
            kernel_name=f"krnl_bench"
            
            obj_res_util = ResourceUtilisation(root_dir, bin_name, kernel_name)
            mydict = obj_res_util.get_resource_utilisation()
            mydict["dtype_op"] = dtype_op
            mydict["impl"] = impl
            mydict["config"] = config

            mydict["bitstream"] = project_dir
            s.append(pd.Series(mydict))

        df = pd.DataFrame(s)
        df.to_csv(f"utilisation_{fpga}.csv", index=False)

        resources = ["bram", "dsp", "ff", "lut"]

        for r in resources:
            pivot_data=df.pivot(index='dtype_op', columns='impl', values=r)
            plot_grouped_bars(pivot_data, ylabel='Utilisation (%)', title=f"Utilisation {r.upper()} by Operation and Data Type", ylim=[], output_file=f"plot_utilisation_{fpga}_{r}.pdf")
