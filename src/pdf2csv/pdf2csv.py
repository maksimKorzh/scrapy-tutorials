import pdftotext
import re
import csv

# open PDF file
with open('cisco.pdf', 'rb') as pdf_file:
    pdf = pdftotext.PDF(pdf_file)

# extract tabular text
lines = pdf[1].replace(', ', ' | ').split('\n')[7:]

# CSV table
table = []

# loop over lines in table
for line in lines:
    # replace trailing spaces with comas
    row = re.sub('   ', ',', line)
    
    # reducing the number of comas to one
    row = [cols.strip() for cols in re.sub(',+', ',', row).split(',')]
    
    # handling missed separators
    row = ','.join(row).replace('  ', ',').split(',')
    
    # append row to table
    table.append(row)
    
    print(row)

# write CSV output
with open('cisco.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(table)
    
    
    
    
    
    
