#!/usr/bin/env python3

import sys
from parser import *
from converter import *
from normalizer import *

def normalize_terms(terms_str):
    output_file = open(sys.argv[3], 'w')

    for t_str in terms_str:
        debruijn_term, free_vars = parse_term_to_deBruijn(t_str)

        normalized = normalize_subst_no(debruijn_term)

        result = deBruijn_to_normal(normalized, free_vars)

        output_file.write(str(result) +";\n")


def compare_term_pars(terms_str):
    output_file = open(sys.argv[3], 'w')

    closures = [parse_term_to_deBruijn(t_str) for t_str in terms_str]

    if len(closures) % 2 == 1:
        closures = closures[:-1]

    for i in range(0, len(closures), 2):
        clo1 = closures[i]
        clo2 = closures[i+1]

        res = beta_equal(clo1, clo2)

        output_file.write(str(res) + ";\n")

if __name__=="__main__":
    if len(sys.argv) <  4:
        print("./main normalize/compare input_file output_file")
        exit()

    input_file = open(sys.argv[2])

    terms_str = terms_strings(input_file.read())

    if sys.argv[1] == "normalize":
        normalize_terms(terms_str)
    elif sys.argv[1] == "compare":
        compare_term_pars(terms_str)
        