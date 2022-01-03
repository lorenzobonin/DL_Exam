#!/usr/bin/python3

import numpy
import pandas
from sys import argv

def sigla2Province(sigla):
    if sigla == "TS":
        return "Trieste"
    elif sigla == "UD":
        return "Udine"
    elif sigla == "PN":
        return "Pordenone"
    elif sigla == "GO":
        return "Gorizia"
    else:
        return sigla

if __name__ == "__main__":
    basename = argv[1][:-4]

    province_col = "RETE"
    latitude_col = "LATITUDINE"
    if "Pollini" in basename:
        province_col = "PROVINCIA"
    elif "rifiuti" in basename:
        province_col = "Prov."
        latitude_col = "Latitudine"

    separator = ';'
    decimal = ','
    if "Aria" not in basename:
        separator = ','
        decimal = '.'


    dataset = pandas.read_csv(argv[1], sep=separator, decimal=decimal)
    for index, row in dataset.iterrows():
        if sigla2Province(row[province_col]) == "Udine":
            if float(row[latitude_col]) > 46.279:
                dataset.at[index, province_col] = "Udine_N"
            else:
                dataset.at[index, province_col] = "Udine_S"

    dataset.to_csv(basename + "_split.csv", index=False)
