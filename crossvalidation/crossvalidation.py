import argparse
import os
from pylab import *

def generate(infile, outdir, folds):
	"""
	"""
	pass

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