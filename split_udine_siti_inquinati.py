#!/usr/bin/python3

import geocoder
import pandas as pd

polluted_sites = pd.read_csv("Data/Censimento_dei_siti_inquinati.csv", sep=';')
municipalities_clean = []
for municipality in polluted_sites["DENCOMUNE"].unique():
    if "," in municipality:
        for one_municipality in municipality.split(','):
            municipalities_clean.append(one_municipality.strip())
    else:
        municipalities_clean.append(municipality.strip())

municipalities_clean = list(set(municipalities_clean))

data = {'comune': municipalities_clean, 'provincia': ["" for mun in municipalities_clean]}
polluted_sites_split = pd.DataFrame(data)
for i, row in polluted_sites_split.iterrows():
    mun = row['comune']
    prov = ""
    if "Colloredo" in mun: # "Colloredo di m.te Albano" is not detected properly by OSM
        mun = "Colloredo di Monte Albano"
    coords = geocoder.osm("{}, Friuli - Venezia Giulia, Italia".format(mun))
    latitude = float(coords.osm['y'])
    string = str(coords[0])
    prov = string.split(',')[1].strip()
    if "Muggia" in mun: # OSM does not handle Muggia properly
        prov = "Trieste"
    if prov == "Udine":
        if latitude < 46.289:
            prov = "Udine_S"
        else:
            prov = "Udine_N"
    polluted_sites_split.at[i, 'provincia'] = prov

polluted_sites_split.to_csv("Data/Censimento_dei_siti_inquinati_split.csv")
