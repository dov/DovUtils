#!/usr/bin/python

"""
Calculate the sum of KPI adjusted values from an org-table table.

This script reads an org table where one column (date_col) indicate a date
and several other columns contain swedish monetary values (indicated by vcols).

The script looks up the KPI value for the date and adjust the montary value at
the same row by the KPI value. The values are then summed and the sums are output.

This script was used to calculate the present value of various historical gifts.

Dov Grobgeld <dov.grobgeld@gmail.com>
Monday 2011-06-06 08:15

This script is in the Public Domain.
"""

import sys,re
import dateutil.parser
import KPI

def ary_fmt(v, fmt="%10.0f",sep=' | '):
    """Pretty print an array"""
    return sep.join([fmt%f for f in v])

# The three columns to summarize
vcols = [2,3,4]

# Labels to print - Thes should correspond to the length of vcols
labels = ['G','P','S']

# What column contains the date
date_col = 0

# Create object for querying the kpi database
kpidb = KPI.KPI()
kpi_today = kpidb.get_latest_kpi()

# Initial empty sums
sums = [0]*len(vcols)
kpi_sums = [0]*len(vcols)

# Open the txt files with the org-table
text_file = open(sys.argv[1])
for line in text_file:
    # Is it a table line?
    if not re.search(r'^\|',line):
        continue

    # Split the columns on the vertical bar and get rid of first colmn
    cols = line.split('|')[1:]

    # Get date and get rid of whitespace
    date_string = re.sub(' ','',cols[date_col])

    # Does it look like date? If not continue.
    if not re.search('^\d+',date_string):
        continue

    # Does it contain a dash? If so, let dateutil parse it and get the
    # monthly kpi.
    if re.search('-',date_string):
        date = dateutil.parser.parse(date_string)
        kpi = kpidb.get_monthly(date.year,date.month-1)

    # otherwise it's a year and we get the yearly average
    else:
        kpi = kpidb.get_yearly(int(date_string))

    # loop over vcols and calculate
    for i,vi in enumerate(vcols):
        # Get rid of (?) in the columns
        v = re.sub(r'\(\?\)','',
                   re.sub(' ','',cols[vi]))

        # Check if we have an entry for the column
        if len(v):
            v=float(v)
            # Sum column
            sums[i]+= v
            # kpi adjust and sum the column
            kpi_sums[i]+= kpi_today/kpi*v

print "        | ",ary_fmt(labels,fmt='       %-3s')
print "--------+-"+"+".join(["-"*12]*3)
print "sums    | ",ary_fmt(sums)
print "kpi_sum | ",ary_fmt(kpi_sums)
