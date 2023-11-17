#! /usr/bin/env python3
"""
Function that generate barcodes
"""

from collections import Counter


def add_barcode(result_folder, list_tsv_file):
    """
    Add barcode to bedfile.txt
    """
    count_ss = []
    list_new_line = []
    for seq in list_tsv_file: #filin:
        seq = seq.split("\t")

        #SA
        start = seq[1]
        strat_block = seq[-1]
        strat_block = strat_block.split(',')
        list_sa = []
        for site in strat_block:
            if int(site) != 0:
                sa = int(site)+int(start)+1
                list_sa.append(str(sa))

        #SD
        size_block = seq[-2]
        size_block = size_block.split(',')
        end = seq[2]
        list_sd = []
        for pos, pos_sa in zip(size_block, strat_block):
            sd = int(pos)+int(start)+int(pos_sa)
            if sd < int(end):
                list_sd.append(str(sd))

        #list ss by reads
        ss = ''
        for sd, sa in zip(list_sd, list_sa):
            ss += sd+"_"+sa+'_'


        seq = ("\t").join(seq)
        new_line = seq.strip()+'\t'+ss[:-1]#+'\t'
        list_new_line.append(new_line)

        count_ss.append(ss[:-1])

    #list_new_line contain the barcode yet.
    #contain all information about the bed.
    liste_new_line_consensus = consensus_start_end_barcode(list_new_line)
    for seq in liste_new_line_consensus:
        seq_ = seq.strip()
        seq_ = seq_.split('\t')
        barcode_c = seq_[-1]
        barcode = barcode_c.split("_")
        barcode = barcode[1:-1]
        barcode = ("_").join(barcode)        
        for index, i in enumerate(count_ss):
            if i == barcode:
                count_ss[index] = barcode_c    

    dict_count_ss = Counter(count_ss)
    

    bedfile_with_barcode = []
    for seq in liste_new_line_consensus:
        ss = seq.strip()
        ss = ss.split('\t')
        ss = ss[-1]
        new_line = seq+"\t"+str(dict_count_ss[ss])+"\n"
        bedfile_with_barcode.append(new_line)


    # to generate file where barcode and seq id are together    
    pathout_bed_with_barcode = f"{result_folder}bedfile_with_barcode.tsv"
    with open(pathout_bed_with_barcode, "w") as filout:
        for line in bedfile_with_barcode:
            filout.write(line)
    
    return bedfile_with_barcode, dict_count_ss

def consensus_start_end_barcode(list_new_line):
    """
    Function that generate start and end consensus position for each barcode.
    """
    #dict_barcode_start_end = {barcode1 : [[liste de start],[liste de end]],barcode2...}
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
    #print(dict_barcode_start_end)
    consensus_start_end_site = consensus_site_counter(dict_barcode_start_end)

    liste_new_line_consensus = []
    for seq in list_new_line:
        seq = seq.strip()
        seq = seq.split('\t')
        barcode = seq[-1]
        start, end = consensus_start_end_site[barcode][0], consensus_start_end_site[barcode][1]
        barcode_consensus = start+"_"+barcode+"_"+end
        seq[-1] = barcode_consensus
        seq = ("\t").join(seq)
        liste_new_line_consensus.append(seq)

    return liste_new_line_consensus


    
    


def consensus_site_counter(dict_barcode_start_end):
    """
    Function that count the start and end site the most represented.
    """
    #dict_barcode_start_end_consensus = {barcode = [start_consensus, end_consensus], barcode2 : [],....}
    dict_barcode_start_end_consensus = {}
    for key_barcode in dict_barcode_start_end:
        list_start = dict_barcode_start_end[key_barcode][0]
        list_end = dict_barcode_start_end[key_barcode][1]
        start_site_consensus, start_occurancy = site_counter(list_start)
        end_site_consensus, end_occurancy = site_counter(list_end)
        dict_barcode_start_end_consensus[key_barcode] = [str(start_site_consensus), str(end_site_consensus)]
    return dict_barcode_start_end_consensus



def site_counter(liste):
    counter = Counter(liste)
    site, occurancy = counter.most_common(1)[0]
    return site, occurancy


