#include <host_support.h>
#include <sys/stat.h>
#include <iostream>
#include <stdio.h>
#include <malloc.h>
#include <sys/time.h>
#include <CL/cl2.hpp>
#include <CL/cl_ext_xilinx.h>
#include "../../vitis-power/vitis-power/vitis-power.hpp"

// Datatype to use, must match the kernel datatype
// we typecast on the device
#define DATA_TYPE double
// Memory page size, ensures that memory is aligned to the boundary for performance
#define PAGESIZE 4096

static void write_to_csv(char * binary_filename, int run_id, int elements, float copy_on, float exec, float copy_off, double, double);
static void init_device(char*, int);
static void copy_on(cl::Event&);
static void execute_on_device(cl::Event&,cl::Event&);
static void copy_off(cl::Event&,cl::Event&,cl::Event&);
static void init_problem(int);
static float getTimeOfComponent(cl::Event&);

DATA_TYPE *input_data_1, *input_data_2, *result_data; // Input and result data

cl::CommandQueue * command_queue;
cl::Context * context;
cl::Program * program;
cl::Kernel * sum_kernel;
cl::Buffer *buffer_input_1, *buffer_input_2, *buffer_result; // Buffers to transfer to and from the device

int main(int argc, char * argv[]) {    
  cl::Event copyOnEvent, kernelExecutionEvent, copyOffEvent;
  double cardPowerAvgInWatt;

  if (argc != 4) {
    printf("You must supply two command line arguments, the bitstream file, the number of data elements and the run_id\n");
    return EXIT_FAILURE;
  }
  int data_size=atoi(argv[2]);
  int run_id=atoi(argv[3]);

  init_problem(data_size);
  init_device(argv[1], data_size);

  copy_on(copyOnEvent);
  bool stop_measurement = false;
  #pragma omp parallel shared(stop_measurement, cardPowerAvgInWatt, copyOnEvent, kernelExecutionEvent) num_threads(2)
  {
      int tid = omp_get_thread_num();
      if(tid == 0) {
        execute_on_device(copyOnEvent, kernelExecutionEvent);
      } else {
          cardPowerAvgInWatt = vitis_power::measureFpgaPower(stop_measurement);
          //cardPowerAvgInWatt = 9.99;
      }
      stop_measurement = true;
  }
  copy_off(copyOnEvent, kernelExecutionEvent, copyOffEvent);

  float kernelTime=getTimeOfComponent(kernelExecutionEvent);
  float copyOnTime=getTimeOfComponent(copyOnEvent);
  float copyOffTime=getTimeOfComponent(copyOffEvent);
  
  printf("Total runtime: %f ms, (%f ms xfer on, %f ms execute, %f ms xfer off) for %d elements; Avg card power: %f W; kernelTimeEnergy: %f J\n", copyOnTime+kernelTime+copyOffTime, copyOnTime, kernelTime, copyOffTime, data_size, cardPowerAvgInWatt, cardPowerAvgInWatt*(kernelTime/1000));    

  write_to_csv(argv[1], run_id, data_size, copyOnTime, kernelTime, copyOffTime, cardPowerAvgInWatt, cardPowerAvgInWatt*(kernelTime/1000));
 
  delete buffer_input_1;
  delete buffer_input_2;
  delete buffer_result;
  delete sum_kernel;
  delete command_queue;
  delete context;
  delete program;
  
  return EXIT_SUCCESS;
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
static void copy_on(cl::Event & copyOnEvent) {
  cl_int err;

  // Queue migration of memory objects from host to device (last argument 0 means from host to device)
  OCL_CHECK(err, err = command_queue->enqueueMigrateMemObjects({*buffer_input_1,*buffer_input_2}, 0, nullptr, &copyOnEvent));
  OCL_CHECK(err, err = command_queue->finish());
}

static void execute_on_device(cl::Event & copyOnEvent, cl::Event & kernelExecutionEvent) {
  cl_int err;

  // Queue kernel execution
  std::vector<cl::Event> kernel_wait_events;
  kernel_wait_events.push_back(copyOnEvent);
  OCL_CHECK(err, err = command_queue->enqueueTask(*sum_kernel, &kernel_wait_events, &kernelExecutionEvent));
  OCL_CHECK(err, err = command_queue->finish());
}

static void copy_off(cl::Event & copyOnEvent, cl::Event & kernelExecutionEvent, cl::Event & copyOffEvent) {
  cl_int err;

  // Queue copy result data back from kernel
  std::vector<cl::Event> data_transfer_wait_events;
  data_transfer_wait_events.push_back(kernelExecutionEvent);
  OCL_CHECK(err, err = command_queue->enqueueMigrateMemObjects({*buffer_result}, CL_MIGRATE_MEM_OBJECT_HOST, &data_transfer_wait_events, &copyOffEvent));

  // Wait for queue to complete
  OCL_CHECK(err, err = command_queue->finish());
}

/**
* Initiates the FPGA device and sets up the OpenCL context
*/
static void init_device(char * binary_filename, int data_size) {
  cl_int err;

  std::vector<cl::Device> devices;
  std::tie(program, context, devices)=initialiseDevice("Xilinx", "u280", binary_filename);

  // Create the command queue (and enable profiling so we can get performance data back)
  OCL_CHECK(err, command_queue=new cl::CommandQueue(*context, devices[0], CL_QUEUE_PROFILING_ENABLE, &err));
  // Create a handle to the sum kernel
  OCL_CHECK(err, sum_kernel=new cl::Kernel(*program, "krnl_bench", &err));
  // Allocate global memory OpenCL buffers that will be copied on and off
  OCL_CHECK(err, buffer_input_1=new cl::Buffer(*context, CL_MEM_USE_HOST_PTR  | CL_MEM_READ_ONLY, data_size * sizeof(DATA_TYPE), input_data_1, &err));
  OCL_CHECK(err, buffer_input_2=new cl::Buffer(*context, CL_MEM_USE_HOST_PTR  | CL_MEM_READ_ONLY, data_size * sizeof(DATA_TYPE), input_data_2, &err));
  OCL_CHECK(err, buffer_result=new cl::Buffer(*context, CL_MEM_USE_HOST_PTR  | CL_MEM_WRITE_ONLY, data_size * sizeof(DATA_TYPE), result_data, &err));

  // Set kernel arguments
  OCL_CHECK(err, err = sum_kernel->setArg(0, *buffer_input_1));
  OCL_CHECK(err, err = sum_kernel->setArg(1, *buffer_input_2));
  OCL_CHECK(err, err = sum_kernel->setArg(2, *buffer_result));  
  OCL_CHECK(err, err = sum_kernel->setArg(3, data_size));
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

  std::ofstream outFile;
  //outFile.open(outdir + "/runtime.csv", std::ios_base::trunc);
  outFile.open(outdir + "/runtime.csv", std::ios_base::app);
  
  outFile << ss.str();
  outFile.close();
}

