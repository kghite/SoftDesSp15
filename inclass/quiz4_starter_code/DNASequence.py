class DNASequence(object):
    """ Represents a sequence of DNA """
    def __init__(self, nucleotides):
        """ constructs a DNASequence with the specified nucleotides.
             nucleotides: the nucleotides represented as a string of
                          capital letters consisting of A's, C's, G's, and T's """
        self.nucleotides = nucleotides
 
    def __str__(self):
        """ Returns a string containing the nucleotides in the DNASequence
        >>> seq = DNASequence("TTTGCC")
        >>> print seq
        TTTGCC
        """
        return self.nucleotides

    def get_reverse_complement(self):
        """ Returns the reverse complement DNA sequence represented
            as an object of type DNASequence

            >>> seq = DNASequence("ATGC")
            >>> rev = seq.get_reverse_complement()
            >>> print rev
            GCAT
            >>> print type(rev)
            <class '__main__.DNASequence'>
        """
        complement = ''
        dna = self.nucleotides

        # compute the compliment dna string
        for i in range(len(dna)):
            if dna[i] == "A":
                complement = complement + 'T'
            elif dna[i] == "C":
                complement = complement + 'G'
            elif dna[i] == "T":
                complement = complement + 'A'
            elif dna[i] == "G":
                complement = complement + 'C'

        self.complement = complement[::-1]

        return self.complement

    def get_proportion_ACGT(self):
        """ Computes the proportion of nucleotides in the DNA sequence
            that are 'A', 'C', 'G', and 'T'
            returns: a dictionary where each key is a nucleotide and the
                corresponding value is the proportion of nucleotides in the
            DNA sequence that are that nucleotide.
            (NOTE: this doctest will not necessarily always pass due to key
                    re-ordering don't worry about matching the order)
        >>> seq = DNASequence("AAGAGCGCTA")
        >>> d = seq.get_proportion_ACGT()
        >>> print (d['A'], d['C'], d['G'], d['T'])
        (0.4, 0.2, 0.3, 0.1)
        """
        dna = self.nucleotides
        prop = {}
        count = float(len(dna))

        for i in dna:
            if i == "A":
                prop['A'] += 1

        prop[A] = prop[A]/count

        self.proportions = prop

        print prop

        return self.proportions
                



if __name__ == '__main__':
    import doctest
    doctest.testmod()
