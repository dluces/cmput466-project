# cmput466-project

Contains three utilities for our CMPUT466 project.

  - [Parser](#parser)
  - [Cross Validation](#crossvalidation)
  - [Find C](#findc)

## parser

Converts a CSV dataset as found in the [pssp website](pssp.srv.ualberta.ca/predictors/public) to the format required by the [pssp software](http://pssp.srv.ualberta.ca/downloads/new).

### Usage

`$ python3 parser.py input_dataset.csv outputprefix`

This will read the `input_dataset.csv` file and output two files `outputprefix.data` with the converted dataset and `outputprefix.intervals` with the intervals file for the dataset.

## crossvalidation

Converts a CSV dataset as found in the [pssp website](pssp.srv.ualberta.ca/predictors/public) to the format required by the [pssp software](http://pssp.srv.ualberta.ca/downloads/new).

### Usage

`$ python3 crossvalidation.py [-h] --input INFILE --output OUTDIR [--folds FOLDS] [--intervals INTERVALS]`

```
arguments:
  -h, --help            show this help message and exit
  --input INFILE, -i INFILE
                        input file in MTLR format.
  --output OUTDIR, -o OUTDIR
                        output directory.
  --folds FOLDS, -f FOLDS
                        number of iterations for the crossvalidation.
  --intervals INTERVALS, -t INTERVALS
                        number of intervals to generate.
```

This will read the `INFILE` file as generated by the [parser](#parser) and outputs the following directory structure:

* `OUTDIR/{INFILE_base}.intervals`: Intervals file with `INTERVALS` number of timepoints.
* `OUTDIR/folds{fold}/{INFILE_base}.train.data`: Training dataset
* `OUTDIR/folds{fold}/{INFILE_base}.valid.data`: Validation dataset

Where `{fold}` is a number from 1 to `{FOLDS}` (so one directory per fold) and `{INFILE_base}` is the dataset name.

## findc

Tries to find the best C1 value to be used with a specific training dataset and prints it to `stdout`.

### Usage

`$ python3 findc.py [-h] --cross CVDIR --ds NAME [--folds FOLDS] [--start START] [--end END] [--mtlr MTLR] [--loss LOSS]`

```
arguments:
  -h, --help            show this help message and exit
  --cross CVDIR, -c CVDIR
                        directory with crossvalidation output (foldX
                        directories).
  --ds NAME, -n NAME    dataset name (not filename--so strip the .data).
  --folds FOLDS, -f FOLDS
                        number of iterations for the crossvalidation.
  --start START, -s START
                        the start of the range of possible C values.
  --end END, -e END     the end of the range of possible C values.
  --mtlr MTLR, -p MTLR  directory where the mtlr executables are located.
  --loss LOSS, -l LOSS  specific loss function to optimize for.
```

## TODO

* Create one single script in the root to run everything, given a input dataset.

## Version

0.0.1

## Installation

Just install python and run any of the utilities.
