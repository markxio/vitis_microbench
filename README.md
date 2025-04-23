# Microbench for arithmetic and algebraic operations 

## Kernel considerations

### pragma hls dataflow but without unroll

For fadd_fabric, Without unroll, in a dataflow structure, with dedicated read, compute and write stages, the FF and LUT for the do_compute module (contains the main_compute_loop) are expected to account for 6.61% and 5.62% of the total configured FF and LUT resources.

    +---------------------+-------------------+---------+----+------+------+-----+
    |       Instance      |       Module      | BRAM_18K| DSP|  FF  |  LUT | URAM|
    +---------------------+-------------------+---------+----+------+------+-----+
    |control_s_axi_U      |control_s_axi      |        0|   0|   291|   490|    0|  
    |do_compute_U0        |do_compute         |        0|   0|   423|   542|    0|  
    |entry_proc_U0        |entry_proc         |        0|   0|     3|    29|    0|  
    |result_port_m_axi_U  |result_port_m_axi  |       16|   0|   881|  1052|    0|  
    |retrieve_data_U0     |retrieve_data      |        0|   0|   960|  1825|    0|  
    |retrieve_data_1_U0   |retrieve_data_1    |        0|   0|   959|  1807|    0|  
    |val1_port_m_axi_U    |val1_port_m_axi    |       16|   0|   881|  1052|    0|  
    |val2_port_m_axi_U    |val2_port_m_axi    |       16|   0|   881|  1052|    0|  
    |write_data_U0        |write_data         |        0|   0|  1116|  1788|    0|  
    +---------------------+-------------------+---------+----+------+------+-----+
    |Total                |                   |       48|   0|  6395|  9637|    0|  
    +---------------------+-------------------+---------+----+------+------+-----+

### pragma hls unroll factor=100

For fadd_fulldsp, with unroll factor=100, the FF and LUT for the main_compute_loop are expected to account for 97.50% and 97.59% of the total configured FF and LUT resources.

Problem: Implementation leads to very long II~250. Would need to make 100 input elements available at iteration start.

Solution: Try manual unroll with eight elements as we can read in burst of eight 64 bit elements from ext mem. Could try to double this by calling do_compute func twice (requires one result output per func call)

    +--------------------------------------------------+---------------------------------------+---------+----+-------+--------+-----+
    |                     Instance                     |                 Module                | BRAM_18K| DSP|   FF  |   LUT  | URAM|
    +--------------------------------------------------+---------------------------------------+---------+----+-------+--------+-----+
    |control_s_axi_U                                   |control_s_axi                          |        0|   0|    291|     490|    0|  
    |grp_krnl_bench_Pipeline_main_compute_loop_fu_121  |krnl_bench_Pipeline_main_compute_loop  |        0|   2|  77641|  112957|    0|  
    |result_port_m_axi_U                               |result_port_m_axi                      |        4|   0|    566|     766|    0|  
    |val1_port_m_axi_U                                 |val1_port_m_axi                        |        4|   0|    566|     766|    0|  
    |val2_port_m_axi_U                                 |val2_port_m_axi                        |        4|   0|    566|     766|    0|  
    +--------------------------------------------------+---------------------------------------+---------+----+-------+--------+-----+
    |Total                                             |                                       |       12|   2|  79630|  115745|    0|  
    +--------------------------------------------------+---------------------------------------+---------+----+-------+--------+-----+

### manual unroll (factor=8 to match 8x64bit burst reads) 

