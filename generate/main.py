#!/bin/python

from generate import Generator

if __name__=="__main__":
    gen = Generator()
    gen.generate(csv_file="float_ops.csv")
    gen.generate_fixed_point_config("fixed_point_ops.csv")
    gen.generate(csv_file="fixed_point_ops.csv")