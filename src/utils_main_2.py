#! /usr/bin/env python3
"""
Function that generate barcodes
"""
from itertools import islice
from collections import Counter
import pysam

def add_barcode(result_folder, filter_truncated):
    """
    Add barcode to bedfile.txt
    """
    count_junction_site = ['']*len(filter_truncated)
    list_new_line = ['']*len(filter_truncated)
    for index, seq in enumerate(filter_truncated):
        seq = seq.split("\t")

        #Acceptor Site (AS)-like position
        start = seq[1]
        strat_block = seq[-1]
        strat_block = strat_block.split(',')
        list_as = []
        for site in strat_block:
            if int(site) != 0:
                sa = int(site)+int(start)+1
                list_as.append(str(sa))

        #Donnor Site (DS) like position
        size_block = seq[-2]
        size_block = size_block.split(',')
        end = seq[2]
        list_ds = []
        for pos, pos_sa in zip(size_block, strat_block):
            sd = int(pos)+int(start)+int(pos_sa)
            if sd < int(end):
                list_ds.append(str(sd))

        #list splice-site-like by reads
        ss = ''
        for sd, sa in zip(list_ds, list_as):
            ss += sd+"_"+sa+'_'


        seq = ("\t").join(seq)
        new_line = seq.strip()+'\t'+ss[:-1]#+'\t'
        list_new_line[index] = new_line

        count_junction_site[index] = ss[:-1]
 
    liste_new_line_consensus, list_consensus = consensus_start_end_barcode(list_new_line)

    dict_count_ss = Counter(list_consensus)


    bedfile_with_barcode = []
    for seq in liste_new_line_consensus:
        ss = seq.strip()
        ss = ss.split('\t')
        ss = ss[-1]
        new_line = seq+"\t"+str(dict_count_ss[ss])+"\n"
        bedfile_with_barcode.append(new_line)

    # to generate count without consensus
    barcode_without_consensus = []
    for index, barcode_count in enumerate(bedfile_with_barcode):
        split_line = barcode_count.split("\t")
        without_consensus = split_line[0].split("_")
        without_consensus = "_".join(without_consensus[1:-1])
        without_consensus = without_consensus+"\t"+split_line[1]
        if without_consensus not in barcode_without_consensus:
            barcode_without_consensus.append(without_consensus)
    # to generate file where barcode and seq id are together
    pathout_bed_with_barcode = f"{result_folder}bedfile_with_barcode.tsv"
    with open(pathout_bed_with_barcode, "w") as filout:
        for line in list_new_line:
            line_ = line.split("\t")
            barcode = line_[-1]
            for count in barcode_without_consensus:
                count = count.split("\t")
                barcode_ = count[0]
                if barcode_ == barcode:
                    newline = line.strip()+"\t"+str(count[1])
                    filout.write(newline)
                    break

    return bedfile_with_barcode, dict_count_ss, count_junction_site

