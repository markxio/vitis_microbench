import sys
sys.path.insert(0, '/home/nx08/nx08/markkfpga/vitis_microbench/vitis-data')
from resource_utilisation import ResourceUtilisation, ResourceUtilisationLinked
from pprint import pprint

if __name__=="__main__":

    ######################################
    ## DELTA-HEDGING 
    ## INCREMENTAL VERSIONS
    ######################################
    base = "/home/nx08/nx08/markkfpga/delta-hedging-naive/"
    slug = "/_x/link/vivado/vpl/prj/prj.runs/impl_1/kernel_util_routed.json"
    rpts = {
            "CU 1": "reference_files_hw_cu1_paths25k_steps84",
            "CU 2": "reference_files_hw_cu2_pathsEach12.5k_steps84_hbm_resutil",
            "CU 5": "reference_files_hw_cu5_paths5kEach_timesteps84",
            "CU 10": "reference_files_hw_cu10_paths2.5kEach_timesteps84_successful",
            "CU 25": "reference_files_hw_cu25_paths1kEach_timesteps84_successful",
            }

    util = {}
    print("---------------- delta-hedging multi-kernel")
    for bench, rpt_file in rpts.items():
        print(f"{bench},", end="")
        print(f"{ResourceUtilisationLinked(base+rpt_file+slug).get_resource_utilisation(csv=True, header=True)}")

