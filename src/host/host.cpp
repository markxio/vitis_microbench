#include <host_support.h>
#include <sys/stat.h>
#include <iostream>
#include <stdio.h>
#include <malloc.h>
#include <vector>
#include <sys/time.h>
#include <CL/cl2.hpp>
#include <CL/cl_ext_xilinx.h>
#include "vitis-power.hpp"

// Datatype to use, must match the kernel datatype
// we typecast on the device
#define DATA_TYPE double
// Memory page size, ensures that memory is aligned to the boundary for performance
#define PAGESIZE 4096

#define NUMBER_CUS 30
char *DEVICE_TYPE;
char *FP_TYPE;

char * getKernelName(const char * base, int index, char * buffer) {
  sprintf(buffer, "%s:{%s_%d}", base, base, index+1);
  return buffer;
}

static void write_to_csv(char * binary_filename, int run_id, int elements, float copy_on, float exec, float copy_off, double, double);
static void init_device(char*, int, int, bool&);
static void copy_on(std::vector<cl::Event>&, int, bool&);
static void execute_on_device(std::vector<cl::Event>&,std::vector<cl::Event>&, int);
static void copy_off(std::vector<cl::Event>&,std::vector<cl::Event>&,std::vector<cl::Event>&, int);
static void init_problem(int);
static float getTimeOfComponent(cl::Event&);
static void check_if_binary_op(const char *binary_filename, bool &binary_op);

DATA_TYPE *input_data_1, *input_data_2, *result_data; // Input and result data

cl::CommandQueue * command_queue;
cl::Context * context;
cl::Program * program;
cl::Kernel * sum_kernel[NUMBER_CUS];
cl::Buffer *buffer_input_1[NUMBER_CUS], *buffer_input_2[NUMBER_CUS], *buffer_result[NUMBER_CUS]; // Buffers to transfer to and from the device


int main(int argc, char * argv[]) {    
  if (argc != 7) {
    printf("You must supply the following command line arguments: the bitstream file, the number of data elements, run_id, device typ [u280|vck], number_cus and FP_TYPE\n");
    return EXIT_FAILURE;
  }

  int data_size=atoi(argv[2]);
  int run_id=atoi(argv[3]);
  DEVICE_TYPE=argv[4];
  int number_cus=atoi(argv[5]);
  FP_TYPE=argv[6];

  bool is_binary_op = false;
  check_if_binary_op(argv[1], is_binary_op);

  std::vector<cl::Event> copyOnEvent(NUMBER_CUS), kernelExecutionEvent(NUMBER_CUS), copyOffEvent(NUMBER_CUS);
  double cardPowerAvgInWatt;

  init_problem(data_size);
  init_device(argv[1], data_size, number_cus, is_binary_op);
  copy_on(copyOnEvent, number_cus, is_binary_op);
  
  bool stop_measurement = false;
  #pragma omp parallel shared(stop_measurement, cardPowerAvgInWatt, copyOnEvent, kernelExecutionEvent) num_threads(2)
  {
      int tid = omp_get_thread_num();
      if(tid == 0) {
        execute_on_device(copyOnEvent, kernelExecutionEvent, number_cus);
      } else {
          if (strstr(DEVICE_TYPE, "u280") != NULL) {
            cardPowerAvgInWatt = vitis_power::U280::measureFpgaPower(stop_measurement);
          } else if (strstr(DEVICE_TYPE, "vck") != NULL) {
            cardPowerAvgInWatt = vitis_power::VCK5000::measureFpgaPower(stop_measurement);
          } else {
            throw std::invalid_argument("DEVICE_TYPE not found");
          }
      }
      stop_measurement = true;
  }
  
  copy_off(copyOnEvent, kernelExecutionEvent, copyOffEvent, number_cus);

  float maxTotalTime=0.0;
  float maxKernelTime=0.0;
  float copyOnTime=0.0, copyOffTime=0.0;
  for (int i=0; i<number_cus; i++) {
      float kernelTime=getTimeOfComponent(kernelExecutionEvent[i]);
      copyOnTime=getTimeOfComponent(copyOnEvent[i]);
      copyOffTime=getTimeOfComponent(copyOffEvent[i]);
      float totalTime=copyOnTime+kernelTime+copyOffTime;
        
      if (totalTime > maxTotalTime) {
          maxTotalTime=totalTime;
      }
      if (kernelTime > maxKernelTime) {
          maxKernelTime=kernelTime;
      }

      printf("CU %d, Total runtime: %f ms, (%f ms xfer on, %f ms execute, %f ms xfer off) for %d elements; Avg card power: %f W; kernelTimeEnergy: %f J\n", i, copyOnTime+kernelTime+copyOffTime, copyOnTime, kernelTime, copyOffTime, data_size, cardPowerAvgInWatt, cardPowerAvgInWatt*(kernelTime/1000));    
  }
  printf("---------------------------------\n");
  printf("maxTotalTime: %f, maxKernelTime: %f\n", maxTotalTime, maxKernelTime);
  write_to_csv(argv[1], run_id, data_size, copyOnTime, maxKernelTime, copyOffTime, cardPowerAvgInWatt, cardPowerAvgInWatt*(maxKernelTime/1000));

  for (int i=0; i<NUMBER_CUS; i++) { 
      delete buffer_input_1[i];
      delete buffer_input_2[i];
      delete buffer_result[i];
      delete sum_kernel[i];
  }
  delete command_queue;
  delete context;
  delete program;
  
  return EXIT_SUCCESS;
}

