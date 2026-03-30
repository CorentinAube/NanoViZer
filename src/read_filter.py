#! /usr/bin/env python3


def filter_by_lenght(result_folder, virus_bed_file, max_3_end, passthrough,\
                     min_3_end, min_read_length, max_5_start, min_5_start):
    '''
    This function filters the reads based on the optional parameters provided 
    by the user. If no parameters are specified, default values will be applied.

    This function also writes BED files for the reads that did not pass 
    the filters, the untruncated reads, and the truncated reads.
    '''

    # create output file
    path_remove_read = result_folder+'remove_reads/remove.bed'
    path_read = result_folder+"spliced_reads/filter_truncated.bed"
    path_read_us = result_folder+"one_block_reads/filter_one_block_reads.bed"

    count_removed = 0
    count_untruncated = 0
    count_truncated = 0

    filter_truncated = []

    with open(path_remove_read, "w", encoding="utf-8") as filout_remove, \
         open(path_read, "w", encoding="utf-8") as filout_filter,\
         open(path_read_us, 'w', encoding="utf-8") as filout_us:
        for seq in virus_bed_file:
            seq = seq.split('\t')
            #remove read too small
            size = seq[-2]; size = size.split(",")
            size = [int(x) for x in size]; size_sum = sum(size)
            if size_sum >= int(min_read_length):
                # check more than two blocks sequences
                if int(seq[9]) > 1:
                    #remove read longer than genome
                    if int(seq[2]) <= int(max_3_end):
                        #remove read that start before a given position
                        if int(seq[1]) >= max_5_start:
                                if int(seq[1]) <= int(min_5_start):
                                    # check the minimal 3' position of read
                                    if int(seq[2]) >= min_3_end:
                                        # check if a 3' position is comprise in a block
                                        if passthrough > 0:
                                            start = seq[-1]; start = start.split(",")
                                            start = [int(x)+1+int(seq[1]) for x in start]
                                            end = [start1+size1 for start1, size1 in zip(start, size)]
                                            test = "no"
                                            for s, e in zip(start, end):
                                                if s <= passthrough+1 <= e:
                                                    new_line = ("\t").join(seq)
                                                    filter_truncated.append(new_line)
                                                    filout_filter.write(new_line)
                                                    count_truncated += 1
                                                    test = "yes"
                                                    break
                                            if test == "no":
                                                new_line = ("\t").join(seq)
                                                filout_remove.write(new_line)
                                                count_removed += 1
                                        else:
                                            new_line = ("\t").join(seq)
                                            filter_truncated.append(new_line)
                                            filout_filter.write(new_line)
                                            count_truncated += 1
                                    else: # remove all reads that are not enought long
                                        new_line = ("\t").join(seq)
                                        filout_remove.write(new_line)
                                        count_removed += 1
                                else: # remove all reads 5'mini
                                    new_line = ("\t").join(seq)
                                    filout_remove.write(new_line)
                                    count_removed += 1
                        else: #remove reads that start before a given position
                            new_line = ("\t").join(seq)
                            filout_remove.write(new_line)
                            count_removed += 1
                    else: #remove reads that are more longer than the genome size
                        new_line = ("\t").join(seq)
                        filout_remove.write(new_line)
                        count_removed += 1
                else: #keep reads with one block ie non spliced
                    new_line = ("\t").join(seq)
                    filout_us.write(new_line)
                    count_untruncated += 1
            else:
                filout_remove.write(new_line)
                count_removed += 1

    count_read = {"total":count_untruncated+count_truncated+count_removed,
                  "single_block":count_untruncated,
                  "multiple_block":count_truncated,
                  "removed":count_removed}

    return filter_truncated, count_read
