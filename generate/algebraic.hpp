
template<typename DT>
static DT fexp_fabric(DT val) {
#pragma HLS BIND_OP variable=out op=fexp impl=fabric
  DT out = exp(val);
    return out;
}
               
template<typename DT>
static DT fexp_meddsp(DT val) {
#pragma HLS BIND_OP variable=out op=fexp impl=meddsp
  DT out = exp(val);
    return out;
}
               
template<typename DT>
static DT fexp_fulldsp(DT val) {
#pragma HLS BIND_OP variable=out op=fexp impl=fulldsp
  DT out = exp(val);
    return out;
}
               
template<typename DT>
static DT flog_fabric(DT val) {
#pragma HLS BIND_OP variable=out op=flog impl=fabric
  DT out = log(val);
    return out;
}
               
template<typename DT>
static DT flog_meddsp(DT val) {
#pragma HLS BIND_OP variable=out op=flog impl=meddsp
  DT out = log(val);
    return out;
}
               
template<typename DT>
static DT flog_fulldsp(DT val) {
#pragma HLS BIND_OP variable=out op=flog impl=fulldsp
  DT out = log(val);
    return out;
}
               
template<typename DT>
static DT fsqrt_fabric(DT val) {
#pragma HLS BIND_OP variable=out op=fsqrt impl=fabric
  DT out = sqrt(val);
    return out;
}
               
template<typename DT>
static DT frsqrt_fabric(DT val) {
#pragma HLS BIND_OP variable=out op=frsqrt impl=fabric
  DT out = sqrt(val);
    return out;
}
               
template<typename DT>
static DT frsqrt_fulldsp(DT val) {
#pragma HLS BIND_OP variable=out op=frsqrt impl=fulldsp
  DT out = sqrt(val);
    return out;
}
               
template<typename DT>
static DT frecip_fabric(DT val) {
#pragma HLS BIND_OP variable=out op=frecip impl=fabric
  DT out = inv(val);
    return out;
}
               
template<typename DT>
static DT frecip_fulldsp(DT val) {
#pragma HLS BIND_OP variable=out op=frecip impl=fulldsp
  DT out = inv(val);
    return out;
}
               
template<typename DT>
static DT dexp_fabric(DT val) {
#pragma HLS BIND_OP variable=out op=dexp impl=fabric
  DT out = exp(val);
    return out;
}
               
template<typename DT>
static DT dexp_meddsp(DT val) {
#pragma HLS BIND_OP variable=out op=dexp impl=meddsp
  DT out = exp(val);
    return out;
}
               
template<typename DT>
static DT dexp_fulldsp(DT val) {
#pragma HLS BIND_OP variable=out op=dexp impl=fulldsp
  DT out = exp(val);
    return out;
}
               
template<typename DT>
static DT dlog_fabric(DT val) {
#pragma HLS BIND_OP variable=out op=dlog impl=fabric
  DT out = log(val);
    return out;
}
               
template<typename DT>
static DT dlog_meddsp(DT val) {
#pragma HLS BIND_OP variable=out op=dlog impl=meddsp
  DT out = log(val);
    return out;
}
               
template<typename DT>
static DT dlog_fulldsp(DT val) {
#pragma HLS BIND_OP variable=out op=dlog impl=fulldsp
  DT out = log(val);
    return out;
}
               
template<typename DT>
static DT dsqrt_fabric(DT val) {
#pragma HLS BIND_OP variable=out op=dsqrt impl=fabric
  DT out = sqrt(val);
    return out;
}
               
template<typename DT>
static DT drsqrt_fulldsp(DT val) {
#pragma HLS BIND_OP variable=out op=drsqrt impl=fulldsp
  DT out = sqrt(val);
    return out;
}
               
template<typename DT>
static DT drecip_fulldsp(DT val) {
#pragma HLS BIND_OP variable=out op=drecip impl=fulldsp
  DT out = inv(val);
    return out;
}
               
template<typename DT>
static DT hsqrt_fabric(DT val) {
#pragma HLS BIND_OP variable=out op=hsqrt impl=fabric
  DT out = sqrt(val);
    return out;
}
               