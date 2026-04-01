import os
from collections import Counter

def seq_gen(count_ss, result_folder, genome_file_name):
    """
    This function retrieves the sequences located near the junction sites.
    """
    count_ss_dict = Counter(count_ss)
    count_ss = list(set(count_ss))
    genome = genome_gen(genome_file_name)


    file = result_folder+"junction_sequence.tsv"
    with open(file, 'w') as filout:
        first_line = "Barcode\tcount\t+1 and +2 in 5' intron\t\
        -2 and -1 in 3' intron\t-10 (in exon) and +12 in 5' intron\t\
        -12 and +10 (in exon) in 3' intron\n"
        filout.write(first_line)
        for site in count_ss:
            site2 = site.split("_")
            if len(site2) == 2:
                sd = site2[0]
                sa = site2[1]
                seq_sd = genome[int(sd):int(sd)+2]
                seq_sa = genome[int(sa)-3:int(sa)-1]

                seq_sd_large = genome[int(sd)-10:int(sd)+12]
                seq_sa_large = genome[int(sa)-12:int(sa)+10]

                c = count_ss_dict[site]
                new_line = site.strip()+"\t"+str(c)+"\t"+seq_sd+"_"+seq_sa+"\t"+seq_sd_large+"\t"+seq_sa_large+"\n"
                filout.write(new_line)
            elif len(site2) > 2:
                ss = ""
                ss_longseq = ""
                for i, _ in enumerate(site2):
                    if i%2 == 0:
                        sd = site2[i].strip()
                        sa = site2[i+1].strip()
                        seq_sd = genome[int(sd):int(sd)+2]
                        ss += seq_sd+"_"
                        seq_sa = genome[int(sa)-3:int(sa)-1]
                        ss += seq_sa+"_"

                        longseq_sd = genome[int(sd)-10:int(sd)+12]
                        ss_longseq += longseq_sd+"\t"
                        longseq_sa = genome[int(sa)-13:int(sa)+9]
                        ss_longseq += longseq_sa+"\t"

                c = count_ss_dict[site]
                new_line = site.strip()+"\t"+str(c)+"\t"+ss[:-1]+"\t"+ss_longseq+"\n"
                filout.write(new_line)

            else:
                new_line = "\n"
                filout.write(new_line)


def genome_gen(genome_file_name):
    """
    Function that retrieves the genome sequence as a single line from a FASTA file.
    """

    file = "../genome/"+genome_file_name
    with open(file, "r") as filin:
        filin = filin.readlines()
        genome = ''
        # check if the sequence is in one line.
        if filin[0].startswith(">") and len(filin) == 2:
            genome = filin[1]
        elif filin[0].startswith(">") and len(filin) > 2:
            for index, line in enumerate(filin):
                if index > 0:
                    line = line.rstrip()
                    genome += line
        else:
            print("""\nPlease add a genome in the fasta format
				  >Genome_name
				  ATGC...\n""")

    return genome
    