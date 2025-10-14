
#include "hls_stream.h"
#include "ap_fixed.h"
#include "hls_math.h"

#define PRAGMA_SUB(x) _Pragma (#x)
#define PRAGMA(x) PRAGMA_SUB(x)

// Defines the data type and external memory access width (ideally to make 512 bit width accesses)
typedef ap_fixed<32,12> DEVICE_DTYPE;
typedef double HOST_DTYPE;
#define EXTERNAL_DATA_WIDTH 8 //16

// The data structure used to pack external memory accesses
struct packed_data {
  DEVICE_DTYPE data[EXTERNAL_DATA_WIDTH];
};

extern "C" {
void krnl_bench(struct packed_data * val1, struct packed_data * val2, struct packed_data * result, int num_its) {
#pragma HLS INTERFACE m_axi port=val1 offset=slave bundle=val1_port
#pragma HLS INTERFACE m_axi port=val2 offset=slave bundle=val2_port
#pragma HLS INTERFACE m_axi port=result offset=slave bundle=result_port

#pragma HLS INTERFACE s_axilite port=val1 bundle=control
#pragma HLS INTERFACE s_axilite port=val2 bundle=control
#pragma HLS INTERFACE s_axilite port=result bundle=control
#pragma HLS INTERFACE s_axilite port=num_its bundle=control
#pragma HLS INTERFACE s_axilite port=return bundle=control

  assert(num_its % 8 == 0);

main_compute_loop:
  for(unsigned int i=0;i<num_its/EXTERNAL_DATA_WIDTH;i++) {
//#pragma HLS UNROLL factor=1000
    struct packed_data v1 = val1[i];
    struct packed_data v2 = val2[i];
    struct packed_data res;

    DEVICE_DTYPE tmp_0;
    DEVICE_DTYPE tmp_1;
    DEVICE_DTYPE tmp_2;
    DEVICE_DTYPE tmp_3;
    DEVICE_DTYPE tmp_4;
    DEVICE_DTYPE tmp_5;
    DEVICE_DTYPE tmp_6;
    DEVICE_DTYPE tmp_7;

#pragma HLS BIND_OP variable=tmp_0 op=add impl=dsp
#pragma HLS BIND_OP variable=tmp_1 op=add impl=dsp
#pragma HLS BIND_OP variable=tmp_2 op=add impl=dsp
#pragma HLS BIND_OP variable=tmp_3 op=add impl=dsp
#pragma HLS BIND_OP variable=tmp_4 op=add impl=dsp
#pragma HLS BIND_OP variable=tmp_5 op=add impl=dsp
#pragma HLS BIND_OP variable=tmp_6 op=add impl=dsp
#pragma HLS BIND_OP variable=tmp_7 op=add impl=dsp

    tmp_0 = (DEVICE_DTYPE)v1.data[0] + (DEVICE_DTYPE)v2.data[0];
    tmp_1 = (DEVICE_DTYPE)v1.data[1] + (DEVICE_DTYPE)v2.data[1]; 
    tmp_2 = (DEVICE_DTYPE)v1.data[2] + (DEVICE_DTYPE)v2.data[2]; 
    tmp_3 = (DEVICE_DTYPE)v1.data[3] + (DEVICE_DTYPE)v2.data[3]; 
    tmp_4 = (DEVICE_DTYPE)v1.data[4] + (DEVICE_DTYPE)v2.data[4]; 
    tmp_5 = (DEVICE_DTYPE)v1.data[5] + (DEVICE_DTYPE)v2.data[5]; 
    tmp_6 = (DEVICE_DTYPE)v1.data[6] + (DEVICE_DTYPE)v2.data[6]; 
    tmp_7 = (DEVICE_DTYPE)v1.data[7] + (DEVICE_DTYPE)v2.data[7]; 

    res.data[0] = (HOST_DTYPE) tmp_0; 
    res.data[1] = (HOST_DTYPE) tmp_1; 
    res.data[2] = (HOST_DTYPE) tmp_2; 
    res.data[3] = (HOST_DTYPE) tmp_3; 
    res.data[4] = (HOST_DTYPE) tmp_4; 
    res.data[5] = (HOST_DTYPE) tmp_5; 
    res.data[6] = (HOST_DTYPE) tmp_6; 
    res.data[7] = (HOST_DTYPE) tmp_7;

    result[i] = res; 
  }
}
}
               