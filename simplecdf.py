#!/usr/bin/env python3
# Script to generate a CDF graph from external file

import matplotlib.pyplot as plt
import numpy as np
import sys, argparse, statistics

parser = argparse.ArgumentParser(description='Make a CDF graph from data in the external file')
parser.add_argument('datafiles', type=str, nargs='+', help='File containing data')
parser.add_argument('--labels', type=str, nargs='+', help='Label of each datafile')
parser.add_argument('--column', type=int, default=0, help='Column index in the datafile containing data to be plotted')
parser.add_argument('--export', type=str, help='Filename of exported graph image')
parser.add_argument('--xlabel', type=str, default='data', help='Label of x axis')
parser.add_argument('--ylabel', type=str, default='CDF', help='Label of y axis')
parser.add_argument('--title', type=str, default='CDF Graph of Data', help='Title of the graph')
parser.add_argument('--caption', type=str, help='Caption below the graph')
args = parser.parse_args()

# Prepare the graph
fig = plt.figure()
graph = fig.add_axes((0.14, 0.21, 0.8, 0.7))

# Prepare the label
labels=[]
if args.labels is not None:
    for label in args.labels:
        labels.append(label)
if len(labels) < len(args.datafiles) and len(args.datafiles) > 1:
    temp = len(args.datafiles) - len(labels)
    for i in range(temp):
        labels.append("data"+str(i))

# Read data from datafiles
for i, datafile in enumerate(args.datafiles):
    data=[]
    for line in open(datafile):
        item = float(line.split()[args.column])
        data.append(item)

    # Prepare the data
    data.sort()
    n_bins = len(data)
    counts, bin_edges = np.histogram(data, bins=n_bins)
    cdf = np.cumsum(counts)

    # Print data characteristic
    print("data: " + str(datafile))
    print("- avg  : " + str(sum(data)/len(data)))
    print("- max  : " + str(data[len(data)-1]))
    print("- min  : " + str(data[0]))
    print("- stdv : " + str(statistics.stdev(data)))

    # Plot the cdf
    if len(labels) > 0:
        graph.plot(bin_edges[1:], cdf/cdf[-1], label=labels[i])
    else:
        graph.plot(bin_edges[1:], cdf/cdf[-1])

# Style the graph
graph.grid()
graph.set_title(args.title)
graph.set_ylabel(args.ylabel)
graph.set_xlabel(args.xlabel)
graph.set_ylim(0, 1.0)
graph.set_xlim(0.0, data[len(data)-1])
if len(labels) > 0:
    fig.legend()
if args.caption:
    fig.text(.5, .05, args.caption, ha='center')
plt.show()