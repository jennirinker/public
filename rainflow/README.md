# rainflow
Rainflow cycle counts and ranges with Goodman correction

Notes  
-------  
The directory includes a module with the function (`rainflow.py`) and 
a demo script (`demo_rainflow.py`).  

`rainflow.py` contains a Python version of a [commonly used C script](https://github.com/WISDEM/AeroelasticSE/tree/master/src/AeroelasticSE/rainflow) 
that was written to work with a mex function for Matlab. The rainflow
function takes an array of turning points of a signal and returns an 
array of the load ranges, range mean, Goodman-adjusted cycle range with 
specified fixed-load mean, cycle count, and Goodman-adjusted cycle range
with zero fixed-load mean.  
  
Dependencies
------------  
Numpy >= v1.3
  
Usage
-----  
To call the function in a script on array of turning points `array_ext`:  
```python
import rainflow as rf  
array_out = rf.rainflow(array_ext)
```  

To run the demonstration from a Python console:  
`>>> execfile('demo_rainflow.py')`  
From the terminal (Windows or UNIX-based):  
`$ python demo_rainflow.py`  

Contacts  
--------  
Jennifer Rinker, jennifer.rinker@duke.edu.  
