# Action Based Conversation Dataset

This repository handles the formatting of the ABCD dataset to conform to the proposed action annotation scheme in the paper "Implementing Actions as Tokens In
Large Language Models" (Honour J, 2025)

**NOTE: This repository uses the Git LFS for `abcd_v1.1.json`, ensure LFS is installed before cloning!**

# Setup

This repository requires no extra setup, any Python 3.x installation will suffice.

# Usage

To process the dataset and produce a formatted conversation jsonl file and tokens list, you can run `format.py`:

```bash
python format.py
```


# Original Work

The original ABCD dataset can be found here https://github.com/asappresearch/abcd this dataset modifies the dataset to our specified format.


# Original Citation
```
@inproceedings{chen2021abcd,
    title = "Action-Based Conversations Dataset: A Corpus for Building More In-Depth Task-Oriented Dialogue Systems",
    author = "Chen, Derek and
        Chen, Howard and
        Yang, Yi and
        Lin, Alex and
        Yu, Zhou",
    booktitle = "Proceedings of the 2021 Conference of the North American Chapter of the Association for 
    	Computational Linguistics: Human Language Technologies, {NAACL-HLT} 2021",
    month = jun,
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2021.naacl-main.239",
    pages = "3002--3017"
}
```

# Original Dataset License
```
MIT License

Copyright (c) 2021 ASAPP Research

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```