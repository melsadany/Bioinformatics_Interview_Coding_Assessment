##################################################################
#                    Section-1/Assembly script                   #
##################################################################
# libs
import os
from collections import Counter
import argparse
import re
##################################################################
def is_dna_sequence(sequence):
    """
    Checks if a given sequence consists of valid DNA bases (A, C, G, T).

    Args:
        sequence (str): The sequence to be checked.

    Returns:
        bool: True if the sequence is a valid DNA sequence, False otherwise.
    """
    return all(base in 'ACGT' for base in sequence)

def find_kmers(assembly_folder, output_path, kmer_length=5):
    """
    Finds k-mers in DNA sequences from files in the specified assembly folder.
    The function will not provide k-mers per sequence if there is multiple sequences per query file

    Args:
        assembly_folder (str): Path to the folder containing assembly files in FASTA format.
        output_path (str): Path to the folder where output files will be saved.
        kmer_length (int, optional): Length of k-mer (default: 5).
    """
    for filename in os.listdir(assembly_folder):
        if filename.endswith(".fasta"):
            kmers = Counter()  # Initialize a new counter for each file

            with open(os.path.join(assembly_folder, filename), 'r') as file:
                lines = file.readlines()
                sequence = ''
                for line in lines[1:]:  # Skip the info line(s) and process each sequence
                    if line.startswith('>'):
                        if is_dna_sequence(sequence):
                            kmers.update([sequence[i:i+kmer_length] for i in range(len(sequence)-kmer_length+1)])
                        else:
                            print(f"Skipping file {filename}. Not a valid DNA sequence.")
                        sequence = ''  # Reset sequence for the next one
                    else:
                        sequence += line.strip()

                # Process the last sequence in the file
                if is_dna_sequence(sequence):
                    kmers.update([sequence[i:i+kmer_length] for i in range(len(sequence)-kmer_length+1)])
                else:
                    print(f"Skipping file {filename}. Not a valid DNA sequence.")
            
            if len(kmers) > 0:  # Check if any k-mers were found
                output_file = os.path.splitext(filename)[0] + "_output.tsv"
                write_output(kmers, output_path, output_file)

def write_output(kmers, output_path, outfile):
    """
    Writes k-mer sequences and their counts to an output file in TSV format.

    Args:
        kmers (Counter): A Counter object containing k-mer sequences and their occurrences.
        output_path (str): Path to the folder where the output file will be saved.
        outfile (str): Name of the output file.
    """
    with open(os.path.join(output_path, outfile), 'w') as file:
        for kmer, count in kmers.items():
            file.write(f"{kmer}\t{count}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find k-mer sequences and their occurrences.")
    parser.add_argument("--kmer_length", type=int, default=5, help="Length of k-mer (default: 5)")
    parser.add_argument("--assembly_folder", default="assembly/", help="Folder containing assembly files (default: assembly/)")
    parser.add_argument("--output_path", default="/project/output/", help="Path for output files (default: /project/output/)")

    args = parser.parse_args()
    
    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)
        
    find_kmers(args.assembly_folder, args.output_path, args.kmer_length)
    
    
    ## use this command to run it in UNIX terminal
    # python applicant_scripts_ME/section-1_ME_092023.py --kmer_length 5 --assembly_folder Section_1/assembly --output_path Section_1/output