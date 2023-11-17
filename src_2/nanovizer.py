#! /usr/bin/env python3

"""
--------HIV Minion Analysis--------

This code as for purpose to analyse site donnor and acceptor
in the HIV transcrit from Minion sequencing.

Nguyen Quang Nam has developped the methodology
__Authors__ = Nguyen Quang Nam

Corentin Aubé has developped python script
__Authors__ = Corentin Aubé

Front development
__Authors__ = Benjamin Morvan

__Lab__ = U1016, Equipe Berlioz-Emiliani
__Date__ = 05/10/2020


Installer bash sur W10
https://blog.ineat-group.com/2020/02/utiliser-le-terminal-bash-natif-dans-windows-10/
"""
import os
import datetime
import utils_main
import read_filter
import barcode
import summary_no_annotation
import one_block_analysis

def main(bam_name, genome_name, genome_size, start_genome, minimal_lenght, end_genome, min_read_length):
    """
    All function to analyse bedfile are launch from here.

    To run file from the terminal : python3 main_bis.py
    """
    #print(file_name)
    # input from flask
    #bam_name = "HDV1dbis_sorted"
    #bam_name = file_name
    # indicate the start position of the genome
    #start_genome = 0
    # Indicate the end postiion of the genome, that means position that read will not be longer
    #end_genome = 1000000000
    # Indicate the minimal lenght of splice reads, the end minimal lenght of the reads
    #minimal_lenght = 0
    #genome_name = "HDV1d"
    #genome_size = 2000
    #barcode_output = ""

    # remove .bam at the end of the file is user indicate them in the front page
    bam_name = utils_main.clean_bam_name(bam_name)

    # create all folder to write and class output files
    import_time = datetime.datetime.now()
    result_folder = "../results/"+bam_name+"_"+import_time.strftime("%Y%m%d_%Hh%Mm%Ss")+"_"+str(min_read_length)+"_"+str(start_genome)+"_"+str(minimal_lenght)+"_"+str(end_genome)+"/"
    os.makedirs(result_folder)
    utils_main.create_folder(result_folder)

    utils_main.bedfile_gen2(bam_name)###, path_to_bedfile)
    #filtre le fichier bed pour ne garder les seq virales ou que les US (viral and others)
    virus_bed_file, all_oneblock_read = utils_main.virus_bed_gen(genome_name, bam_name) #all_oneblock_read ne sert à rien

    ##### Option facultative pour le moment, permet de déterminer les génomiques
    # rescue all data and analyse the US read to determine if it's in the intron or not
    #one_block_data = one_block_analysis.main(all_oneblock_read, genome_name)


    # Filter the read in function of the start and end
    # position of the columns 2 and 3 of the bedfile and
    # create file with US or splice reads.
    filter_splice, count_read = read_filter.filter_by_lenght(result_folder, virus_bed_file,\
                                                             end_genome, start_genome,\
                                                             minimal_lenght, min_read_length) ########### NEW MINIMAL SIZE of read

    # Add pos of barcode da ss_pos_filter_splict.tsv
    list_tsv_file, dict_count_ss = barcode.add_barcode(result_folder, filter_splice)
    # Create tsv file with unique barcode
    barcode_count = read_filter.unique_barcode(list_tsv_file)

    dict_sd_pos, dict_sa_pos, nb_blocs, start_plot, list_size, junction, list_size_json, end_plot =\
    summary_no_annotation.create_summary(filter_splice, barcode_count)
    data = utils_main.json_gen(dict_sd_pos, dict_sa_pos, nb_blocs,\
                               start_plot, list_size_json, junction,\
                               dict_count_ss, count_read, genome_size, end_plot)#, one_block_data)

    #export data en tsv
    utils_main.data_export(dict_sd_pos, dict_sa_pos, nb_blocs, start_plot,\
                           list_size, junction, dict_count_ss, count_read, result_folder, end_plot)

    return data


if __name__ == '__main__':
    bam_name = "sam2bam_bam_alignments_2020258"
    min_position_3 = 0
    min_position_5 = 0
    max_position_5 = 1000000000
    genome_name = "pNLGV_4GS_Tm"
    genome_size = 15000
    min_read_length = 0
    main(bam_name, genome_name, genome_size, min_position_3, min_position_5, max_position_5, min_read_length)
