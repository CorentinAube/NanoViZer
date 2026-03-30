#! /usr/bin/env python3

import os
import time
import datetime
import subprocess
import utils_main
import read_filter
import utils_main_2
import utils_main_3
import utils_main_4

def main(file_name, genome_name, genome_size, passthrough, min_3_end,\
         max_3_end, min_read_length, max_5_start, genome_file_name, min_5_start):
    
    """
    This is the main function that will launch each NanoViZer function 
    to obtain the BED file from the BAM file, filter the reads, 
    generate the barcodes, perform barcode analyses, and save the results 
    in the "Results" folder. This function returns a JSON file.
    """

    start = time.time()

    # Remove the .bam extension if provided by the user on the front page
    file_name = utils_main.clean_bam_name(file_name)

    import_time = datetime.datetime.now()

    # create the result foder
    result_folder = "../results/"+file_name+"_"+import_time.strftime("%Y%m%d_%Hh%Mm%Ss")+"/"
    os.makedirs(result_folder)
    utils_main.create_folder(result_folder)

    utils_main.log_file_gen(result_folder, file_name, genome_name, genome_size, passthrough, min_3_end,\
                            max_3_end, min_read_length, max_5_start, genome_file_name,min_5_start)

    print("bedfile step run")
    utils_main.bedfile_gen(file_name)
    utils_main.genome_nam_gen(file_name, result_folder)
    print("bedfile step done")

    print("Keep viral reads step run")
    #filter the bedfile to keep viral reads.
    virus_bed_file = utils_main.virus_bed_gen(genome_name, file_name)
    print("Keep viral reads step done")

    print("filtering step run")
    # Read filtering according to the parameters.
    filter_truncated, count_read = read_filter.filter_by_lenght(result_folder, virus_bed_file,\
                                                                max_3_end, passthrough,\
                                                                min_3_end, min_read_length,\
                                                                max_5_start, min_5_start)

    print("filtering step done")

    print("add barcode1 run")
    # Add pos of barcode da ss_pos_filter_splict.tsv
    bedfile_with_barcode, dict_count_ss, count_junction_site = utils_main_2.add_barcode(result_folder, filter_truncated)
    # Create tsv file with unique barcode
    untruncated_pos_count = utils_main_2.oneblock_coverage(result_folder, genome_name, genome_size,\
                                                           file_name, max_5_start, max_3_end)
    print("add barcode2 run")
    barcode_count = utils_main_2.unique_barcode(bedfile_with_barcode)
    print("add barcode2 done")

    print("generate junction sequence run")
    file = os.listdir("../genome/")
    if genome_file_name != None:
        if genome_file_name in file:
            utils_main_4.seq_gen(count_junction_site, result_folder, genome_file_name)
        else:
            print("""

                Please add the genome refseq file in the genome folder
                or check the file name to allows sequence analysis.

                """)
    print("generate junction sequence done")

    print("create summary run")
    dict_ds_pos, dict_as_pos, nb_blocs, start_plot, list_size, junction, list_size_json, end_plot =\
    utils_main_3.create_summary(virus_bed_file, filter_truncated, barcode_count)
    data = utils_main.json_gen(dict_ds_pos, dict_as_pos, nb_blocs,\
                               start_plot, list_size_json, junction,\
                               dict_count_ss, count_read, end_plot,\
                               untruncated_pos_count, genome_size)
    print("create summary done")

    print("create tsv file run")
    #export data in tsv files
    utils_main.data_export(dict_ds_pos, dict_as_pos, nb_blocs, start_plot,\
                           list_size, junction, dict_count_ss, count_read, result_folder, end_plot)
    print("create tsv file done")

    shell_line = f"rm {result_folder}{genome_name}.txt"
    subprocess.run(shell_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print(time.time()-start)
    return data
