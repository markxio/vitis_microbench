import pandas as pd
from pathlib import Path

from kernel_template.fixed_point.binary import Kernel as fixed_kernel_binary
from kernel_template.fixed_point.unary import Kernel as fixed_kernel_unary
from kernel_template.floating_point.binary import Kernel as float_kernel_binary
from kernel_template.floating_point.unary import Kernel as float_kernel_unary

class Generator:
    # static members

    def __init__(self):
        # members 
        return

    # add, sub, mul, div
    def template_binary(self, op, impl, sign):
        return f"""
template<typename DT>
static DT bench(DT val1, DT val2) {{
#pragma HLS BIND_OP variable=out op={op} impl={impl}
  DT out = val1 {sign} val2;
    return out;
}}
               """

    # exp(value), log(value), sqrt(value), rsqrt(), recip()
    def template_unary(self, op, impl, func):
        return f"""
template<typename DT>
static DT bench(DT val) {{
#pragma HLS BIND_OP variable=out op={op} impl={impl}
  DT out = {func}(val);
    return out;
}}
               """

    def write_kernel(self, isFloatingPoint, op, impl, dtype, external_data_width, symbol, wordlength=0, integerbits=0) -> bool:
        if "add" in op or "sub" in op or "mul" in op or "div" in op:
            # binary
            #if 3 != len(op):
            if isFloatingPoint:
                precision="floating_point"
                kernel_str = float_kernel_binary().get(dtype=dtype, external_data_width=external_data_width, op=op, impl=impl, sign=symbol)
            else:
                precision="fixed_point"
                kernel_str = fixed_kernel_binary().get(wordlength=wordlength, integerbits=integerbits, external_data_width=external_data_width, op=op, impl=impl, sign=symbol)
        else:
            # unary 
            # TODO: conditionals
            # all fixed point: sqrt, rsqrt, recip
            #if 3 != len(op):
            if isFloatingPoint:
                precision="floating_point"
                kernel_str = float_kernel_unary().get(dtype=dtype, external_data_width=external_data_width, op=op, impl=impl, func=symbol)
            else:
                precision="fixed_point"
                kernel_str = fixed_kernel_unary().get(wordlength=wordlength, integerbits=integerbits, external_data_width=external_data_width, op=op, impl=impl, func=symbol)

        # write kernel to file
        fixed_point=""
        #if 3 == len(op):
        if not isFloatingPoint:
            # it's fixed point precision
            fixed_point=str(wordlength) + "_" + str(integerbits) + "_"

        Path(f"../src/device/{precision}").mkdir(parents=True, exist_ok=True)
        with open(f"../src/device/{precision}/{op}_{fixed_point}{impl}.cpp", "w+") as f:
            f.writelines(kernel_str)

        return True

    def add_external_data_width_col(self, op: str):
        first_char = op[0]
        if "h" == first_char:
            external_data_width = 32
        elif "f" == first_char:
            external_data_width = 16
        elif "d" == first_char:
            external_data_width = 8
        else:
            exit("add_external_data_width_col(): dtype not available for floating-point - choose from [half, float, double]")
        
        return external_data_width

    def add_dtype_col(self, op: str) -> str:
        first_char = op[0]
        dtype=""
        if "h" == first_char:
            dtype += "half"
        elif "f" == first_char:
            dtype += "float"
        elif "d" == first_char:
            dtype += "double"
        else:
            exit("add_dtype_col(): dtype not available for floating-point - choose from [half, float, double]")
        
        return str(dtype)

    def generate(self, csv_file: str):
        config = pd.read_csv(csv_file, dtype = {"Sign": str, "Function": str})

        isFloatingPoint=True
        if "WordLength" not in list(config.columns):
            print("Generating floating-point kernels...")
            # it's the csv for floating-point ops
            # for fixed-point we already added both dtype and external_data_width
            config["dtype"] = config.apply(lambda row: self.add_dtype_col(op=row.Operation), axis=1)
            config["dtype"]=config["dtype"].astype(str)
            config["ExternalDataWidth"] = config.apply(lambda row: self.add_external_data_width_col(op=row.Operation), axis=1)
            config["WordLength"] = config.apply(lambda row: 0, axis=1)
            config["IntegerBits"] = config.apply(lambda row: 0, axis=1)
        else:
            print("Generating fixed-point kernels...")
            # fixed-point precision
            config["dtype"]  = config.apply(lambda row: "rien", axis=1)
            isFloatingPoint=False
        
        binary = config[config["Sign"]!="0"]

        if len(binary) > 0:
            binary["kernel"] = binary.apply(lambda row: self.write_kernel(isFloatingPoint=isFloatingPoint, op=row.Operation, impl=row.Implementation, dtype=row.dtype, external_data_width=row.ExternalDataWidth, symbol=row.Sign, wordlength=row.WordLength, integerbits=row.IntegerBits), axis=1)
        
        unary = config[config["Function"]!="0"]

        if len(unary) > 0:
            unary["kernel"] = unary.apply(lambda row: self.write_kernel(isFloatingPoint=isFloatingPoint, op=row.Operation, impl=row.Implementation, dtype=row.dtype, external_data_width=row.ExternalDataWidth, symbol=row.Function, wordlength=row.WordLength, integerbits=row.IntegerBits), axis=1)

    def generate_fixed_point_config(self, output_csv):
        self.fixed_point_config = {
            # TODO: change to single list instead of permutation
            "op": ["mul", "add", "sub", "div", "exp", "log", "sqrt", "rsqrt", "recip"],
            "impl": ["fabric", "dsp"],
            "bits": [(8,3), (8,4), (16,6), (16,8), (32,12), (32,16), (64,12), (64,24)] # (W,I)
        }

        s = []
        # get all combinations
        for op in self.fixed_point_config["op"]:
            for impl in self.fixed_point_config["impl"]:
                for bits in self.fixed_point_config["bits"]:
                    # fn/unary
                    if "mul" in op or "add" in op or "sub" in op or "div" in op:
                        fn=0
                    else:
                        fn=op
                        #exit("We're generating fixed point ops and op was neither add, sub or mul")
                    # sign/binary
                    if "mul" in op:
                        sign="*"
                    elif "add" in op:
                        sign="+"
                    elif "sub" in op:
                        sign="-"
                    elif "div" in op:
                        sign="/"
                    else:
                        sign=0

                    external_data_width=int(512/int(bits[0]))

                    print(f'{op}_{str(bits[0])}_{str(bits[1])}')
                    s.append(pd.Series({"Operation": op, "Implementation": impl, "WordLength": str(bits[0]), "IntegerBits": str(bits[1]), "ExternalDataWidth": external_data_width, "MinLatency": 0, "MaxLatency": 4, "Sign": sign, "Function": fn}))

        df = pd.DataFrame(s)
        df.to_csv(output_csv, index=None)