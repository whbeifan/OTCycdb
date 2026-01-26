#!/usr/bin/env python
#coding:utf-8

import os
import re
import sys
import logging
import argparse

from collections import OrderedDict

LOG = logging.getLogger(__name__)

__version__ = "1.1.0"
__author__ = ("Xingguo Zhang",)
__email__ = "invicoun@foxmail.com"
__all__ = []


def read_kofamscan(file):

    if file.endswith(".gz"):
        fh = gzip.open(file)
    else:
        fh = open(file)

    for line in fh:
        if not line or line.startswith("#"):
            continue
        line = line.strip().split("\t")

        yield line

    fh.close()


def get_kofamscan2best(file, evalue=1e-5):

    r = OrderedDict()
    for line in read_kofamscan(file):
        if line[0] == "*":
            temp = line[1::]
            r[temp[0]] = temp
        else:
            if float(line[4]) >= evalue:
                continue
            score = float(line[3])
            if line[0] in r:
                temp = r[line[0]]
                if float(temp[3]) <= score:
                    r[line[0]] = line
                else:
                    continue
            else:
                r[line[0]] = line

    print("#Seq Id\tKO\tScore\tE-value\tKO definition")
    for i in r:
        line = r[i]
        print("%s\t%s\t%s\t%s\t%s" % (line[0], line[1], line[3], line[4], line[5]))
    
    return 0


def add_help_parser(parser):

    parser.add_argument("input", metavar="FILE", type=str, 
        help="Input the kofamscan2 database annotation results")
    parser.add_argument("-ev", "--evalue", metavar="FLOAT", type=float, default=1e-5,
        help="Set the filter to exclude results with an E-value greater than this, default=1e-5")

    return parser



def main():

    logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO,
        format="[%(levelname)s] %(message)s"
    )
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
    description='''
name:
     get_kofamscan2best.py: 获取kofamscan注释的最优结果

attention:
     get_kofamscan2best.py kofamscan.tsv  >KEGG.tsv
''')
    args = add_help_parser(parser).parse_args()
    get_kofamscan2best(args.input, evalue=args.evalue)


if __name__ == "__main__":

    main()
