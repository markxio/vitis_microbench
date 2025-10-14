from pathlib import Path
import pandas as pd
import os
from vitis_microbench.vitis_data.resource_utilisation import ResourceUtilisation

def load_configs():
    df = pd.read_csv("../generate/fixed_point_ops.csv")
    # Operation,Implementation,WordLength,IntegerBits
    df["config"] = df["Operation"] + "_" + df["WordLength"].astype(str) + "_" + df["IntegerBits"] + "_" + df["Implementation"]
    configs = df["config"].tolist()

    df = pd.read_csv("../generate/float_ops.csv")
    # Operation,Implementation
    df["config"] = df["Operation"] + "_" + df["Implementation"]
    configs.extend(df["config"].tolist())

    return configs

def write_csv_stats(fpga, target, kernel_type, kernel_name, tdir):
    configs = load_configs()

    synth_data = []
    synth_slr_data = []
    linked_data = []
    module_data = []

    # target directory
    os.system(f"mkdir -p {tdir}")
    for config in configs:
        root_dir = f"reference_files_{fpga}_{target}_{config}_{kernel_type}"
        resutil = ResourceUtilisation(root_dir=root_dir, binary_name=config, kernel_name=kernel_name)

        synth_data.append(resutil.get_stats_synth())
        synth_slr_data.append(resutil.get_stats_synth(per_slr=True))
        linked_data.append(resutil.get_stats_linked())
        module_data.append(resutil.get_module_estimate("main_compute_loop"))

    pd.DataFrame(synth_data, index=configs).to_csv(f"{tdir}/csynth.csv")
    pd.DataFrame(synth_slr_data, index=configs).to_csv(f"{tdir}/csynth_slr.csv")
    pd.DataFrame(linked_data, index=configs).to_csv(f"{tdir}/linked.csv")
    pd.DataFrame(module_data, index=configs).to_csv(f"{tdir}/csynth_module.csv")
