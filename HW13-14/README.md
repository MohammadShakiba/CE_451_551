# GradeMaster

This package is used for grading the students based on their home work, midterm, and final scores. This code is originally made in Python2 by Prof. Johanes Hachmann and 
Dr. Mojtaba Haghighatlari. Here, I have modified and optimized the code. The modifications and changes are explained in more details in the [CHANGES.md](CHANGES.md) file.

The summary of the main changes are as follows:


* Optimization of the statistical approaches with numpy,

* Replacement of the optparse with argparse,

* Pandas optimization for reading the homeworks and exam data,

* Making the code work with Python3,

* Some other minor optimiaztions for printings with some ideas for generalization of some parts of the code


# Installation

You can install the code using the modified `makefile` even though this file is designed for other purposes but the installation can be done using:
```
python setup.py install
```


# Running the code

The code can be run using the following script:

```
cd grademaster/
python grademaster.py --data_file ../tests/grade_dummy_file_v2.csv --error_file error.log --logfile log.log

```

Or one can try the installed code in `build/lib/grademaster/grademaster.py`. Here, I used the latest `csv` file.

The variables that can be passed through the code are:
```
--data_file, specifies the name of the raw data file in CSV format...
--job_file, specifies the name of the job file that specifies sets...
--requestmeeting',specifies the a meeting is requested in the student email
--print_level, specifies the print level for on screen and the logfile
--logfile, specifies the name of the log-file
--error_file, specifies the name of the error-file
```



