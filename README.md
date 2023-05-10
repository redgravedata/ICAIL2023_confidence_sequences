## Confidence Sequences for Evaluating One-Phase Technology-Assisted Review (Accepted at ICAIL 2023)
---
This repository is the official implementation of Confidence Sequences for Evaluating One-Phase Technology-Assisted Review. [this should be a link to the ArXiv paper]

We present a new evaluation approach for one-phase TAR workflows based on confidence sequences. Although the method is expensive in terms of sample size, it is plausible for large-scale reviews and has many opportunities for improvement.

We believe that our approach will be valuable to researchers and practitioners interested in evaluating the effectiveness of one-phase TAR workflows in the context of eDiscovery.

### Requirements
---
These experiments were conducted under
* Python 3.9
* Jupyter Notebook
* Required Libraries: csv, pandas, numpy, scipy, matplotlib, hashlib, copy, pickle, gzip

### Run
---
The original pickle files used in the experiment are not provided. Instead, the document orderings for each of the 9 document collections are provided in the data section of this repository as CSV files. These CSV files can be used to replicate the experiment in the WSR_and_URE_with_graphs.ipynb file. For transparency, the notebooks and Python modules used to create both the PRN numbers and documents orderings have been provided in the code section. 

All data referenced in the notebooks should be in the same directory to run the notebook properly. 

### Results
---
**95% two-sided confidence intervals on recall for OneShot/URE (dark) vs. our method (light)**

![Results Two-Sided Confidence Intervals](95_two-sided_conf_interval.jpg "95% two-sided confidence intervals on recall for OneShot/URE (dark) vs. our method (light) for post-review coding
effort from 100 to 25600 documents")

**95% lower one-sided confidence intervals on recall for OneShot/URE (dark) vs. skewed intervals for our method (light)**

![Results Lower One-Sided Confidence Intervals](95_lower_one-sided_conf_interval.jpg "95% lower one-sided confidence intervals on recall for OneShot/URE (dark) vs. skewed intervals for our method (light)")

