#!/bin/bash

# This script required BLAST to be already installed 
# I have mine installed in my condo environment 
# skip the activation line if you do not have a condo environment and have BLAST already installed locally 
conda activate EGA 

# Set your directories
project_dir=/Volumes/Mac/Documents/job-applications/assessments/jmilabs/Bioinformatics_Interview_Coding_Assessment

query_file=${project_dir}/Section_2/query/query.fasta
assembly_file=${project_dir}/Section_2/assembly/GCA_019243775.1_ASM1924377v1_genomic.fasta
output_folder=${project_dir}/Section_2/output
output_file=alignment_output.txt

# Create output folder if it doesn't exist
mkdir -p $output_folder
cd ${output_folder}

# run blast using a protein sequence against a genomic DNA sequence db or ref ... I.e., tblastn
tblastn -query $query_file -subject $assembly_file -outfmt "6 qseqid sseqid pident length qcovs" | awk '$3 == 100 && $5 == 100 {print}' > $output_file


# use this command in UNIX shell to run the script
# bash applicant_scripts_ME/section-2_ME_092023.sh