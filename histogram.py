#!/usr/bin/env python

import sys
import argparse
import matplotlib.pyplot as plt
import numpy as np
from os.path import basename

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    description='Examine stdin for numbers and plot them in a histogram.')

parser.add_argument(
    '--bins', default=10, type=int,
    help='The number of bins in the histogram.')

parser.add_argument(
    '--save', help='A file name to save an image to.')

parser.add_argument(
    '--noShow', dest='show', action='store_false',
    help='If given, do not automatically show the histogram image.')

parser.add_argument(
    '--addN', action='store_true',
    help='Add (n=XXX) to the title.')

parser.add_argument(
    '--x', default='Count', help='X axis label.')

parser.add_argument(
    '--y', default='Frequency', help='Y axis label.')

parser.add_argument(
    '--title', default='Histogram', help='Histogram title.')

parser.add_argument(
    '--reportNonNumeric', action='store_true',
    help='Report input fields that are not numeric')

parser.add_argument(
    '--printNumbers', action='store_true',
    help='Print numbers found on standard input, one per line.')

args = parser.parse_args()

if not (args.save or args.show):
    print('%s: You are neither showing nor saving the histogram... '
          'nothing to do!' % basename(sys.argv[0]), file=sys.stderr)
    sys.exit(1)

x = []
append = x.append

# Save anything on stdin that looks like a number.
for line in sys.stdin:
    for value in line.split():
        numericValue = None
        try:
            numericValue = int(value)
        except ValueError:
            try:
                numericValue = float(value)
            except ValueError:
                if args.reportNonNumeric:
                    print(f'Non-numeric{value!r} found.', file=sys.stderr)

        if numericValue is not None:
            append(numericValue)
            if args.printNumbers:
                print(value)

fig, ax = plt.subplots()
ax.hist(x, bins=args.bins)

mean = np.mean(x)
std = np.std(x)
median = np.median(x)

ax.axvline(x=mean, linewidth=1, color='#aaa')
ax.axvline(x=median, linewidth=1, color='#999', linestyle='dotted')

ax.set_xlabel(args.x, fontsize=9)
ax.set_ylabel(args.y, fontsize=9)
ax.set_title(
    args.title +
    (f'\nn={len(x)}, mean={mean:.2f}, median={median:.2f}, std={std:.2f}'
     if args.addN else ''),
    fontsize=11)

if args.save:
    fig.savefig(args.save)

if args.show:
    plt.show()
