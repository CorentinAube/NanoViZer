#! /usr/bin/env python3
"""
Function utils for main_bis_clean.py to select files.
"""

import os
import subprocess
import shutil

def create_folder(result_folder):
    '''
    Create all folders.
    '''
    # create result_folder if not exist to write file
    if os.path.exists(result_folder):
        shutil.rmtree(result_folder)
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)
    remove_folder = result_folder+"remove_reads/"
    if not os.path.exists(remove_folder):
        os.makedirs(remove_folder)
    us_folder = result_folder+"one_block_reads/"
    if not os.path.exists(us_folder):
        os.makedirs(us_folder)
    ss_folder = result_folder+"spliced_seq/"
    if not os.path.exists(ss_folder):
        os.makedirs(ss_folder)
    """
    remove_folder = result_folder+"barcode/"
    if not os.path.exists(remove_folder):
        os.makedirs(remove_folder)
    remove_folder = result_folder+"fastq/"
    if not os.path.exists(remove_folder):
        os.makedirs(remove_folder)
    """

def clean_bam_name(bam_name):
    """
    Function that check if there not .bam at the end of the file name.
    """
    if bam_name.endswith(".bam"):
        return bam_name[:-4]
    else:
        return bam_name


def bedfile_gen2(bam_name):
    '''
    Function that launch deeptools if the file was not already processed.
    '''
    bed_name_list = os.listdir("../data/")
    #if bam_name+".bam" not in bed_name_list:
    #    exit()
    if bam_name+".bed" not in bed_name_list:
        folder = "../data/"
        bam = bam_name+".bam"
        bed = bam_name+".bed"
        shell_line = f"./Bed_gen_v3.sh {folder} {bam} {bed}"
        subprocess.run(shell_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #os.system(shell_line)


def list_virus_cell_bed(list_bed_file):
    """
    Function that allows to create a list of bed file of virus,
    cell or complet kind of reads.
    """
    # list of the _cell.bed
    cell_bed_file = [file for file in list_bed_file if "_cell.bed" in file]
    # list of the _virus.bed
    virus_bed_file = [file for file in list_bed_file if "_virus.bed" in file]

    return cell_bed_file, virus_bed_file


def virus_bed_gen(genome_name, bam_name):
    """
    Function that keep only reads that are aligned on viral genome
    by parsing column 0 of the Bed file.

    The genome name can be give or not and a search by key word to remove
    human read are applied.
    """
    pathin = f"../data/{bam_name}.bed"
    """
    if genome_name is None:
        host = ["1", "2", "3", "4", "5","6", "7", "8", "9", "10", "11",
            "12", "13","14","15","16","17","18","19","20","21","22",
            "X", "x", "Y", "y","mt","MT"]
        with open(pathin, "r", encoding="utf-8") as filin:
            filin = filin.readlines()
            new_filin = []
            for line in filin:
                line_split = line.split('\t')
                if line_split[0] not in host:
                    new_filin.append(line)

        return new_filin

    else:
    """
    with open(pathin, "r", encoding="utf-8") as filin:
        filin = filin.readlines()
        new_filin = []
        all_oneblock_read = []
        for line in filin:
            all_oneblock_read.append(line)
            line_split = line.split('\t')
            if genome_name == line_split[0]:
                new_filin.append(line)

    return new_filin, all_oneblock_read

def json_gen(dict_sd_pos, dict_sa_pos, nb_blocs, start_plot, list_size_json,\
             junction, dict_count_ss, count_read, genome_size, end_plot):# , one_block_data):
    """
    Function to generate json data and return to Nanovizer that
    return to flask.py
    """
    list_data = [dict_sd_pos, dict_sa_pos, nb_blocs, start_plot, list_size_json,\
                 junction, dict_count_ss, end_plot, count_read]

    list_dedict_sd = []
    list_dedict_sa = []
    list_dedict_block = []
    list_dedict_start = []
    list_dedict_end = []
    list_dedict_size = []
    list_dedict_junction = []
    list_dedict_barcode = []
    new_count_read = {}
    for index, _ in enumerate(list_data):
        if index == 0:
            for key in dict_sd_pos:
                dict_data = {key:dict_sd_pos[key]}
                list_dedict_sd.append(dict_data)
        if index == 1:
            for key in dict_sa_pos:
                dict_data = {key:dict_sa_pos[key]}
                list_dedict_sa.append(dict_data)
        if index == 2:
            for key in nb_blocs:
                dict_block = {key:nb_blocs[key]}
                list_dedict_block.append(dict_block)
        if index == 3:
            for key in start_plot:
                dict_start = {key:start_plot[key]}
                list_dedict_start.append(dict_start)
        if index == 4:
            for key in list_size_json:
                #dict_size = {"size":key}
                #list_dedict_size.append(dict_size)
                list_dedict_size.append(key)
        if index == 5:
            for key in junction:
                key_list = key.split("_")
                #dict_junction = {"junction":key, "count":junction[key]}
                dict_junction = {"3_prime":int(key_list[0]), "5_prime":int(key_list[1]),\
                                 "count":int(junction[key])}
                list_dedict_junction.append(dict_junction)
        if index == 6:
            for key in dict_count_ss:
                new_key = f"1_{key}_{str(genome_size)}"
                #dict_junction = {new_key:dict_count_ss[key]}
                dict_junction = {key:dict_count_ss[key]}    #retire juste le 1 et le end
                list_dedict_barcode.append(dict_junction)

        if index == 7:
            for key in end_plot:
                dict_end = {key:end_plot[key]}
                list_dedict_end.append(dict_end)

        #summary_read = count_read | one_block_data

    data = {"3_prime_count": list_dedict_sd,
            "5_prime_count" : list_dedict_sa,
            "block_count" : list_dedict_block,
            "start_site_count" : list_dedict_start,
            "end_site_count" : list_dedict_end,
            "read_size" : list_dedict_size,
            "junction_count" : list_dedict_junction,
            "barcode_count" : list_dedict_barcode,
            "read_summary_count" : count_read}#,
            #"read_summary_count" : summary_read}
    return data


def data_export(dict_sd_pos, dict_sa_pos, nb_blocs, start_plot, list_size,\
                junction, dict_count_ss, count_read, result_folder, end_plot):
    """
    Function to export data into a tsv file for downoal them.
    """
    filename = result_folder+"5prime_site.tsv"
    with open(filename, "w", encoding="utf-8") as filout:
        line_1 = "5prime_site\tCount\n"
        filout.write(line_1)
        for key in dict_sd_pos:
            new_line = f'{key}\t{dict_sd_pos[key]}\n'
            filout.write(new_line)

    filename = result_folder+"3prime_site.tsv"
    with open(filename, "w", encoding="utf-8") as filout:
        line_1 = "3prime_site\tCount\n"
        filout.write(line_1)
        for key in dict_sa_pos:
            new_line = f'{key}\t{dict_sa_pos[key]}\n'
            filout.write(new_line)

    filename = result_folder+"number_of_blocks.tsv"
    with open(filename, "w", encoding="utf-8") as filout:
        line_1 = "number_of_blocks\tCount\n"
        filout.write(line_1)
        for key in nb_blocs:
            new_line = f'{key}\t{nb_blocs[key]}\n'
            filout.write(new_line)

    filename = result_folder+"start_site.tsv"
    with open(filename, "w", encoding="utf-8") as filout:
        line_1 = "start_site\tCount\n"
        filout.write(line_1)
        for key in start_plot:
            new_line = f'{key}\t{start_plot[key]}\n'
            filout.write(new_line)

    filename = result_folder+"end_site.tsv"
    with open(filename, "w", encoding="utf-8") as filout:
        line_1 = "end_site\tCount\n"
        filout.write(line_1)
        for key in end_plot:
            new_line = f'{key}\t{end_plot[key]}\n'
            filout.write(new_line)

    filename = result_folder+"read_size.tsv"
    with open(filename, "w", encoding="utf-8") as filout:
        line_1 = "size\tCount\n"
        filout.write(line_1)
        for key in list_size:
            new_line = f'{key}\t{list_size[key]}\n'
            filout.write(new_line)

    filename = result_folder+"junction.tsv"
    with open(filename, "w", encoding="utf-8") as filout:
        line_1 = "junction\tCount\n"
        filout.write(line_1)
        for key in junction:
            new_line = f'{key}\t{junction[key]}\n'
            filout.write(new_line)

    filename = result_folder+"barcode.tsv"
    with open(filename, "w", encoding="utf-8") as filout:
        line_1 = "barcode\tCount\n"
        filout.write(line_1)
        for key in dict_count_ss:
            new_line = f'{key}\t{dict_count_ss[key]}\n'
            filout.write(new_line)
   
    filename = result_folder+"read_count.tsv"
    with open(filename, "w", encoding="utf-8") as filout:
        line_1 = "Category\tCount\n"
        filout.write(line_1)
        for category in count_read:
            new_line = f'{category}\t{count_read[category]}\n'
            filout.write(new_line)