def oneblock_coverage(result_folder, genome_name, genome_size, file_name, \
                      max_5_start, max_3_end):
    """
    Function to obtain genome coverage.
    """
    bam_file = f"../data/{file_name}.bam"
    pysam.index(bam_file)
    bam = pysam.AlignmentFile(bam_file, "rb")
    coverage = [0] * genome_size

    if max_3_end == 1000000000000:
        regions = [(genome_name, max_5_start, int(genome_size))]
        file = result_folder+"coverage.tsv"
        with open(file, "w") as filout:
            line = "Genome position\tCount\n"
            filout.write(line)
            if regions:
                # If specific regions are defined, process only those regions
                for chrom, start, end in regions:
                    for pileup_column in bam.pileup(chrom, start, end):
                        coverage[pileup_column.reference_pos] += pileup_column.nsegments
                        new_line = str(pileup_column.reference_pos)+"\t"+str(pileup_column.nsegments)+"\n"
                        filout.write(new_line)
            else:
                # Otherwise, process the entire file
                for pileup_column in bam.pileup():
                    coverage[pileup_column.reference_pos] += pileup_column.nsegments

            bam.close()
    else:
        regions = [(genome_name, max_5_start, max_3_end)]
        file = result_folder+"coverage.tsv"
        with open(file, "w") as filout:
            line = "Genome position\tCount\n"
            filout.write(line)
            if regions:
                for chrom, start, end in regions:
                    for pileup_column in bam.pileup(chrom, start, end):
                        coverage[pileup_column.reference_pos] += pileup_column.nsegments
                        new_line = str(pileup_column.reference_pos)+"\t"+str(pileup_column.nsegments)+"\n"
                        filout.write(new_line)
            else:
                for pileup_column in bam.pileup():
                    coverage[pileup_column.reference_pos] += pileup_column.nsegments

            bam.close()

    coverage_dict = {index+1: value for index, value in enumerate(coverage)}

    if max_3_end != 1000000000000:
        end = max_3_end-len(coverage_dict)
        key_inter = list(islice(coverage_dict.keys(), max_5_start, len(coverage_dict)+end))
        untruncated_pos_count = {k: coverage_dict[k] for k in key_inter}
    elif max_3_end == 1000000000000:
        key_inter = list(islice(coverage_dict.keys(), max_5_start, len(coverage_dict)))
        untruncated_pos_count = {k: coverage_dict[k] for k in key_inter}

    return untruncated_pos_count


def consensus_start_end_barcode(list_new_line):
    """
    Function that generate start and end consensus position for each barcode.
    """
    dict_barcode_start_end = {}
    for seq in list_new_line:
        seq = seq.strip()
        seq = seq.split('\t')
        start = int(seq[1])+1
        end = int(seq[2])-1
        barcode = seq[-1]
        if barcode not in dict_barcode_start_end:
            dict_barcode_start_end[barcode] = [[start], [end]]
        else:
            dict_barcode_start_end[barcode][0].append(start)
            dict_barcode_start_end[barcode][1].append(end)
    consensus_start_end_site = consensus_site_counter(dict_barcode_start_end)

    list_consensus = [""]*len(list_new_line)
    liste_new_line_consensus = ['']*len(list_new_line)
    for index, seq in enumerate(list_new_line):
        seq = seq.strip()
        seq = seq.split('\t')
        barcode = seq[-1]
        start, end = consensus_start_end_site[barcode][0], consensus_start_end_site[barcode][1]
        barcode_consensus = start+"_"+barcode+"_"+end
        list_consensus[index] = barcode_consensus
        seq[-1] = barcode_consensus
        seq = ("\t").join(seq)
        liste_new_line_consensus[index] = barcode_consensus

    return liste_new_line_consensus, list_consensus

def consensus_site_counter(dict_barcode_start_end):
    """
    Function that count the start and end site the most represented.
    """
    dict_barcode_start_end_consensus = {}
    for key_barcode in dict_barcode_start_end:
        list_start = dict_barcode_start_end[key_barcode][0]
        list_end = dict_barcode_start_end[key_barcode][1]
        start_site_consensus, _ = site_counter(list_start)
        end_site_consensus, _ = site_counter(list_end)
        dict_barcode_start_end_consensus[key_barcode] = [str(start_site_consensus), str(end_site_consensus)]
    return dict_barcode_start_end_consensus


def site_counter(liste):
    counter = Counter(liste)
    site, occurancy = counter.most_common(1)[0]
    return site, occurancy

def unique_barcode(bedfile_with_barcode):
    '''
    Create file with unique barcode and count.
    '''
    barcode_dict = {}
    for read in bedfile_with_barcode:
        read = read.strip()
        read = read.split('\t')
        barcode = read[-2]
        count = read[-1]
        if barcode not in barcode_dict:
            barcode_dict[barcode] = count

    return barcode_dict

