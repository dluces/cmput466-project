import sys
import csv

def parse(infile, outfile):
	"""
	Parses a CSV dataset (infile) and writes it in the format expected by the
	MTLR (outfile).
	"""
	out = [];
	intervals = [];
	first = True;

	# Open the input csv dataset
	with open(infile, newline='') as csvfile:
		# Read the input csv dataset
		reader = csv.reader(csvfile);

		# Loop over each line of the csv
		for row in reader:
			# Skip the headers
			if first:
				first = False;
				continue;

			# The parsed row will have the first two elements
			parsedrow = row[0:2];

			# Add the current interval
			if not float(row[0]) in intervals:
				intervals.append(float(row[0]));
			
			# Loop over the feature values
			for i in range(2, len(row)):
				# Validate that the feature has a value
				if float(row[i]) == 0:
					continue;

				# Append the feature
				parsedrow.append('{0}:{1}'.format(i-1, row[i]));

			# Send it to the output
			out.append(' '.join(parsedrow));

	# Sort the intervals
	intervals.sort();

	# Write intervals
	with open(outfile + '.intervals', 'w') as intervalsfile:
		print('\r\n'.join([str(interval) for interval in intervals]),
			file=intervalsfile);

	# Write dataset
	with open(outfile + '.data', 'w') as parsedfile:
		print('\r\n'.join(out), file=parsedfile);

	# No error
	return 0;

def main():
	if len(sys.argv) != 3:
		print('Usage: python3 parser.py inputfile outputfile');
		return 1;

	infile = sys.argv[1];
	outfile = sys.argv[2];
	return parse(infile, outfile);


if __name__ == '__main__':
	main();