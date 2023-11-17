"""
Code to generate fasta sequence for each barcode that user
want in one fasta file.
"""

import sys
import os
import utils_main


# 1 avoir le barcode V et avoir le nom du fastq V
# 2 avoir le bedfile avec les barcode V
# 3 récupérer tous les ID du bed file V
# 4 parse fastq to select ID and write in a new fastq V
# 5 write bed file for selected barcode V
# 6 test the new function !!!!


def barcode_to_id(barcode_clean, bedfile):#, barcodefile, result_folder):
    '''
    Function that obtain id of sequence with the barcode on the Bed file.
    '''
    pathout = f"{result_folder}+bedfile_for_{barcode_clean}.bed"
    id_list = []
    with open(bedfile, "r") as filin, open(pathout, "w") as filout:
        for read in filin:
            read = read.split("\t")
            read_barcode = read[-2]
            read_id = read[3]
            if read_barcode == barcode_clean:
                id_list.append(read_id)
                new_read = read[:-2]
                new_read = ("\t").join(new_read)
                filout.write(new_read)

    return id_list


def id_seq_to_fasta(barcode_clean, fastq, id_list, result_folder):
    """
    Function that write a fasta file with id.
    """
    dict_seq = {}
    fastq_file = f"../data/{fastq}.fastq"
    with open(fastq, "r", encoding="utf-8") as filin_fastq:
        filin_fastq = filin_fastq.readlines()
        for index, read in enumerate(filin_fastq):
            if read.startswith('@'):
                id_fastq = read[1:]
                id_fastq = id_fastq.split(" ")
                id_fastq = id_fastq[0]

                if id_fastq in id_list:
                    dict_seq[id_fastq] = filin_fastq[index+1]

    pathout = f"{result_folder}+{barcode_clean}_fasta.fasta"
    with open(pathout, 'w', encoding="utf-8") as filout:
        for seq in dict_seq:
            new_line = '> {0}\n{1}\n'.format(seq, dict_seq[seq])
            filout.write(new_line)



def main(fastq, barcode, result_folder):
    barcode_clean = barcode.split("_")
    barcode_clean = barcode_clean[2:-2]
    barcode_clean = ("").join(barcode_clean)

    bedfile = f"{result_folder}+bedfile_withbarcode.tsv"
    id_list = barcode_to_id(barcode_clean, bedfile)
    if fastq.endswith(".fastq"):
        fastq = fastq[:-6]
        id_seq_to_fasta(barcode_clean, fastq, id_list, result_folder)
    else:
        id_seq_to_fasta(barcode_clean, fastq, id_list, result_folder)


if __name__ == '__main__':
    main()