For fadd_fabric, with manually unrolled eight adds per burst read (read struct from ext mem then perf eight adds per iteration) the FF and LUT for the main_compute_loop are expected to account for 39.85% and 42.58% of the total configured FF and LUT resources.

    +---------------------------------+------------------------------+---------+----+-----+------+-----+
    |             Instance            |            Module            | BRAM_18K| DSP|  FF |  LUT | URAM|
    +---------------------------------+------------------------------+---------+----+-----+------+-----+
    |control_s_axi_U                  |control_s_axi                 |        0|   0|  291|   490|    0|  
    |fadd_32ns_32ns_32_5_no_dsp_1_U1  |fadd_32ns_32ns_32_5_no_dsp_1  |        0|   0|  243|   338|    0|  
    |fadd_32ns_32ns_32_5_no_dsp_1_U2  |fadd_32ns_32ns_32_5_no_dsp_1  |        0|   0|  243|   338|    0|  
    |fadd_32ns_32ns_32_5_no_dsp_1_U3  |fadd_32ns_32ns_32_5_no_dsp_1  |        0|   0|  243|   338|    0|  
    |fadd_32ns_32ns_32_5_no_dsp_1_U4  |fadd_32ns_32ns_32_5_no_dsp_1  |        0|   0|  243|   338|    0|  
    |fadd_32ns_32ns_32_5_no_dsp_1_U5  |fadd_32ns_32ns_32_5_no_dsp_1  |        0|   0|  243|   338|    0|  
    |fadd_32ns_32ns_32_5_no_dsp_1_U6  |fadd_32ns_32ns_32_5_no_dsp_1  |        0|   0|  243|   338|    0|  
    |fadd_32ns_32ns_32_5_no_dsp_1_U7  |fadd_32ns_32ns_32_5_no_dsp_1  |        0|   0|  243|   338|    0|  
    |fadd_32ns_32ns_32_5_no_dsp_1_U8  |fadd_32ns_32ns_32_5_no_dsp_1  |        0|   0|  243|   338|    0|  
    |result_port_m_axi_U              |result_port_m_axi             |       16|   0|  881|  1052|    0|  
    |val1_port_m_axi_U                |val1_port_m_axi               |       16|   0|  881|  1052|    0|  
    |val2_port_m_axi_U                |val2_port_m_axi               |       16|   0|  881|  1052|    0|  
    +---------------------------------+------------------------------+---------+----+-----+------+-----+
    |Total                            |                              |       48|   0| 4878|  6350|    0|  
    +---------------------------------+------------------------------+---------+----+-----+------+-----+

For fadd_fulldsp, with manually unrolled eight adds per burst read, 53.88% and 32.38% of the total configured FF and LUT resources:

    +--------------------------------------------------+---------------------------------------+---------+----+------+------+-----+
    |                     Instance                     |                 Module                | BRAM_18K| DSP|  FF  |  LUT | URAM|
    +--------------------------------------------------+---------------------------------------+---------+----+------+------+-----+
    |control_s_axi_U                                   |control_s_axi                          |        0|   0|   291|   490|    0|  
    |grp_krnl_bench_Pipeline_main_compute_loop_fu_121  |krnl_bench_Pipeline_main_compute_loop  |        0|  16|  3428|  1746|    0|  
    |result_port_m_axi_U                               |result_port_m_axi                      |       16|   0|   881|  1052|    0|  
    |val1_port_m_axi_U                                 |val1_port_m_axi                        |       16|   0|   881|  1052|    0|  
    |val2_port_m_axi_U                                 |val2_port_m_axi                        |       16|   0|   881|  1052|    0|  
    +--------------------------------------------------+---------------------------------------+---------+----+------+------+-----+
    |Total                                             |                                       |       48|  16|  6362|  5392|    0|  
    +--------------------------------------------------+---------------------------------------+---------+----+------+------+-----+

#### estimates

| ops | precision | % of total ff | % of total LUT | 
| --- | --------- | ------------- | -------------- |
| 8   | double    | 39.85         | 42.58          |
| 16  | float     | 56.99         | 59.73          |
| 32  | half      | 72.61         | 74.79          |


## Versal ACAP

For Versal ACAPs, the [DSP58](https://docs.amd.com/r/2022.1-English/ug1273-versal-acap-design/UltraRAM-Primitives) primitive includes the same features as in UltraScale devices, including a multiplier, adder, pre-adder, and registers to fully pipeline the primitive. However, sizing differs and the primitives include additional features.

### Dot product

The DSP58 can implement a dot product, which is a multiplier that is represented as three smaller multipliers that are added together. Dot products are often used in filters in image processing. For more information, see the Versal ACAP DSP Engine Architecture Manual (AM004). The following figure shows an example of a dot product with an extra adder.

Note: For the dot product to infer, the RTL must use signed logic.

### bind_op

Vitis HLS implements the operations in the code using specific implementations. The BIND_OP pragma specifies that for a specific variable, an operation (mul, add, div) should be mapped to a specific device resource for implementation (impl) in the RTL. If the BIND_OP pragma is not specified, Vitis HLS automatically determines the resources to use for operations.

For example, to indicate that a specific multiplier operation (mul) is implemented in the device fabric rather than a DSP, you can use the BIND_OP pragma.

You can also specify the latency of the operation using the latency option.

Important: To use the latency option, the operation must have an available multi-stage implementation. The HLS tool provides a multi-stage implementation for all basic arithmetic operations (add, subtract, multiply, and divide), and all floating-point operations.
