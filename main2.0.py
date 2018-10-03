from readfasta import readfasta
from genetic_code import code
from random import randint
import glob, os

def main():
    print( "Bioinformatics - Assignment 1 - Group 3" )

    random_was_right = 0
    we_were_right = 0
    number_of_files_scanned = 0
    ACTUAL_READING_FRAME = 1

    os.chdir( os.getcwd() + "/genes/" )
    for file in glob.glob( "*.fsa" ):
        gene = readfasta( file )[0][1]
        rfs = get_all_reading_frames( gene )
        print( "\nThere are " + str( find_intron( gene ) ) + " introns" )
        print( gene )

        if randint( 0, 5 ) == ACTUAL_READING_FRAME:
            random_was_right = random_was_right + 1

        if find_best_reading_frame( rfs ) == ACTUAL_READING_FRAME:
            we_were_right = we_were_right + 1

        number_of_files_scanned = number_of_files_scanned + 1

    print()
    print( str( number_of_files_scanned ) + " genes scanned" )
    print( "Our program was right " +
          str( we_were_right/number_of_files_scanned * 100 )
           + "% of the time" )
    print( "Random was right " +
           str( random_was_right/number_of_files_scanned * 100 )
           + "% of the time" )

def find_best_reading_frame( rfs ):
    #
    # PUT OUR CODE HERE
    #

    rf_scores = [0, 0, 0, 0, 0, 0]
    possible_orf_list = []

    # rf_number: the six possible reading frames, 0 through 5
    # rf_bases: a string with all the bases of the reading frame
    for rf_number, rf_bases in enumerate( rfs ):
        this_rf_score = 0

        # gets list of pairs of the start and stop indexes of the
        # possible orfs in the rf_number-th reading frame
        porfs = possible_orfs(rf_bases)
        possible_orf_list.append(porfs)

        # if the possible orfs are in an AT rich region, 
        # increase the score
        for porf in porfs:
            if at_rich_check(rf_bases, porf[0]):
                rf_scores[rf_number] = rf_scores[rf_number] + 1

    # get the index of the best reading frame score
    best_rf = rf_scores.index( max( rf_scores ) )

    print( rf_scores )
    print( "The best ORF is ORF" + str( best_rf ) + "!" )

    return best_rf

def get_all_reading_frames( gene ):
    rf_list = []
    rf_list.append( gene )
    rf_list.append( gene[1:] ) # not including first character of string
    rf_list.append( gene[2:] ) # not including first or second

    rev = gene[::-1]
    rf_list.append( rev ) # reverse the string
    rf_list.append( rev[1:] )
    rf_list.append( rev[2:] )

    return rf_list

#outputs possible orfs of over length 50 codons and returns them as a list
##of pairs of the index of the first and last basepair
def possible_orfs( dna ):
    orf_list = []
    position_of_last_start = 0
    looking_for_start = True
    for i in range( 0, len( dna ), 3 ):
        codon = dna[i:i + 3]
        
        if codon == 'ATG' and looking_for_start == True:
            looking_for_start = False
            postion_of_last_start = i
        if is_stop_codon( codon ) and looking_for_start == False:
            looking_for_start = True
            if ( ( i+3 ) - postion_of_last_start ) >= 50 * 3:
                orf_list.append( [postion_of_last_start, i + 3] )
    return orf_list

def is_stop_codon( codon ):
    return codon == 'TAA' or codon == 'TAG' or codon == 'TGA'

def at_rich_check( sequence, start_index ):
    if start_index < 200:
        return False

    at_rich_region = sequence[ start_index - 200:start_index - 1 ]
    intergenic_region = sequence[ start_index + 3:start_index + 202 ]
    
    rich_at_count = 0
    for i in range( 0, 199 ):
        if at_rich_region[ i ] == 'A' or at_rich_region[ i ] == 'T':
            rich_at_count += 1

    intergenic_at_count = 0
    for i in range( 0, 199 ):
        if intergenic_region[ i ] == 'A' or intergenic_region[ i ] == 'T':
            intergenic_at_count += 1

    return rich_at_count > intergenic_at_count

#3' splice site UAG or CAG
#intron 5' sequence GTATGT
#Rian's Code
def find_intron( dna ): 
    rna = dna.replace( 'T', 'U' )
    pos_last_start = 0
    looking_for_start = True # while true, look for first start and ignore stops,
                             # if false, look until stop is found
    count = 0
    for i in range( 0, len( rna ), 1 ):
        start_seq = rna[ i:i + 6 ]
        end_seq = rna[ i:i + 3 ]
        if start_seq == "GUAUGU" and looking_for_start == True:
            looking_for_start = False
            pos_last_start = i
            print( "\nStart of intron at " + str( pos_last_start ) )
        if ( end_seq == "UAG" or end_seq == "CAG" ) and looking_for_start == False:
            looking_for_start = True
            pos_end = i + 3 # Add 3 to see where the last base of the stop is
            count += 1
            print( "\nEnd of intron at " + str( pos_end ) )
            
    return count

main()