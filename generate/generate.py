import pandas as pd
from kernel_template.arithmetic import Kernel as kernel_arithmetic
from kernel_template.algebraic import Kernel as kernel_algebraic

class Generator:
    # static members

    def __init__(self):
        # members 
        return

    # add, sub, mul, div
    def template_arithmetic(self, op, impl, sign):
        return f"""
template<typename DT>
static DT bench(DT val1, DT val2) {{
#pragma HLS BIND_OP variable=out op={op} impl={impl}
  DT out = val1 {sign} val2;
    return out;
}}
               """

    # exp(value), log(value), sqrt(value), rsqrt(), recip()
    def template_algebraic(self, op, impl, func):
        return f"""
template<typename DT>
static DT bench(DT val) {{
#pragma HLS BIND_OP variable=out op={op} impl={impl}
  DT out = {func}(val);
    return out;
}}
               """

    def generate(self, op, impl, symbol) -> str:
        first_char = op[0]
        if "h" == first_char:
            dtype = "half"
            external_data_width = 32
        elif "f" == first_char:
            dtype = "float"
            external_data_width = 16
        elif "d" == first_char:
            dtype = "double"
            external_data_width = 8
        else:
            exit("dtype not available for floating-point - choose from [half, float, double]")
       
        if "add" in op or "sub" in op or "mul" in op or "div" in op:
            # arithmetic
            kernel_str = kernel_arithmetic(dtype=dtype, external_data_width=external_data_width, op=op, impl=impl, sign=symbol)
        else:
            # algebraic
            kernel_str = kernel_algebraic(dtype=dtype, external_data_width=external_data_width, op=op, impl=impl, func=symbol)

        # write kernel to file
        with open(f"../src/device/{op}_{impl}.cpp", "w+") as f:
            f.writelines(kernel_str)

        return True

    def generate(self, csv_file: str):
        config = pd.read_csv(csv_file)

        arithmetic = config[config["Sign"]!="0"]
        arithmetic["kernel"] = arithmetic.apply(lambda row: generate(op=row.Operation, impl=row.Implementation, symbol=row.Sign), axis=1)
        
        algebraic = config[config["Function"]!="0"]
        algebraic["bench"] = algebraic.apply(lambda row: generate(op=row.Operation, impl=row.Implementation, symbol=row.Function), axis=1)

if __name__=="__main__":
    gen = Generator()
    gen.generate(csv_file="float_ops.csv")