static void check_if_binary_op(const char *binary_filename, bool &binary_op) {
  // check if binary_op, then one input
  // else if functions such as sqrt, then two inputs

  std::string add("add");
  std::string sub("sub");
  std::string mul("mul");
  std::string div("div");

  // Create a stringstream and a vector to hold the split parts
  // get the bitstream filename (stripped by any dirs)
  // e.g. dadd_fabric.hw.xclbin
  // instead of bin/multi/dadd_fabric.hw.xclbin
  std::string fname(binary_filename);
  std::istringstream ss(fname);
  std::string part;
  std::vector<std::string> parts;
  
  // Split by "/"
  while (std::getline(ss, part, '/')) {
      parts.push_back(part);
  }
  
  // Get the last part after the final separator
  std::string f = parts.back(); // bitstream filename

  if (f.find(add) != std::string::npos) {
    binary_op = true; 
    printf("substring %s found in string %s\n", add.c_str(), f.c_str());
  }
  if (f.find(sub) != std::string::npos) {
    binary_op = true; 
    printf("substring %s found in string %s\n", sub.c_str(), f.c_str());
  }
  if (f.find(mul) != std::string::npos) {
    binary_op = true; 
    printf("substring %s found in string %s\n", mul.c_str(), f.c_str());
  }
  if (f.find(div) != std::string::npos) {
    binary_op = true; 
    printf("substring %s found in string %s\n", div.c_str(), f.c_str());
  }

  // max number of CUs depends on number of supported hbm/ddr connections
  //if (binary_op and strstr(DEVICE_TYPE, "u280") != NULL) {
  //  NUMBER_CUS=16; // 32 hbm ports, two ports per kernel
  //} else if (!binary_op and strstr(DEVICE_TYPE, "u280") != NULL) {
  //  NUMBER_CUS=10; // 32 hbm ports, three ports per kernel
  //} else if (binary_op and strstr(DEVICE_TYPE, "vck") != NULL) {
  //  NUMBER_CUS=42; // assume 84 ddr ports, two ports per kernel
  //} else if (!binary_op and strstr(DEVICE_TYPE, "vck") != NULL) {
  //  NUMBER_CUS=28; // assume 84 ddr ports, three ports per kernel
  //}
  //
  //////////////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////
}

/**
* Retrieves the time in milliseconds of the OpenCL event execution
*/
static float getTimeOfComponent(cl::Event & event) {
  cl_ulong tstart, tstop;

  event.getProfilingInfo(CL_PROFILING_COMMAND_START, &tstart);
  event.getProfilingInfo(CL_PROFILING_COMMAND_END, &tstop);
  return (tstop-tstart)/1.E6;
}

/**
* Performs execution on the device by transfering input data, running the kernel, and copying result data back
* We use OpenCL events here to set the dependencies properly
*/
static void copy_on(std::vector<cl::Event> & copyOnEvent, int number_cus, bool &is_binary_op) {
  cl_int err;

  for (int i=0; i<number_cus; i++) {
      // Queue migration of memory objects from host to device (last argument 0 means from host to device)
      if (is_binary_op) {
        OCL_CHECK(err, err = command_queue->enqueueMigrateMemObjects({*buffer_input_1[i],*buffer_input_2[i]}, 0, nullptr, &copyOnEvent[i]));
      } else {
        OCL_CHECK(err, err = command_queue->enqueueMigrateMemObjects({*buffer_input_1[i]}, 0, nullptr, &copyOnEvent[i]));
      }
      //OCL_CHECK(err, err = command_queue->finish());
  }
}

static void execute_on_device(std::vector<cl::Event> & copyOnEvent, std::vector<cl::Event> & kernelExecutionEvent, int number_cus) {
  cl_int err;

  for (int i=0; i<number_cus; i++) {
      // Queue kernel execution
      std::vector<cl::Event> kernel_wait_events;
      kernel_wait_events.push_back(copyOnEvent[i]);
      OCL_CHECK(err, err = command_queue->enqueueTask(*sum_kernel[i], &kernel_wait_events, &kernelExecutionEvent[i]));
      //OCL_CHECK(err, err = command_queue->finish());
  }
}

