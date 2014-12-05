import argparse
import os
from pylab import *

def generate(infile, outdir, k):
	"""
	Generates the k-directories inside the outdir.
	It will then create four files in each directory:
	A train dataset and its interval file,
	and a validation dataset and its interval file.
	"""

	# Output for each fold
	out = [];

	# Prepare the output
	for i in range(k):
		out.append([]);

	# Open the input csv dataset
	with open(infile, newline='') as dataset:
		# Loop over all the examples
		data = dataset.readlines();

	# Get the base filename (basically, the dataset name)
	basefilename = os.path.basename(os.path.splitext(infile)[0]);

	# Get intervals
	intervals = set();
	for example in data:
		intervals.add(float(example.split(' ')[0]));
	intervals = [str(example) for example in sorted(intervals)];

	# Create the output directory if it does not exit
	if not os.path.exists(outdir):
		os.makedirs(outdir);

	# Write intervals
	intervalsname = os.path.join(outdir, basefilename + '.intervals');
	with open(intervalsname, 'w') as writefile:
		print('\r\n'.join(intervals), file=writefile);
		
	# Shuffle data
	shuffle(data);

	# Generate the k-folds
	folds = [data[i::k] for i in range(k)];
	
	# Write the datasets
	for i in range(k):
		# Validation set will be the current fold
		validation = folds[i];

		# Training set will be the examples in the rest of the folds
		training = [example for fold in folds if fold is not validation
					for example in fold];

		# Path for current fold
		path = os.path.abspath(os.path.join(outdir, 'fold'+str(i+1)));

		# Create the directory for the current fold
		if not os.path.exists(path):
			os.makedirs(path);

		# Prefix for the filenames
		filename = os.path.join(path, basefilename);

		# Write validation dataset
		with open(filename + '.valid.data', 'w') as writefile:
			print(''.join(validation), file=writefile);

		# Write training dataset
		with open(filename + '.train.data', 'w') as writefile:
			print(''.join(training), file=writefile);

	# No errors
	return 0;

def main():
	parser = argparse.ArgumentParser(description='Crossvalidation generator.');
	
	parser.add_argument('--input', '-i', dest='infile', required=True,
		help='input file in MTLR format.');
	parser.add_argument('--output', '-o', dest='outdir', required=True,
		help='output directory.');
	parser.add_argument('--folds', '-f', dest='folds', default=5,
		help='number of iterations for the crossvalidation.');

	# Parse the arguments
	args = parser.parse_args();
	
	# Generate the datasets
	return generate(args.infile, args.outdir, args.folds);


if __name__ == '__main__':
	main();