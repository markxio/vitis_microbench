
template<typename DT>
static DT fadd_fabric(DT val1, DT val2) {
#pragma HLS BIND_OP variable=out op=fadd impl=fabric
  DT out = val1 + val2;
    return out;
}
               
template<typename DT>
static DT fadd_fulldsp(DT val1, DT val2) {
#pragma HLS BIND_OP variable=out op=fadd impl=fulldsp
  DT out = val1 + val2;
    return out;
}
               
template<typename DT>
static DT fadd_primitivedsp(DT val1, DT val2) {
#pragma HLS BIND_OP variable=out op=fadd impl=primitivedsp
  DT out = val1 + val2;
    return out;
}
               
template<typename DT>
static DT fsub_fabric(DT val1, DT val2) {
#pragma HLS BIND_OP variable=out op=fsub impl=fabric
  DT out = val1 - val2;
    return out;
}
               
template<typename DT>
static DT fsub_fulldsp(DT val1, DT val2) {
#pragma HLS BIND_OP variable=out op=fsub impl=fulldsp
  DT out = val1 - val2;
    return out;
}
               
template<typename DT>
static DT fsub_primitivedsp(DT val1, DT val2) {
#pragma HLS BIND_OP variable=out op=fsub impl=primitivedsp
  DT out = val1 - val2;
    return out;
}
               
template<typename DT>
static DT fdiv_fabric(DT val1, DT val2) {
#pragma HLS BIND_OP variable=out op=fdiv impl=fabric
  DT out = val1 / val2;
    return out;
}
               
template<typename DT>
static DT fmul_fabric(DT val1, DT val2) {
#pragma HLS BIND_OP variable=out op=fmul impl=fabric
  DT out = val1 * val2;
    return out;
}
               
template<typename DT>
static DT fmul_meddsp(DT val1, DT val2) {
#pragma HLS BIND_OP variable=out op=fmul impl=meddsp
  DT out = val1 * val2;
    return out;
}
               
template<typename DT>
static DT fmul_fulldsp(DT val1, DT val2) {
#pragma HLS BIND_OP variable=out op=fmul impl=fulldsp
  DT out = val1 * val2;
    return out;
}
               
template<typename DT>
static DT fmul_maxdsp(DT val1, DT val2) {
#pragma HLS BIND_OP variable=out op=fmul impl=maxdsp
  DT out = val1 * val2;
    return out;
}
               
template<typename DT>
static DT fmul_primitivedsp(DT val1, DT val2) {
#pragma HLS BIND_OP variable=out op=fmul impl=primitivedsp
  DT out = val1 * val2;
    return out;
}
               
template<typename DT>
static DT dadd_fabric(DT val1, DT val2) {
#pragma HLS BIND_OP variable=out op=dadd impl=fabric
  DT out = val1 + val2;
    return out;
}
               
template<typename DT>
static DT dadd_fulldsp(DT val1, DT val2) {
#pragma HLS BIND_OP variable=out op=dadd impl=fulldsp
  DT out = val1 + val2;
    return out;
}
               
template<typename DT>
static DT dsub_fabric(DT val1, DT val2) {
#pragma HLS BIND_OP variable=out op=dsub impl=fabric
  DT out = val1 - val2;
    return out;
}
               
template<typename DT>
static DT dsub_fulldsp(DT val1, DT val2) {
#pragma HLS BIND_OP variable=out op=dsub impl=fulldsp
  DT out = val1 - val2;
    return out;
}
               
template<typename DT>
static DT ddiv_fabric(DT val1, DT val2) {
#pragma HLS BIND_OP variable=out op=ddiv impl=fabric
  DT out = val1 / val2;
    return out;
}
               
template<typename DT>
static DT dmul_fabric(DT val1, DT val2) {
#pragma HLS BIND_OP variable=out op=dmul impl=fabric
  DT out = val1 * val2;
    return out;
}
               
template<typename DT>
static DT dmul_meddsp(DT val1, DT val2) {
#pragma HLS BIND_OP variable=out op=dmul impl=meddsp
  DT out = val1 * val2;
    return out;
}
               
template<typename DT>
static DT dmul_fulldsp(DT val1, DT val2) {
#pragma HLS BIND_OP variable=out op=dmul impl=fulldsp
  DT out = val1 * val2;
    return out;
}
               
template<typename DT>
static DT dmul_maxdsp(DT val1, DT val2) {
#pragma HLS BIND_OP variable=out op=dmul impl=maxdsp
  DT out = val1 * val2;
    return out;
}
               
template<typename DT>
static DT hadd_fabric(DT val1, DT val2) {
#pragma HLS BIND_OP variable=out op=hadd impl=fabric
  DT out = val1 + val2;
    return out;
}
               
template<typename DT>
static DT hadd_meddsp(DT val1, DT val2) {
#pragma HLS BIND_OP variable=out op=hadd impl=meddsp
  DT out = val1 + val2;
    return out;
}
               
template<typename DT>
static DT hadd_fulldsp(DT val1, DT val2) {
#pragma HLS BIND_OP variable=out op=hadd impl=fulldsp
  DT out = val1 + val2;
    return out;
}
               
template<typename DT>
static DT hsub_fabric(DT val1, DT val2) {
#pragma HLS BIND_OP variable=out op=hsub impl=fabric
  DT out = val1 - val2;
    return out;
}
               
template<typename DT>
static DT hsub_meddsp(DT val1, DT val2) {
#pragma HLS BIND_OP variable=out op=hsub impl=meddsp
  DT out = val1 - val2;
    return out;
}
               
template<typename DT>
static DT hsub_fulldsp(DT val1, DT val2) {
#pragma HLS BIND_OP variable=out op=hsub impl=fulldsp
  DT out = val1 - val2;
    return out;
}
               
template<typename DT>
static DT hdiv_fabric(DT val1, DT val2) {
#pragma HLS BIND_OP variable=out op=hdiv impl=fabric
  DT out = val1 / val2;
    return out;
}
               
template<typename DT>
static DT hmul_fabric(DT val1, DT val2) {
#pragma HLS BIND_OP variable=out op=hmul impl=fabric
  DT out = val1 * val2;
    return out;
}
               
template<typename DT>
static DT hmul_fulldsp(DT val1, DT val2) {
#pragma HLS BIND_OP variable=out op=hmul impl=fulldsp
  DT out = val1 * val2;
    return out;
}
               
template<typename DT>
static DT hmul_maxdsp(DT val1, DT val2) {
#pragma HLS BIND_OP variable=out op=hmul impl=maxdsp
  DT out = val1 * val2;
    return out;
}
               