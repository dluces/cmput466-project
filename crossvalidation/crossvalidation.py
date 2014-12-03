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
		
	# Shuffle data
	shuffle(data);

	# Generate the k-folds
	folds = [data[i::k] for i in range(k)];
	
	# Write the datasets
	for i in range(k):
		# Validation set will be the current fold
		validation = folds[i];

		# Validation intervals
		validationi = set();
		for example in validation:
			validationi.add(float(example.split(' ')[0]))
		validationi = [str(example) for example in sorted(validationi)];

		# Training set will be the examples in the rest of the folds
		training = [example for fold in folds if fold is not validation
					for example in fold];

		# Training intervals
		trainingi = set();
		for example in training:
			trainingi.add(float(example.split(' ')[0]))
		trainingi = [str(example) for example in sorted(trainingi)];

		# Path for current fold
		path = os.path.abspath(os.path.join(outdir, 'fold'+str(i+1)));

		# Create the directory for the current fold
		if not os.path.exists(path):
			os.makedirs(path)

		# Prefix for the filenames
		filename = os.path.basename(os.path.splitext(infile)[0]);
		filename = os.path.join(path, filename);

		# Write validation dataset
		with open(filename + '.valid.data', 'w') as writefile:
			print(''.join(validation), file=writefile);

		# Write validation intervals
		with open(filename + '.valid.intervals', 'w') as writefile:
			print('\r\n'.join(validationi), file=writefile);

		# Write training dataset
		with open(filename + '.train.data', 'w') as writefile:
			print(''.join(training), file=writefile);

		# Write training intervals
		with open(filename + '.train.intervals', 'w') as writefile:
			print('\r\n'.join(trainingi), file=writefile);

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