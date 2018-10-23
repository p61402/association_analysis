# Association Analysis

## Report

[Report Link](https://hackmd.io/s/r1_i3unom)

## Usage

### OSX virtual environment

```bash
source venv/bin/activate
python main.py -m [mode]
```

method|mode
:------:|:---:
Brute force|bf
Apriori|ap
FP-growth|fp

### Your own python3 interpreter

You need to install the following packages:

- pandas
- numpy
- mlxtend

Then type the command same as above.

```bash
python main.py -m [mode]
```

## Files

- **main.py** : Main file to execute the program.
- **brute_force.py** : Implement brute force algorithm.
- **apriori.py** : Implement apriori algorithm.
- **fp_growth.py** : Implement fp-growth algorithm.
- **preprocess.py** : Preprocessing dataset.
- **data.txt** : dataset