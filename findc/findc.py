import argparse
import os
import subprocess
from pylab import *

mtlr_train = 'mtlr_train';
mtlr_test = 'mtlr_test';
model_temp = './model.tmp';
train_data = None;
test_data = None;
intervals_file = None;
intervals_number = 0;
cv_dirs = [];

def findc(k, start, end, loss):
	"""
	Simple way to find the best C1 value, using k-fold cross validation. 
	This uses a binary search approach to find the best C1 value.
	"""

	global intervals_file, intervals_number;

	# Get the number of intervals
	intervals_number = sum(1 for _ in open(intervals_file, 'rbU'));

	# Set the minimum
	basec = start;

	# calculate the start-point c and its error
	minc = start;
	minerror = testc(start, k, loss);

	# Binary search
	while (start < end and (end - start) > 0.05):
		# calculate the mid-point c and its error
		midc = float((start+end)/2);
		miderror = testc(midc, k, loss);

		# If the mid-point error is lower (or equal)
		# (this will prefer larger C values with the same error)
		if miderror <= minerror:
			# The mid-point will be the new minimum
			minc = midc;
			minerror = miderror;

			# Print it
			print("*C: {0}, error: {1}".format(minc, minerror));

			# We advance towards the end
			start = minc;

		# If the mid-point error is higher
		else:
			# We move the end to the mid-point
			end = midc;
	
	# Print the best C
	print("*C: {0}, error: {1}".format(minc, minerror));

	# No errors
	return 0;

def testc(c, k, loss):
	"""
	Tests a C using crossvalidation
	"""
	
	global mtlr_test, mtlr_train, model_temp;
	global train_data, test_data;
	global intervals_file, intervals_number;
	global cv_dirs;

	# Build the base command for training
	base_train = [mtlr_train, '-d', '0']; # Command and c1
	base_train += ['-m', str(intervals_number)]; # Add time points
	base_train += ['-q', intervals_file]; # Intervals
	base_train += ['-o', model_temp]; # Output

	# Build the base command for testing
	base_test = [mtlr_test, '-l', loss]; # Command and loss fn
	base_test += ['-m', str(intervals_number)]; # Add time points
	base_test += ['-q', intervals_file]; # Intervals
	base_test += ['-o', model_temp]; # Model

	# Array of errors returned
	errors = [];

	# Check if the crossvalidation dataset and interval files exist
	for currentdir in cv_dirs:
		# Get the current fold train and validation datasets
		traindata = os.path.join(currentdir, train_data);
		testdata = os.path.join(currentdir, test_data);
		
		# Form the current training command
		current_train = base_train.copy();
		current_train += ['-i', traindata]; # Training data
		current_train += ['-c', str(c)]; # Current C

		# Form the current testing command
		current_test = base_test.copy();
		current_test += ['-i', testdata]; # Testing data
		
		# Train the model
		subprocess.call(current_train, stdout=subprocess.DEVNULL);

		# Test the model
		out = subprocess.check_output(current_test);

		# Parse the output to get the error
		out = out.decode('ascii');
		out = out[out.index("l2-log-"):out.index("\n#avg log-like")];

		# Append the error
		errors.append(float(out.split(' ')[1]));

	print(" C: {0}, error: {1}".format(c, mean(errors)));

	# No errors
	return mean(errors);

def main():
	global mtlr_test, mtlr_train;
	global train_data, test_data;
	global intervals_file, intervals_number;
	global cv_dirs;

	parser = argparse.ArgumentParser(description='Finds the best C param.');
	
	parser.add_argument('--cross', '-c', dest='cvdir', required=True,
		help='directory with crossvalidation output (foldX directories).');
	parser.add_argument('--ds', '-n', dest='name', required=True,
		help='dataset name (not filename--so strip the .data).');
	parser.add_argument('--folds', '-f', dest='folds', default=5,
		help='number of iterations for the crossvalidation.');
	parser.add_argument('--start', '-s', dest='start', default=1,
		help='the start of the range of possible C values.');
	parser.add_argument('--end', '-e', dest='end', default=100,
		help='the end of the range of possible C values.');
	parser.add_argument('--mtlr', '-p', dest='mtlr', default='.',
		help='directory where the mtlr executables are located.');
	parser.add_argument('--loss', '-l', dest='loss', default='l2_log',
		help='specific loss function to optimize for.');

	# Parse the arguments
	args = parser.parse_args();
	
	# Get the mtlr executables filenames
	mtlr_train = os.path.join(args.mtlr, 'mtlr_train');
	mtlr_test = os.path.join(args.mtlr, 'mtlr_test');

	# Check the mtlr_train executable
	if not os.path.isfile(mtlr_train):
		print("Error: {0} is not a file".format(mtlr_train));
		return -1;

	# Check the mtlr_test executable
	if not os.path.isfile(mtlr_test):
		print("Error: {0} is not a file".format(mtlr_test));
		return -2;

	# Get the training filenames
	train_data = args.name + '.train.data';
	test_data = args.name + '.valid.data';
	
	# Check if the crossvalidation dataset and interval files exist
	for i in range(int(args.folds)):
		# Get the current fold name
		currentfold = "fold" + str(i+1);

		# Get the current fold directory
		currentdir = os.path.abspath(os.path.join(args.cvdir, currentfold));

		# Add the current fold directory to the array
		cv_dirs.append(currentdir);

		# Get the current fold filenames
		traindata = os.path.join(currentdir, train_data);
		testdata = os.path.join(currentdir, test_data);
		
		# Check the training files
		if not os.path.isfile(traindata):
			print("Error: Train files missing in {0}".format(currentdir));
			return -3;

		# Check the training files
		if not os.path.isfile(testdata):
			print("Error: Test files missing in {0}".format(currentdir));
			return -4;

	# Get the intervals filename
	intervals_file = os.path.join(args.cvdir, args.name + '.intervals');
	
	# Check the intervals file
	if not os.path.isfile(intervals_file):
		print("Error: Interval file missing: {0}".format(intervals_file));
		return -5;

	# Find the best C
	return findc(args.folds, float(args.start), float(args.end), args.loss);


if __name__ == '__main__':
	main();