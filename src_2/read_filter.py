#! /usr/bin/env python3
'''
Contain all functions to filter files.
'''


def filter_by_lenght(result_folder, virus_bed_file, end_genome, start_genome,\
                     minimal_lenght, minimal_size):
    '''
    Function that write a file that contain only reads that are
    not longer that the genome size.
    Write a file with all remove reads.
    Write a file with US and splice
    '''

    # create output file
    path_remove_read = result_folder+'remove_reads/remove.bed'
    path_read = result_folder+"spliced_seq/filter_splice.bed"
    path_read_us = result_folder+"one_block_reads/filter_one_block_reads.bed"
    path_short_splice = result_folder+"remove_reads/filter_short_multiple_block_reads.bed"

    count_plasmid = 0
    count_us = 0
    count_splice = 0
    count_short_multipleblocks = 0
    count_too_small_read = 0

    filter_splice = []
    with open(path_remove_read, "w", encoding="utf-8") as filout_remove, \
         open(path_read, "w", encoding="utf-8") as filout_filter,\
         open(path_read_us, 'w', encoding="utf-8") as filout_us, \
         open(path_short_splice, "w", encoding="utf-8") as filout_short:
        for seq in virus_bed_file:
            seq = seq.split('\t')
            #remove read too small
            size = seq[-2]; size = size.split(","); size = [int(x) for x in size]; size = sum(size)
            if size >= int(minimal_size):
                #remove read longer than genome and read before start
                if int(seq[2]) <= int(end_genome) and int(seq[1]) >= int(start_genome):
                    # check more than two blocks sequences
                    if int(seq[9]) > 1:
                        # check the minimal 3' position of read
                        if int(seq[2]) >= minimal_lenght: # 6131 D4b
                            new_line = ("\t").join(seq)
                            filter_splice.append(new_line) ###
                            filout_filter.write(new_line)
                            count_splice += 1
                        else: # remove all reads that are not enought long
                            new_line = ("\t").join(seq)
                            filout_short.write(new_line)
                            count_short_multipleblocks += 1
                    else: #keep reads with one block ie non spliced
                        new_line = ("\t").join(seq)
                        filout_us.write(new_line)
                        count_us += 1
                else: #remove read that are more longer than the genome size
                    new_line = ("\t").join(seq)
                    filout_remove.write(new_line)
                    count_plasmid += 1
            else:
                count_too_small_read += 1
    """
    count_read = [{"type":"total", "count":count_us+count_splice},
                   {"type":"one block", "count":count_us},
                   {"type":"multiple blocks", "count":count_splice},
                   {"type":"short mutliple blocks", "count":count_short_multipleblocks},
                   {"type":"removed reads", "count":count_plasmid}]
    """
    count_read = {"total":count_us+count_splice,
                  "single_block":count_us,
                  "multiple_block":count_splice,
                  "short_mutliple_block":count_short_multipleblocks,
                  "removed":count_plasmid,
                  "too_small_reads":count_too_small_read} ############# ligne qui fait beuger le front
    
    return filter_splice, count_read

def unique_barcode(list_tsv_file):
    '''
    Create file with unique barcode and count.
    '''
    barcode_dict = {}
    for read in list_tsv_file:
        read = read.strip()
        read = read.split('\t')
        barcode = read[-2]
        count = read[-1]
        if barcode not in barcode_dict:
            barcode_dict[barcode] = count

    return barcode_dict
