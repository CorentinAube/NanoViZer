#!/bin/bash
# Code that convert Bed file from MinIon plateform to 2 bed files xxx_cell.bed and xxx_virus.bed
# Needs two arguments : 
#	-path to file.bam
#	-name of bam file without extension

#exemple:
#	./Bed_gen.sh ../data/ sam2bam_bam_alignments_2020258

dir=$1
genome_name=$2
bed_name=$3

cd $dir


#Create the Bed file in bed12 format
###bed_full=$f.bed
bedtools bamtobed -bed12 -i $genome_name > $bed_name #$bed_full
#bed=${bed_full/.bam/_bam}
#mv $bed_full $bed
#echo 'bam2bed end'

##bed_cell=${bed}_cell.bed
#grep -v 'pNLGV_4GS_Tm' $bed > $bed_cell
#grep -v $genome_name $bed > $bed_cell
#mv_bed_cell=${bed_cell/_bam.bed_cell.bed/_cell.bed}
#mv $bed_cell $mv_bed_cell
#echo 'bed cell end'

##bed_virus=${bed}_virus.bed
#grep 'pNLGV_4GS_Tm' $bed > $bed_virus
##grep $genome_name $bed $bed > $bed_virus
##mv_bed_virus=${bed_virus/_bam.bed_virus.bed/_virus.bed}
##mv $bed_virus $mv_bed_virus
##echo 'bed virus end'




#Code is working.

#-------------------------------------------------------------------------------------------------#
#First simple code that just analyse one bam file
#this code is working but it is not in a for loop

#Directory
##dir=$1
#Bam file
##file=$2

##cd $dir

#Create the Bed file in bed12 format
##bedtools bamtobed -bed12 -i $file.bam > $file.bed
##echo 'bam2bed'

##grep -v 'pNLGV_4GS_Tm' $file.bed > ${file}_cell.bed
##echo 'grep1'

##grep 'pNLGV_4GS_Tm' $file.bed > ${file}_virus.bed
##echo 'grep2'
