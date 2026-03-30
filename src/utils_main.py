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
    ss_folder = result_folder+"spliced_reads/"
    if not os.path.exists(ss_folder):
        os.makedirs(ss_folder)


def log_file_gen(result_folder, file_name, genome_name, genome_size, passthrough, min_3_end,\
                max_3_end, min_read_length, max_5_start, genome_file_name, min_5_start):
    """
    Create the log to save all the parameters for the analysis.
    """
    file = result_folder+"log_file.txt"
    with open(file, "w") as filin:
        new_line = 'file_name: {0}\ngenome_name: {1}\ngenome_size: {2}\n\
5prime_mini: {3}\npassthrough: {4}\n3prime_mini: {5}\n\
3prime_max: {6}\n5prime_max: {8}\n\
min_read_length: {7}\ngenome_file_name: {9}'.format(file_name, genome_name, genome_size, min_5_start, passthrough, min_3_end, max_3_end, min_read_length, max_5_start, genome_file_name)
        filin.write(new_line)
    

def clean_bam_name(bam_name):
    """
    Function that check if there not .bam at the end of the file name.
    """
    if bam_name.endswith(".bam"):
        return bam_name[:-4]
    else:
        return bam_name


def bedfile_gen(file_name):
    '''
    Function that launch deeptools to generate the bed file
    if the file was not already processed.
    '''
    bed_name_list = os.listdir("../data/")
    if file_name+".bed" not in bed_name_list:
        folder = "../data/"
        bam = file_name+".bam"
        bed = file_name+".bed"
        shell_line = f"./Bed_gen_v3.sh {folder} {bam} {bed}"
        subprocess.run(shell_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def genome_nam_gen(file_name, result_folder):
    """
    Function that return all the genome names present in the Bedfile to help
    the user if he does not know the genome name used for the mapping.
    """
    pathin = f"../data/{file_name}.bed"
    filout = result_folder+"genome_name.tsv"
    genome = []
    with open(pathin, "r", encoding="utf-8") as filin, open(filout, "w") as filout:
        filin = filin.readlines()
        for line in filin:
            line_split = line.split('\t')
            if line_split[0] not in genome:
                genome.append(line_split[0])
        line = "Genomes found in the bam file\n"
        filout.write(line)
        list_genome = "\n".join(genome)
        filout.write(list_genome)

    
def virus_bed_gen(genome_name, file_name):
    """
    Function that keep only reads that are aligned on viral genome
    by parsing column 0 of the Bed file.
    """
    pathin = f"../data/{file_name}.bed"

    with open(pathin, "r", encoding="utf-8") as filin:
        filin = filin.readlines()
        new_filin = []
        for line in filin:
            line_split = line.split('\t')
            if genome_name == line_split[0]:
                new_filin.append(line)

    return new_filin

def json_gen(dict_ds_pos, dict_as_pos, nb_blocs, start_plot, list_size_json,\
             junction, dict_count_ss, count_read, end_plot,\
             untruncated_pos_count, genome_size):
    """
    Function that generates a JSON file.
    """
    list_data = [dict_ds_pos, dict_as_pos, nb_blocs, start_plot, list_size_json,\
                 junction, dict_count_ss, count_read, end_plot, untruncated_pos_count]

    list_dedict_ds = []
    list_dedict_as = []
    list_dedict_block = []
    list_dedict_start = []
    list_dedict_end = []
    list_dedict_size = []
    list_dedict_junction = []
    list_dedict_barcode = []
    list_dedict_untruncated_pos = []
    for index, _ in enumerate(list_data):
        if index == 0:
            for key in dict_ds_pos:
                dict_data = {key:dict_ds_pos[key]}
                list_dedict_ds.append(dict_data)
        if index == 1:
            for key in dict_as_pos:
                dict_data = {key:dict_as_pos[key]}
                list_dedict_as.append(dict_data)
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
                list_dedict_size.append(key)
        if index == 5:
            for key in junction:
                key_list = key.split("_")
                dict_junction = {"3_prime":int(key_list[0]), "5_prime":int(key_list[1]),\
                                 "count":int(junction[key])}
                list_dedict_junction.append(dict_junction)
        if index == 6:
            for key in dict_count_ss:
                dict_junction = {key:dict_count_ss[key]}
                list_dedict_barcode.append(dict_junction)

        if index == 7:
            for key in end_plot:
                dict_end = {key:end_plot[key]}
                list_dedict_end.append(dict_end)

        if index == 9:
            for key in untruncated_pos_count:
                if key > 0 and key < genome_size:
                    dict_data = {key:untruncated_pos_count[key]}
                    list_dedict_untruncated_pos.append(dict_data)

    data = {"3_prime_count": list_dedict_ds,
            "5_prime_count" : list_dedict_as,
            "block_count" : list_dedict_block,
            "start_site_count" : list_dedict_start,
            "end_site_count" : list_dedict_end,
            "read_size" : list_dedict_size,
            "junction_count" : list_dedict_junction,
            "variant_count" : list_dedict_barcode,
            "read_summary_count" : count_read,
            "onblock_pos_data" : list_dedict_untruncated_pos}

    return data


def data_export(dict_ds_pos, dict_as_pos, nb_blocs, start_plot, list_size,\
                junction, dict_count_ss, count_read, result_folder, end_plot):
    """
    Function that exports data to a TSV file.
    """
    filename = result_folder+"3prime_site.tsv"
    with open(filename, "w", encoding="utf-8") as filout:
        line_1 = "3prime_block_site\tCount\n"
        filout.write(line_1)
        for key in dict_ds_pos:
            new_line = f'{key}\t{dict_ds_pos[key]}\n'
            filout.write(new_line)

    filename = result_folder+"5prime_site.tsv"
    with open(filename, "w", encoding="utf-8") as filout:
        line_1 = "5prime_block_site\tCount\n"
        filout.write(line_1)
        for key in dict_as_pos:
            new_line = f'{key}\t{dict_as_pos[key]}\n'
            filout.write(new_line)

    filename = result_folder+"number_of_blocks.tsv"
    with open(filename, "w", encoding="utf-8") as filout:
        line_1 = "Number_of_blocks\tCount\n"
        filout.write(line_1)
        for key in nb_blocs:
            new_line = f'{key}\t{nb_blocs[key]}\n'
            filout.write(new_line)

    filename = result_folder+"start_site.tsv"
    with open(filename, "w", encoding="utf-8") as filout:
        line_1 = "Start_site\tCount\n"
        filout.write(line_1)
        for key in start_plot:
            new_line = f'{key}\t{start_plot[key]}\n'
            filout.write(new_line)

    filename = result_folder+"end_site.tsv"
    with open(filename, "w", encoding="utf-8") as filout:
        line_1 = "End_site\tCount\n"
        filout.write(line_1)
        for key in end_plot:
            new_line = f'{key}\t{end_plot[key]}\n'
            filout.write(new_line)

    filename = result_folder+"read_size.tsv"
    with open(filename, "w", encoding="utf-8") as filout:
        line_1 = "Size\tCount\n"
        filout.write(line_1)
        for key in list_size:
            new_line = f'{key}\t{list_size[key]}\n'
            filout.write(new_line)

    filename = result_folder+"junction.tsv"
    with open(filename, "w", encoding="utf-8") as filout:
        line_1 = "Junction\tCount\n"
        filout.write(line_1)
        for key in junction:
            new_line = f'{key}\t{junction[key]}\n'
            filout.write(new_line)

    filename = result_folder+"variants.tsv"
    with open(filename, "w", encoding="utf-8") as filout:
        line_1 = "Barcode\tCount\n"
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
