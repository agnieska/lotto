#!/usr/bin/env python
# coding: utf-8

import os
# import sys
# from pathlib import Path
import subprocess
from pprint import pprint
import pandas as pd
import numpy as np
import json
# from datetime import date
print("Import completed")


#############################################################
#           FUNCTIONS
#############################################################

def save_json(my_dict, filename):
    with open(filename, "w", encoding="utf-8") as file: #"iso8859-1"
        json.dump(my_dict, file, indent=2, allow_nan=False, ensure_ascii=False, sort_keys = True)


def load_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def list_files(path):
    ls = os.listdir(path)
    only_files = [f for f in ls if os.path.isfile(os.path.join(path, f))]
    # print (only_files)
    return only_files


def extract_html_list_content(HTML_path, year):
    first_line = 'class="lista_ostatnich_losowan"'
    last_line = '<!-- lista_ostatnich_losowan -->'
    filename = HTML_path + year + "-wyniki.html"
    with open(file=filename, mode="r", encoding="utf-8") as file:
        content = file.read()
    content = content.split(first_line)[1].split(last_line)[0]   
    return content


def extract_html_lists_elements(content):
    ul_list = content.split('</ul>')
    # print(len(ul_list))
    # print(ul_list[0])
    # print(ul_list[1])
    # print(ul_list[len(ul_list)-2])
    # print(ul_list[len(ul_list)-1])
    text = 'ul style="position: relative;">'
    ul_list = [el.split(text)[1] for el in ul_list if 'ul' in el]
    # print(len(ul_list))
    # print(ul_list[0])
    # print(ul_list[1])
    # print(ul_list[len(ul_list)-2])
    # print(ul_list[len(ul_list)-1])
    return ul_list


def extract_values_create_dict(ul_list):
    results_dict = {}
    results_list = []
    for ul in ul_list:
        li_list = ul.split('</li>')
        li_dict = {}
        li_dict['numbers'] = []
        for li in li_list:
            if 'numbers' in li:
                li_dict['numbers'].append(int(li.split('>')[1].strip().strip('.')))
            if 'date' in li:
                li_dict['date'] = li.split('>')[1].strip().strip('.')
            if 'nr' in li:
                li_dict['lp'] = int(li.split('>')[1].strip().strip('.'))
        # pprint(li_dict)
        results_list.append(li_dict)
        results_dict[li_dict['lp']] = li_dict
    return results_list, results_dict


def calcul_frequency (results_list):
    n = len(results_list)
    # frequency_list = list(np.zeros(50))
    # pprint(frequency_list)
    frequency_dict = {}
    percents_dict = {}
    for i in range(1, 50):
        frequency_dict[str(i)] = 0
        percents_dict[str(i)] = 0
    # pprint(frequency_dict)
    # pprint(percents_dict)
    for el in results_list:
        numbers = el['numbers']
        for number in numbers:
            #frequency_list[number] = frequency_list[number] + 1
            frequency_dict[str(number)] = frequency_dict[str(number)] + 1
    # print("Frequency calculated")
    # pprint(frequency_list)
    for number in frequency_dict:
        percents_dict[number] = frequency_dict[number]/n
    print("Percents calculated")
    # pprint(frequency_dict)
    return frequency_dict, percents_dict


def calcul_frequency_sorted (results_list):
    n = len(results_list)
    #frequency_list = list(np.zeros(50))
    # pprint(frequency_list)
    frequency_dict = {}
    for i in range(1, 50):
        frequency_dict[str(i)] = 0
    # pprint(frequency_dict)
    for el in results_list:
        numbers = el['numbers']
        for number in numbers:
            #frequency_list[number] = frequency_list[number] + 1
            frequency_dict[str(number)] = frequency_dict[str(number)] + 1
    # pprint(frequency_list)
    # pprint(frequency_dict)
    print("Frequency calculated")
    d = frequency_dict
    frequences = [(k , d[k]) for k in sorted(d, key=d.get, reverse=True)]
    print("Frequency list sorted")
    percents = [(k, round(d[k]/n,3)) for k in sorted(d, key=d.get, reverse=True)]
    print("Percents calculated and sorted")
    # pprint(frequences)
    # pprint(percents)
    return frequences, percents


##############################################
#               MAIN
##############################################

# define parameters
download_script = 'wget.sh'
HTML_path = "../HTML/"

# download html pages
if not os.path.isdir(HTML_path) or len(list_files(HTML_path)) == 0:
    subprocess.run(["sh", download_script])
    print("Pages html downloaded")
else:
    print("Pages html exist")

####################################################
# extract content

whole_results_dict = {}
whole_results_list = []
for i in range(1957, 2020):
    year = str(i)
    content = extract_html_list_content(HTML_path, year)
    ul_list = extract_html_lists_elements(content)
    results_list_year, results_dict_year = extract_values_create_dict(ul_list)
    # print("year: ", year, "dict :", len(results_dict_year),
    #    "list :", len(results_list_year))
    whole_results_dict.update(results_dict_year)
    whole_results_list.extend(results_list_year)
print("Nombre tirages liste :", len(whole_results_list))
print("Nombre tirages dict :", len(whole_results_dict))
df = pd.DataFrame(whole_results_list)
# print(df.shape)
# print(df.head(20))
df = pd.DataFrame(whole_results_dict).transpose()
# print(df.shape)
# print(df.head(20))
print("Values extracted")
save_json(whole_results_dict, "../lotto_values_d.json")
save_json(whole_results_list, "../lotto_values_l.json")
print("Values saved to json files")

##################################################
# calcul frequency and percents
whole_results_list = load_json("../lotto_values_l.json")
frequences, percents = calcul_frequency_sorted(whole_results_list)
print("The most often winning are :", frequences[0:20])
print("The less often winning are :", frequences[-20:])
