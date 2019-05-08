# Framework for energy consumption estimation 
*The framework developed here intends to achieve an accurate prediction of energy consumption of **HPC** applications at runtime by extracting the signature of the application. This process requires mainly the use of a dynamic profiling and an static analysis of the source code*

**Note**: Current version is not finished, so part of the content may not be fulfilled

### Requirements
In order to use/modify anu module of the framework, it just requires the following knowledge:
* Basic understanding of Python
* Simple bash scripting
* Linux OS

### Supported Application Lamguages
Currently, only fortran is supported

### How to Use
The whole process can be executed just by running the following command on your Linux terminal located in the same directory as `main.py`:  
**Note:** Whole process is not yet available

 * `$: python main.py --source-code-directory --application-language`
 
 This command will execute the application stored in `nas_bt` directory. If you're willing to analyze your own application, just place it on the same directory and name it identically.
 
 Once the whole process has been performed, the results will be located under directory `results`.
 
 ### Step by Step
 The framework also provides the chance to execute every module independently. Let us see how:
 
 **Call Graph**  
 This module is in charge of retrieving the different paths the code may take all along the code. To check results, take a look at `results/cfg/`  
 **Note**: Currently, the module only works from python IDE(e.g. Spyder) and the paths are only stored in memory
 
 To execute the *call graph*, just run the following command on your Linux terminal:
 
 * `$: python call_graph.py`
 
 **Instruction Estimation**  
 In order to calculate the energy consumption, it is needed the total number of instructions over the code together with the number of instructions executed on each path, so we can calculate everything with the following command:
 **Note**: Highly recommended to be executed on python IDE. Not tested yet from command line
 
 * `$: python estimate_instructions.py`
 
 The module generates a file located on `results/instructions_estimation/total_instructions_per_function`
 
 **Application Signature**
 Its task is to generate and run the binary file of each path for a short period of time in order to get the counter metrics of the application to analyze at runtime.
 **Note**: So far, it only creates the binary files of each path. Working only on python IDE
 
 The module can be run on the command line like this:
 * `python xxx.py`
