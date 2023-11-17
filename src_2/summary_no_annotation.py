#! /usr/bin/env python3
#! /usr/bin/Rscript
"""
Function utils to write the summary file to check data.
"""

import re


def create_summary(filter_splice, barcode_count):
    '''
    Function that run all sumary function.
    '''
    #for json data
    dict_sd_pos, dict_sa_pos,\
    nb_blocs, start_plot, dict_size_tsv, list_size_json, end_plot = distribution_spice_site(filter_splice)

    #for json data
    junction = junction_combinaison_graph(barcode_count)

    return dict_sd_pos, dict_sa_pos, nb_blocs, start_plot, dict_size_tsv, junction, list_size_json, end_plot


def distribution_spice_site(file):
    '''
    Function that plot the start position
    '''
    # check all start position columns 1
    start_pos = [0]*len(file)###filin)

    # All data for json file
    dict_sd_pos = {}
    dict_sa_pos = {}
    dict_nb_block = {}
    dict_start_plot = {}
    dict_end_plot = {}
    dict_size_tsv = {}
    list_size_json = []
    for index, line in enumerate(file):###filin):
        line = line.strip().split('\t')
        nb_block = int(line[-3])
        if nb_block not in dict_nb_block:
            dict_nb_block[nb_block] = 1
        else:
            dict_nb_block[nb_block] += 1

        size = sum(int(i) for i in line[-2].split(","))

        if size not in dict_size_tsv:
            dict_size_tsv[size] = 1
        else:
            dict_size_tsv[size] += 1

        list_size_json.append(size)

        #End position plot
        end = int(line[2])-1
        if end not in dict_end_plot:
            dict_end_plot[end] = 1
        else:
            dict_end_plot[end] += 1

        start = int(line[1])+1
        if start not in dict_start_plot:
            dict_start_plot[start] = 1
        else:
            dict_start_plot[start] += 1

        start_pos[index] = start
        start_genome = int(line[1])
        size_blocks = line[-2].split(",")
        starts_blocks = line[-1].split(",")
        end_genome = int(line[2])
        #SD
        for size_b, start_b in zip(size_blocks, starts_blocks):
            sd = start_genome+int(size_b)+int(start_b)
            if sd < end_genome:
                if sd not in dict_sd_pos:
                    dict_sd_pos[sd] = 1
                else:
                    dict_sd_pos[sd] += 1
        #SA
        for start_b in starts_blocks:
            if start_b != '0':
                sa = start_genome+1+int(start_b)
                if sa not in dict_sa_pos:
                    dict_sa_pos[sa] = 1
                else:
                    dict_sa_pos[sa] += 1

    return dict_sd_pos, dict_sa_pos, dict_nb_block, dict_start_plot, dict_size_tsv, list_size_json, dict_end_plot

def junction_combinaison_graph(path):
    """
    Function that generate junctions.
    """
    filin = []
    for key in path:
        # key_corrected: remove start and end position to only have junctions
        key_corrected = key.split("_")
        key_corrected = "_".join(key_corrected[1:-1])
        line = key_corrected+"_"+path[key]
        filin.append(line)
    junction = {}
    for line in filin:
        line = re.split("_|\t", line)
        # 2 blocks
        if len(line) == 3:
            count = int(line[-1].rstrip())
            new_line = line[0]+"_"+line[1]
            if new_line not in junction:
                junction[new_line] = count
            else:
                junction[new_line] += count
        # > 2 block
        else:
            count = int(line[-1].rstrip())
            for i in range(0, int(len(line)-1), 2):
                new_line = line[i]+"_"+line[i+1]
                if new_line not in junction:
                    junction[new_line] = count
                else:
                    junction[new_line] += count

    return junction
