from pathlib import Path
import sys
sys.path.insert(0, '/home/nx08/nx08/markkfpga/vitis_microbench/vitis-data')
from resource_utilisation import ResourceUtilisation, ResourceUtilisationLinked, ResourceUtilisationLinkedSingleKernel
from pprint import pprint

def get_u280_floating_point_configs() -> list:
    return [
                "dadd_fabric",
                "dadd_fulldsp",
                "ddiv_fabric",
                "dexp_fabric",
                "dexp_fulldsp",
                "dexp_meddsp",
                "dlog_fabric",
                "dlog_fulldsp",
                "dlog_meddsp",
                "dmul_fabric",
                "dmul_fulldsp",
                "dmul_maxdsp",
                "dmul_meddsp",
                "drecip_fulldsp",
                "drsqrt_fulldsp",
                "dsqrt_fabric",
                "dsub_fabric",
                "dsub_fulldsp",
                "fadd_fabric",
                "fadd_fulldsp",
                "fdiv_fabric",
                "fexp_fabric",
                "fexp_fulldsp",
                "fexp_meddsp",
                "flog_fabric",
                "flog_fulldsp",
                "flog_meddsp",
                "fmul_fabric",
                "fmul_fulldsp",
                "fmul_maxdsp",
                "fmul_meddsp",
                "frecip_fabric",
                "frecip_fulldsp",
                "frsqrt_fabric",
                "frsqrt_fulldsp",
                "fsqrt_fabric",
                "fsub_fabric",
                "fsub_fulldsp",
                "hadd_fabric",
                "hadd_fulldsp",
                "hadd_meddsp",
                "hdiv_fabric",
                "hmul_fabric",
                "hmul_fulldsp",
                "hmul_maxdsp",
                "hsqrt_fabric",
                "hsub_fabric",
                "hsub_fulldsp",
                "hsub_meddsp"
            ]

def get_u280_fixed_point_configs() -> list:
    return [
                "add_16_6_dsp",
                "add_16_6_fabric",
                "add_16_8_dsp",
                "add_16_8_fabric",
                "add_32_12_dsp",
                "add_32_12_fabric",
                "add_32_16_dsp",
                "add_32_16_fabric",
                "add_64_12_dsp",
                "add_64_12_fabric",
                "add_64_24_dsp",
                "add_64_24_fabric",
                "add_8_3_dsp",
                "add_8_3_fabric",
                "add_8_4_dsp",
                "add_8_4_fabric",
                "mul_16_6_dsp",
                "mul_16_6_fabric",
                "mul_16_8_dsp",
                "mul_16_8_fabric",
                "mul_32_12_dsp",
                "mul_32_12_fabric",
                "mul_32_16_dsp",
                "mul_32_16_fabric",
                "mul_64_12_dsp",
                "mul_64_12_fabric",
                "mul_64_24_dsp",
                "mul_64_24_fabric",
                "mul_8_3_dsp",
                "mul_8_3_fabric",
                "mul_8_4_dsp",
                "mul_8_4_fabric",
                "sub_16_6_dsp",
                "sub_16_6_fabric",
                "sub_16_8_dsp",
                "sub_16_8_fabric",
                "sub_32_12_dsp",
                "sub_32_12_fabric",
                "sub_32_16_dsp",
                "sub_32_16_fabric",
                "sub_64_12_dsp",
                "sub_64_12_fabric",
                "sub_64_24_dsp",
                "sub_64_24_fabric",
                "sub_8_3_dsp",
                "sub_8_3_fabric",
                "sub_8_4_dsp",
                "sub_8_4_fabric"
            ]

