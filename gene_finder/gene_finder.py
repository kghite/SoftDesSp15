# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:24:42 2014

@author: Kathryn Hite

Description: Determine the amino acids present in a given dna sequence

"""

# you may find it useful to import these variables (although you are not required to use them)
from amino_acids import aa, codons, aa_table
import random
from load import load_seq

def shuffle_string(s):
    """ Shuffles the characters in the input string
        NOTE: this is a helper function, you do not have to modify this in any way """

    return ''.join(random.sample(s,len(s)))


def get_complement(nucleotide):
    """ Returns the complementary nucleotide

        nucleotide: a nucleotide (A, C, G, or T) represented as a string
        returns: the complementary nucleotide
    >>> get_complement('A')
    'T'
    >>> get_complement('C')
    'G'
    """
    if nucleotide == "A":
        return("T")
    elif nucleotide == "C":
        return("G")
    elif nucleotide == "T":
        return("A")
    elif nucleotide == "G":
        return("C")


def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specfied DNA
        sequence
    
        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string
    >>> get_reverse_complement("ATGCCCGCTTT")
    'AAAGCGGGCAT'
    >>> get_reverse_complement("CCGCGTTCA")
    'TGAACGCGG'
    """
    complement = ''
    r_complement = ''

    # compute the compliment dna string
    for i in range(len(dna)):
        complement = complement + get_complement(dna[i])

    return complement[::-1]


def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start codon and returns
        the sequence up to but not including the first in frame stop codon.  If there
        is no in frame stop codon, returns the whole string.
        
        dna: a DNA sequence
        returns: the open reading frame represented as a string
    >>> rest_of_ORF("ATGTGAA")
    'ATG'
    >>> rest_of_ORF("ATGAGATAGG")
    'ATGAGA'
    """
    stop_codon = ('TGA', 'TAA', 'TAG')
    e_index = len(dna)

    # loop through the dna string in 3 character sets to identify stop codons
    for i in range(0, len(dna) - 2, 3):
        codon = dna[i:i+3]
        if codon in stop_codon:
            e_index = i
            return dna[0:e_index]

    return dna


def find_all_ORFs_oneframe(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence and returns
        them as a list.  This function should only find ORFs that are in the default
        frame of the sequence (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_oneframe("ATGCATGAATGTAGATAGATGTGCCC")
    ['ATGCATGAATGTAGA', 'ATGTGCCC']
    """
    oneframe_orf_list = []
    start_codon = 'ATG'
    i = 0

    # loop through the dna string in three character sets to find start codons
    while i < len(dna):
        # if a start codon is found then find a stop codon and add the open reading frame to the list 
        if dna[i:i+3] == start_codon:
            oneframe_orf_list.append(rest_of_ORF(dna[i:]))
            i = i + len(rest_of_ORF(dna[i:]))
        i += 3

    return oneframe_orf_list


def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in all 3
        possible frames and returns them as a list.  By non-nested we mean that if an
        ORF occurs entirely within another ORF and they are both in the same frame,
        it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs

    >>> find_all_ORFs("ATGCATGAATGTAG")
    ['ATGCATGAATGTAG', 'ATGAATGTAG', 'ATG']
    """
    all_orf_list = []

    # search for open reading frames 3 times, shifting the start position over one index each time
    for i in range(3):
        all_orf_list = all_orf_list + find_all_ORFs_oneframe(dna[i:])
        
    return all_orf_list


def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_both_strands("ATGCGAATGTAGCATCAAA")
    ['ATGCGAATG', 'ATGCTACATTCGCAT']
    """
    # find all open reading frames in the dna get the reverse compliment of the dna, find all open reading frames in reverse compliment
    r_dna = get_reverse_complement(dna)
    both_strands_list = find_all_ORFs(dna) + find_all_ORFs(r_dna)

    return both_strands_list


def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string
    >>> longest_ORF("ATGCGAATGTAGCATCAAA")
    'ATGCTACATTCGCAT'
    """
    longest_orf = ''

    # find the longest orf in both strands
    longest_orf = max(find_all_ORFs_both_strands(dna))

    return longest_orf


def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        
        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF 
    >>> longest_ORF("ATGCGAATGTAGCATCAAA")
    'ATGCTACATTCGCAT'
    """
    longest_orf_len = []

    # shuffle the dna num_trials times and get longest orf from all trials
    for i in range(num_trials):
        dna_shuffled = shuffle_string(dna)
        longest_orf_len.append(len(longest_ORF(dna_shuffled)))

    return max(longest_orf_len)  


def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region).
        
        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment

        >>> coding_strand_to_AA("ATGCGA")
        'MR'
        >>> coding_strand_to_AA("ATGCCCGCTTT")
        'MPA'
    """
    amino_acid_list = ''
    i = 0

<<<<<<< HEAD
    # loop through codons in dna string and add corresponding amino acid to the list
    while i in range(len(dna) - 2):
        codon = dna[i:i+3]
        amino_acid = aa_table[codon]
        amino_acid_list = amino_acid_list + amino_acid
        i += 3

    return amino_acid_list


def gene_finder(dna):
    """ Returns the amino acid sequences coded by all genes that have an ORF
        larger than the specified threshold.
        
        dna: a DNA sequence
        threshold: the minimum length of the ORF for it to be considered a valid
                   gene.
        returns: a list of all amino acid sequences whose ORFs meet the minimum
                 length specified.
    Unable to create a doc test, because the result will be different each time
=======
def gene_finder(dna):
    """ Returns the amino acid sequences that are likely coded by the specified dna
        
        dna: a DNA sequence
        returns: a list of all amino acid sequences coded by the sequence dna.
>>>>>>> 922a6e32441860ab0413630f74531e6e47a16a7c
    """

    threshold = longest_ORF_noncoding(dna, 1500)
    print threshold
    all_orfs = []
    amino_acid_list = []

    # compute all orfs and return amino acids from orfs passing the threshold
    all_orfs = find_all_ORFs_both_strands(dna)
    for orf in all_orfs:
        if len(orf) > threshold:
            amino_acid_list.append(coding_strand_to_AA(orf))

    return amino_acid_list


''' Doctest and Run gene_finder'''
if __name__ == "__main__":
    import doctest
    doctest.testmod()

    dna = load_seq("./data/X73525.fa")
    genes = gene_finder(dna)
    print genes
