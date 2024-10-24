# Microbench for arithmetic and algebraic operations 

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
