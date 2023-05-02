# Changes made to the code

* `argparse` was added for parsing the arguments passed by the user
* Added a dictionary for generalizing the grading as a default parameter in the `percent2lettergrade` function
```
def percent2lettergrade(percentgrade, grading_boundaries={"A": 96, "A-": 91, "B+": 86, "B": 81, "B-": 76, "C+": 71, "C": 66, "C-": 61, "D+": 56, "D": 51}):
```

* Added `numpy` median function for computing the median function instead of the manually coded function `median_func`



