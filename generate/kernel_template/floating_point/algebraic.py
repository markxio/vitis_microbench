def get_dtype(op: str) -> str:
    first_char = op[0]
    dtype=""
    if "h" == first_char:
        dtype += "half"
    elif "f" == first_char:
        dtype += "float"
    elif "d" == first_char:
        dtype += "double"
    else:
        exit("get_dtype(): dtype not available for floating-point - choose from [half, float, double]")
    
    return str(dtype)

class Kernel:
    def __init__(self):
        return

    def get(self, dtype, external_data_width, op, impl, func):
        mytype=get_dtype(op)
        return f"""
#include "hls_stream.h"
#include "ap_fixed.h"
#include "hls_math.h"

#define PRAGMA_SUB(x) _Pragma (#x)
#define PRAGMA(x) PRAGMA_SUB(x)

// Defines the data type and external memory access width (ideally to make 512 bit width accesses)
typedef {mytype} DEVICE_DTYPE;
typedef double HOST_DTYPE;
#define EXTERNAL_DATA_WIDTH 8 //{external_data_width}

// The data structure used to pack external memory accesses
struct packed_data {{
  HOST_DTYPE data[EXTERNAL_DATA_WIDTH];
}};

extern "C" {{
void krnl_bench(struct packed_data * val1, struct_packed_data * result, int num_its) {{
#pragma HLS INTERFACE m_axi port=val1 offset=slave bundle=gmem
#pragma HLS INTERFACE m_axi port=result offset=slave bundle=gmem

#pragma HLS INTERFACE s_axilite port=val1 bundle=control
#pragma HLS INTERFACE s_axilite port=result bundle=control
#pragma HLS INTERFACE s_axilite port=num_its bundle=control
#pragma HLS INTERFACE s_axilite port=return bundle=control

main_compute_loop:
  for(unsigned int i=0;i<num_its;i++) {{
//#pragma HLS UNROLL factor=1000
    struct packed_data v1 = val1[i];
    struct packed_data res;

#pragma HLS BIND_OP variable=res op={op} impl={impl}
    res.data[0] = (HOST_DTYPE)(hls::{func}((DEVICE_DTYPE)v1.data[0]));
    res.data[1] = (HOST_DTYPE)(hls::{func}((DEVICE_DTYPE)v1.data[1]));
    res.data[2] = (HOST_DTYPE)(hls::{func}((DEVICE_DTYPE)v1.data[2]));
    res.data[3] = (HOST_DTYPE)(hls::{func}((DEVICE_DTYPE)v1.data[3]));
    res.data[4] = (HOST_DTYPE)(hls::{func}((DEVICE_DTYPE)v1.data[4]));
    res.data[5] = (HOST_DTYPE)(hls::{func}((DEVICE_DTYPE)v1.data[5]));
    res.data[6] = (HOST_DTYPE)(hls::{func}((DEVICE_DTYPE)v1.data[6]));
    res.data[7] = (HOST_DTYPE)(hls::{func}((DEVICE_DTYPE)v1.data[7]));

    result[i] = res; 
  }}
}}
}}
               """
