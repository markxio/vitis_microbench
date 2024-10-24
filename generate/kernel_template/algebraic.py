

class Kernel:
    def __init__(self, dtype, external_data_width, op, impl, func):
        return f"""
#include "hls_stream.h"

#define PRAGMA_SUB(x) _Pragma (#x)
#define PRAGMA(x) PRAGMA_SUB(x)

// Defines the data type and external memory access width (ideally to make 512 bit width accesses)
#define DATA_TYPE {dtype} 
#define EXTERNAL_DATA_WIDTH {external_data_width}

// The data structure used to pack external memory accesses
struct packed_data {{
  DATA_TYPE data[EXTERNAL_DATA_WIDTH];
}};

static void retrieve_data(struct packed_data*, hls::stream<DATA_TYPE>&, int);
static void do_compute(hls::stream<DATA_TYPE>&, hls::stream<DATA_TYPE>&, int);
static void write_data(hls::stream<DATA_TYPE>&, struct packed_data*, int);

extern "C" {{
void {op}_{impl}(struct packed_data * val1, struct packed_data * result, int num_its) {{
#pragma HLS INTERFACE m_axi port=val1 offset=slave bundle=gmem
#pragma HLS INTERFACE m_axi port=result offset=slave bundle=gmem

#pragma HLS INTERFACE s_axilite port=val1 bundle=control
#pragma HLS INTERFACE s_axilite port=result bundle=control
#pragma HLS INTERFACE s_axilite port=num_its bundle=control
#pragma HLS INTERFACE s_axilite port=return bundle=control

  hls::stream<DATA_TYPE> val1_stream, result_stream;
#pragma HLS STREAM variable=val1_stream depth=8
#pragma HLS STREAM variable=result_stream depth=8

#pragma HLS DATAFLOW
  retrieve_data(val1, val1_stream, num_its);
  do_compute(val1_stream, result_stream, num_its);
  write_data(result_stream, result, num_its);
}}
}}

static void retrieve_data(struct packed_data * val1, hls::stream<DATA_TYPE> & stream, int num_its) {{
  const unsigned int base_its=num_its / EXTERNAL_DATA_WIDTH;
  main_load_data_loop:
  for (unsigned int i=0;i<base_its;i++) {{
PRAGMA(HLS PIPELINE II=EXTERNAL_DATA_WIDTH)
    struct packed_data real_values=val1[i];
    for (unsigned int j=0;j<EXTERNAL_DATA_WIDTH;j++) stream.write(real_values.data[j]);
  }}
  if (base_its * EXTERNAL_DATA_WIDTH < num_its) {{
    struct packed_data real_values=val1[base_its];
    remainder_load_data_loop:
    for (unsigned int j=0;j<num_its - (base_its * EXTERNAL_DATA_WIDTH);j++) stream.write(real_values.data[j]);
  }}
}}

static void do_compute(hls::stream<DATA_TYPE> & val1_stream, hls::stream<DATA_TYPE> & output_stream, int num_its) {{
  main_compute_loop:
  for(unsigned int i=0;i<num_its;i++) {{
#pragma HLS PIPELINE II=1
    DATA_TYPE in1 = val1_stream.read()
    DATA_TYPE out = bench<DATA_TYPE>(in1)
    output_stream.write(out);
  }}
}}

static void write_data(hls::stream<DATA_TYPE> & result_stream, struct packed_data * out, int num_its) {{
  const unsigned int base_its=num_its / EXTERNAL_DATA_WIDTH;
  main_write_data_loop:
  for (unsigned int i=0;i<base_its;i++) {{
PRAGMA(HLS PIPELINE II=EXTERNAL_DATA_WIDTH)
    struct packed_data real_values;
    for (unsigned int j=0;j<EXTERNAL_DATA_WIDTH;j++) {{
      real_values.data[j]=result_stream.read();
    }}
    out[i]=real_values;
  }}
  if (base_its * EXTERNAL_DATA_WIDTH < num_its) {{
    struct packed_data real_values;
    remainder_write_data_loop:
    for (unsigned int j=0;j<num_its - (base_its * EXTERNAL_DATA_WIDTH);j++) {{
      real_values.data[j]=result_stream.read();
    }}
    out[base_its]=real_values;
  }}
}}

template<typename DT>
static DT bench(DT val1) {{
#pragma HLS BIND_OP variable=out op={op} impl={impl}
  DT out = {func}(val1);
  return out;
}}
               """