static void copy_off(std::vector<cl::Event> & copyOnEvent, std::vector<cl::Event> & kernelExecutionEvent, std::vector<cl::Event> & copyOffEvent, int number_cus) {
  cl_int err;

  for (int i=0; i<number_cus; i++) {
      // Queue copy result data back from kernel
      std::vector<cl::Event> data_transfer_wait_events;
      data_transfer_wait_events.push_back(kernelExecutionEvent[i]);
      OCL_CHECK(err, err = command_queue->enqueueMigrateMemObjects({*buffer_result[i]}, CL_MIGRATE_MEM_OBJECT_HOST, &data_transfer_wait_events, &copyOffEvent[i]));
  }
  // Wait for queue to complete
  OCL_CHECK(err, err = command_queue->finish());
}

/**
* Initiates the FPGA device and sets up the OpenCL context
*/
static void init_device(char * binary_filename, int data_size, int number_cus, bool &is_binary_op) {
  cl_int err;
  char buffer[50];

  std::vector<cl::Device> devices;
  std::tie(program, context, devices)=initialiseDevice("Xilinx", DEVICE_TYPE, binary_filename); // vck, u280 

  // Create the command queue (and enable profiling so we can get performance data back)
  OCL_CHECK(err, command_queue=new cl::CommandQueue(*context, devices[0], CL_QUEUE_PROFILING_ENABLE, &err));

  for (int j=0; j<number_cus; j++) {
      // Create a handle to the sum kernel
      OCL_CHECK(err, sum_kernel[j]=new cl::Kernel(*program, getKernelName("krnl_bench", j, buffer), &err));
      // Allocate global memory OpenCL buffers that will be copied on and off
      OCL_CHECK(err, buffer_input_1[j]=new cl::Buffer(*context, CL_MEM_USE_HOST_PTR  | CL_MEM_READ_ONLY, data_size * sizeof(DATA_TYPE), input_data_1, &err));
      if (is_binary_op) {
        OCL_CHECK(err, buffer_input_2[j]=new cl::Buffer(*context, CL_MEM_USE_HOST_PTR  | CL_MEM_READ_ONLY, data_size * sizeof(DATA_TYPE), input_data_2, &err));
      }
      OCL_CHECK(err, buffer_result[j]=new cl::Buffer(*context, CL_MEM_USE_HOST_PTR  | CL_MEM_WRITE_ONLY, data_size * sizeof(DATA_TYPE), result_data, &err));

      // Set kernel arguments
      int i=0;
      OCL_CHECK(err, err = sum_kernel[j]->setArg(i++, *buffer_input_1[j]));
      if (is_binary_op) {
        OCL_CHECK(err, err = sum_kernel[j]->setArg(i++, *buffer_input_2[j]));
      }
      OCL_CHECK(err, err = sum_kernel[j]->setArg(i++, *buffer_result[j]));  
      OCL_CHECK(err, err = sum_kernel[j]->setArg(i++, data_size));
  }
}

/**
* Initialises the underlying input and result data (and ensures these are aligned to page boundaries for performance) along
* with setting the initial input data
*/
static void init_problem(int data_size) {
  input_data_1=(DATA_TYPE*) memalign(PAGESIZE, sizeof(DATA_TYPE) * data_size);
  input_data_2=(DATA_TYPE*) memalign(PAGESIZE, sizeof(DATA_TYPE) * data_size);
  result_data=(DATA_TYPE*) memalign(PAGESIZE, sizeof(DATA_TYPE) * data_size);
#pragma omp parallel for 
  for (int i=0;i<data_size;i++) {
    input_data_1[i]=(DATA_TYPE) i;
    input_data_2[i]=(DATA_TYPE) i;
  }
}

static void write_to_csv(char * binary_filename, int run_id, int elements, float copy_on, float exec, float copy_off, double power_watt, double energy_joule) {
  std::stringstream ss;
  if (run_id==0) {
    ss << "bitstream,run_id,elements,total_runtime_ms,copy_on_ms,execute_ms,copy_off_ms,power_w,energy_j" << std::endl;
  }

  ss << binary_filename << "," << run_id << "," << elements << "," << copy_on+exec+copy_off << "," << copy_on << "," << exec << "," << copy_off << "," << power_watt << "," << energy_joule << std::endl;

  std::string outdir = "output";
  struct stat buffer;
  if (stat(outdir.c_str(), &buffer) != 0) {
    if (mkdir(outdir.c_str(), 0777) != 0) {
      std::cout << "Output Directory (" << outdir << ") was NOT created!"
                << std::endl;
      exit(1);
    }   
  }   

  std::string device_type(DEVICE_TYPE);
  std::string fp_type(FP_TYPE);
  std::ofstream outFile;
  outFile.open(outdir + "/runtime_" + device_type + "_" + fp_type + ".csv", std::ios_base::app);
  
  outFile << ss.str();
  outFile.close();
}

