# Bioinformatic Tools

## Extract_uniq_reads.py

[Compatibility: Python3]
This script is used for extracting unique reads from **SAM** files by comparing the id of each read and removing the duplicated ones. The input should be one SAM file, and there must be one subdirectory named "header" to store the header information of the SAM files. In the "header" subdirectory, header information files should be named with the prefix plus the suffix `_header.sam` (for example, 1_header.sam, where '1' is the prefix). BTW, the header information can be generated by Samtools (samtools view -H).

**Usage**: `python3 Extract_uniq_reads.py sample_name.sam prefix`
