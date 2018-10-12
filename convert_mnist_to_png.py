#!/usr/bin/env python

import struct
import string
import sys
import png
import os

from array import array
from os import path


# source: http://abel.ee.ucla.edu/cvxopt/_downloads/mnist.py
def read(fname_img):
    #fname_img = os.path.join(path, 't10k-images-idx3-ubyte')
    #fname_lbl = os.path.join(path, 't10k-labels-idx1-ubyte')
    fname_lbl = fname_img.replace('images-idx3', 'labels-idx1')

    flbl = open(fname_lbl, 'rb')
    magic_nr, size = struct.unpack(">II", flbl.read(8))
    lbl = array("b", flbl.read())
    flbl.close()

    fimg = open(fname_img, 'rb')
    magic_nr, size, rows, cols = struct.unpack(">IIII", fimg.read(16))
    img = array("B", fimg.read())
    fimg.close()

    return lbl, img, size, rows, cols

def write_dataset(labels, data, size, rows, cols, output_dir):
    # create output directories
    output_dirs = [ path.join(output_dir, i) for i in string.lowercase ]
    print output_dirs
    for dir in output_dirs:
        if not path.exists(dir):
            os.makedirs(dir)

    # write data
    for (i, label) in enumerate(labels):
        output_filename = path.join(output_dirs[label-1], str(i) + ".png")
        print("writing " + output_filename)
        with open(output_filename, "wb") as h:
            w = png.Writer(cols, rows, greyscale=True)
            data_i = [
                data[ (i*rows*cols + j*cols) : (i*rows*cols + (j+1)*cols) ]
                for j in range(rows)
            ]
            data_j = [ [ None ] * len(data) ] * len(data_i[0])
            for j in range(len(data_i)):
                for k in range(len(data_i[j])):
                    data_j[j][k] = data_i[k][j]
            w.write(h, data_i)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: {0} <input_path> <output_path>".format(sys.argv[0]))
        sys.exit()

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    labels, data, size, rows, cols = read(input_path)
    write_dataset(labels, data, size, rows, cols,
                  path.join(output_path))
