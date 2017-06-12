from __future__ import division
import random
import argparse
import sys
import os

parser = argparse.ArgumentParser()
parser.add_argument("input", help="input FASTQ filename")
parser.add_argument("-f", "--fraction", type=float, help="fraction of reads to sample")
parser.add_argument("-n", "--number", type=int, help="number of reads to sample")
parser.add_argument("-s", "--sample", type=int, help="number of output files to write", default=1)
args = parser.parse_args()

random.seed(12)

if args.fraction and args.number:
    sys.exit("give either a fraction or a number, not both")

if not args.fraction and not args.number:
    sys.exit("you must give either a fraction or a number")

print("counting records....")
with open(args.input) as inRead:
    num_lines = sum([1 for line in inRead])
if int(num_lines % 4) != 0:
    print("File Corrupted: Number of lines in FASTQ file not divisible by 4.")
    exit()
total_records = int(num_lines / 4)

if args.fraction:
    args.number = int(total_records * args.fraction)

number_to_sample = args.number

print("sampling " + str(number_to_sample) + " out of " + str(total_records) + " records")

fname = os.path.basename(args.input)

try:
    records_to_keep = set(random.sample(range(total_records + 1), number_to_sample))
    record_number = 0
    with open(args.input) as inFile:
        with open("subset_"+fname, "w") as output:
            for tag in inFile:
                bases = inFile.readline()
                sign = inFile.readline()
                quality = inFile.readline()
                if record_number in records_to_keep:
                    output.write(tag)
                    output.write(bases)
                    output.write(sign)
                    output.write(quality)
                record_number += 1
except ValueError as e:
    if str(e) != "Sample larger than population or is negative":
        raise
    else:
        print("Desired number of reads is greater than number of reads in original file.")
        print("No down-sampling is necessary.")
