#! usr/bin/env python3

import re
import argparse

parser = argparse.ArgumentParser(
    description = '''This script is used for extract junction from gtf files.''',
    epilog = """Author: Hao Zhang. Please feel free to contact zhanghao.sicau@outlook.com for any help!""")

parser.add_argument('-i', '--input', type = str, help = 'input file')
parser.add_argument('-o', '--output', type = str, help = 'output file')
args = parser.parse_args()


# define function
def extTrans(file):
    anno = open(file, 'r')
    transD = dict()
    exonD = dict()

    for line in anno:
        if not line.startswith('#'):
            line_split = line.strip().split('\t')
            line_type = line_split[2]

            # for transcript

            if line_type == 'transcript':
                chr = line_split[0]
                strand = line_split[6]

                geneIDObj = re.search('gene_id "(\S*)"', line_split[8])
                if geneIDObj is not None:
                    geneID = geneIDObj.group(1)

                transTPMObj = re.search('TPM "(\S*)"', line_split[8])
                if transTPMObj is not None:
                    transTPM = transTPMObj.group(1)

                transIDObj = re.search('transcript_id "(\S*)"', line_split[8])
                if transIDObj is not None:
                    transID = transIDObj.group(1)

                refGeneIDObj = re.search('ref_gene_id "(\S*)"', line_split[8])
                if refGeneIDObj is not None:
                    refGeneID = refGeneIDObj.group(1)

                refTransIDObj = re.search('reference_id "(\S*)"', line_split[8])
                if refTransIDObj is not None:
                    refTransID = refTransIDObj.group(1)

                refGeneNameObj = re.search('ref_gene_name "(\S*)"', line_split[8])
                if refGeneNameObj is not None:
                    refGeneName = refGeneNameObj.group(1)
                
                if transID not in transD:
                    if refTransIDObj is not None:
                        transD[transID] = [chr, strand, transID, refTransID, geneID, refGeneID, refGeneName, transTPM]
                    else:
                        transD[transID] = [chr, strand, transID, geneID, transTPM]
                else:
                    print('{0} is duplicated.'.format(transID))
                

            # for exon
            if line_type == 'exon':
                start = line_split[3]
                end = line_split[4]
                
                # search trans_id
                transIDObj = re.search('transcript_id "(\S*)"', line_split[8])
                if transIDObj is not None:
                    transID = transIDObj.group(1)

                # add location
                if transID not in exonD:
                    exonD[transID] = list()
                
                exonD[transID].append(start)
                exonD[transID].append(end)


    # extract junction
    junctionD = dict()
    for trans_i in exonD:
        length_i = len(exonD[trans_i])
        if length_i > 2:
            junctionD[trans_i] = list()
            time = int((length_i - 2) / 2)
            for time_i in range(time):
                junction_start_i = int(exonD[trans_i][2 * time_i + 1]) + 1
                junction_end_i = int(exonD[trans_i][2 * time_i + 2]) - 1
                junction_i = "{0}:{1}|{2}:{3}".format(transD[trans_i][0], junction_start_i, junction_end_i, transD[trans_i][1])
                junctionD[trans_i].append(junction_i)
    
    return junctionD, transD, exonD

# run the extract function
junctionD, transD, exonD = extTrans(args.input)

# make the table
table = open(args.output, 'w')
for trans_i in junctionD:
    for junction_i in junctionD[trans_i]:

        if len(transD[trans_i]) == 8:
            newline = "{0}\t{1}\t{2}".format(junction_i, transD[trans_i][3], transD[trans_i][5])
            print(newline, file = table)

        else:
            trans_formal_i = transD[trans_i][0] + ":" + ':'.join(exonD[trans_i])
            newline = "{0}\t{1}\tNA".format(junction_i, trans_formal_i)
            print(newline, file = table)
