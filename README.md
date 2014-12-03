# cmput466-project

Contains three utilities for our CMPUT466 project.

  - [Parser](#parser)
  - [Cross Validation](#crossvalidation)
  - [Find C](#findc)

## parser

Converts a CSV dataset as found in the [pssp website](pssp.srv.ualberta.ca/predictors/public) to the format required by the [pssp software](http://pssp.srv.ualberta.ca/downloads/new).

### Usage

`$ python parser.py input_dataset.csv outputprefix`

This will read the `input_dataset.csv` file and output two files `outputprefix.data` with the converted dataset and `outputprefix.intervals` with the intervals file for the dataset.

## crossvalidation

Converts a CSV dataset as found in the [pssp website](pssp.srv.ualberta.ca/predictors/public) to the format required by the [pssp software](http://pssp.srv.ualberta.ca/downloads/new).

### Usage

`$ python crossvalidation.py [-h] --input INFILE --output OUTDIR [--folds FOLDS]`

```
arguments:
  -h, --help            show this help message and exit
  --input INFILE, -i INFILE
                        input file in MTLR format.
  --output OUTDIR, -o OUTDIR
                        output directory.
  --folds FOLDS, -f FOLDS
                        number of iterations for the crossvalidation.`
```

This will read the `INFILE` file as generated by the [parser](#parser) and output `FOLDS` number of directories in the `OUTDIR` directory. Each of these created directories will contain four files:

* `INFILE_with_no_extension.train.data`: Train dataset
* `INFILE_with_no_extension.train.intervals`: Intervals file for the train dataset
* `INFILE_with_no_extension.test.data`: Test dataset
* `INFILE_with_no_extension.test.intervals`: Intervals file for the test dataset

## findc

In progress.

## TODO

* Create one single script in the root to run everything, given a input dataset.

## Version

0.0.1

## Installation

Just install python and run any of the utilities.