def get_vck_floating_point_configs() -> list:
    return [
                "dadd_fabric",
                "dadd_fulldsp",
                "ddiv_fabric",
                "dexp_fabric",
                "dexp_fulldsp",
                "dexp_meddsp",
                "dlog_fabric",
                "dlog_fulldsp",
                "dlog_meddsp",
                "dmul_fabric",
                "dmul_fulldsp",
                "dmul_maxdsp",
                "dmul_meddsp",
                "drecip_fulldsp",
                "drsqrt_fulldsp",
                "dsqrt_fabric",
                "dsub_fabric",
                "dsub_fulldsp",
                "fadd_fabric",
                "fadd_fulldsp",
                "fadd_primitivedsp",
                "fdiv_fabric",
                "fexp_fabric",
                "fexp_fulldsp",
                "fexp_meddsp",
                "flog_fabric",
                "flog_fulldsp",
                "flog_meddsp",
                "fmul_fabric",
                "fmul_fulldsp",
                "fmul_maxdsp",
                "fmul_meddsp",
                "fmul_primitivedsp",
                "frecip_fabric",
                "frecip_fulldsp",
                "frsqrt_fabric",
                "frsqrt_fulldsp",
                "fsqrt_fabric",
                "fsub_fabric",
                "fsub_fulldsp",
                "fsub_primitivedsp",
                "hadd_fabric",
                "hadd_fulldsp",
                "hadd_meddsp",
                "hdiv_fabric",
                "hsub_fabric",
                "hsub_fulldsp",
                "hsub_meddsp"
            ] 

def get_vck_fixed_point_configs() -> list:
    return [
                "add_16_6_dsp",
                "add_16_6_fabric",
                "add_16_8_dsp",
                "add_16_8_fabric",
                "add_32_12_dsp",
                "add_32_12_fabric",
                "add_32_16_dsp",
                "add_32_16_fabric",
                "add_64_12_dsp",
                "add_64_12_fabric",
                "add_64_24_dsp",
                "add_64_24_fabric",
                "add_8_3_dsp",
                "add_8_3_fabric",
                "add_8_4_dsp",
                "add_8_4_fabric",
                "mul_16_6_dsp",
                "mul_16_6_fabric",
                "mul_16_8_dsp",
                "mul_16_8_fabric",
                "mul_32_12_dsp",
                "mul_32_12_fabric",
                "mul_32_16_dsp",
                "mul_32_16_fabric",
                "mul_64_12_dsp",
                "mul_64_12_fabric",
                "mul_64_24_dsp",
                "mul_64_24_fabric",
                "mul_8_3_dsp",
                "mul_8_3_fabric",
                "mul_8_4_dsp",
                "mul_8_4_fabric",
                "sub_16_6_dsp",
                "sub_16_6_fabric",
                "sub_16_8_dsp",
                "sub_16_8_fabric",
                "sub_32_12_dsp",
                "sub_32_12_fabric",
                "sub_32_16_dsp",
                "sub_32_16_fabric",
                "sub_64_12_dsp",
                "sub_64_12_fabric",
                "sub_64_24_dsp",
                "sub_64_24_fabric",
                "sub_8_3_dsp",
                "sub_8_3_fabric",
                "sub_8_4_dsp",
                "sub_8_4_fabric"
            ]

def bitstream_exists(f: str) -> bool:
    my_file = Path(f)
    if my_file.is_file():
        # file exists
        return True
    return False

def get_u280_multi_kernel_floating_point_dirs():
    dirs=[]
    for config in get_u280_floating_point_configs():
        dirs.append(f"u280_hw_{config}_multi")
    return dirs

def get_u280_multi_kernel_fixed_point_dirs():
    dirs=[]
    for config in get_u280_fixed_point_configs():
        dirs.append(f"u280_hw_{config}_multi")
    return dirs

def print_linked_resutil(base: str, util_linked_json: str, configs: list):
    for config in configs:
        f = f"{base}/reference_files_{config}{util_linked_json}"
        resutil = ResourceUtilisationLinked(f)
        print(resutil.get_resource_utilisation(csv=True))

if __name__=="__main__":
    base="/home/nx08/nx08/markkfpga/vitis_microbench"
    util_linked_json="/_x/link/vivado/vpl/prj/prj.runs/impl_1/kernel_util_routed.json"
    util_hls_rpt="/_x/reports/hadd_fulldsp/hls_reports/krnl_bench_csynth.rpt"

    #f="/home/nx08/nx08/markkfpga/myproj/reference_files_hw_half_assets50_timesteps1260_cu6/_x/link/vivado/vpl/prj/prj.runs/impl_1/kernel_util_routed.json"
    #resutil = ResourceUtilisationLinked(f)
    #print(resutil.get_header())

    print_linked_resutil(base, util_linked_json, get_u280_multi_kernel_floating_point_dirs())
    print_linked_resutil(base, util_linked_json, get_u280_multi_kernel_fixed_point_dirs())
