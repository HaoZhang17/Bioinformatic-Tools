#!/usr/bin/env python3
'''
This python script runs with Python3 to extract unique reads from the SAM format file. 
There should be a subdirectory named "header" to store the header information of the SAM file. 
The header information can be extracted using Samtools (samtools view -H in.bam > out.sam). 
Now this script only support one SAM file as the input now!
'''

import sys, os, time

if len(sys.argv) > 1:
	filename = sys.argv[1]
	sample_num = sys.argv[2]

else:
	filename = input('Enter the file name (SAM file): ')
	sample_num = input('Enter the prefix of output file: ')

start_time = time.time()
start_localtime = time.asctime(time.localtime(time.time()))


# read file and acquire read IDs
keysList = list()
input_file = open(filename, 'r')
total_line = 0
for line in input_file:
	if not line.startswith('@'):
		line_split = line.split('\t')
		keysList.append(line_split[0])
	total_line += 1
input_file.close()
print('Done reading the file.')

# get unique and duplicated read IDs
uniq_key = set()
dupli_key = set()
q = 0
for key_i in keysList:
	''' # method 2
	if key_i not in uniq_key and key_i not in dupli_key:
		uniq_key.add(key_i)
	else:
		dupli_key.add(key_i)
		uniq_key.discard(key_i)
	'''
	
	# method 1
	if key_i not in uniq_key and key_i not in dupli_key:
		uniq_key.add(key_i)
	else:
		if key_i not in dupli_key:
			dupli_key.add(key_i)
			uniq_key.remove(key_i)				#!!!!!!!

	# for alert	
	q += 1
	if q%100000 == 0:
		print('Dealing with read ' + str(q) + '/' + str(len(keysList)))
print('There are ' + str(len(uniq_key)) + ' unique reads.')


# get the header lines of input sam file and write to the output file
os.chdir('./header')
header_string = ''
header = open(str(sample_num) + '_header.sam', 'r')
for line in header:
	header_string += line
header.close()

os.chdir('../')
outfile = open(str(sample_num) + '_uniq_accepted_hits.sam', 'w')
print(header_string, file = outfile, end = '')


# start to compare and write the unique reads to the output file
print('Start to summarize information...')
input_file = open(filename, 'r')

q_2 = 0
for line in input_file:
	line_split = line.split('\t')
	if line_split[0] in uniq_key:
		print(line, file = outfile, end = '')

	# for alert
	q_2 += 1
	if q_2%100000 == 0:
		print('Summarizing line ' + str(q_2) + '/' + str(total_line))

input_file.close()
outfile.close()

end_time = time.time()
end_localtime = time.asctime(time.localtime(time.time()))
total_time = end_time - start_time
print('All done!\nThe start time is ' + start_localtime + '.\nThe end time is' + end_localtime + '\nThis program lasted for %.2f seconds' % (total_time))
