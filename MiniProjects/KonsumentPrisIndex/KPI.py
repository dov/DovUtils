#!/usr/bin/python

"""
A module for looking up the Swedish Konsumentprisindex. See:

http://www.scb.se/Pages/TableAndChart____272151.aspx

Dov Grobgeld <dov.grobgeld@gmail.com>
Monday 2011-06-06 08:16

This script is in the public domain.
"""

import re

# This could easily be pulled from the web, but I'm pasting it here from the web page.
kpi_text = """
2011
	306,15 	308,02 	310,11 	311,44 	  	  	  	  	  	  	  	  	 
2010
	299,79 	301,59 	302,32 	302,36 	302,92 	302,97 	302,04 	302,06 	304,60 	305,57 	306,58 	308,73 	303,46
2009
	297,88 	297,95 	298,80 	299,26 	299,45 	300,17 	298,80 	299,42 	300,35 	301,11 	301,03 	301,69 	299,66
2008
	294,09 	295,28 	298,08 	299,67 	300,99 	302,45 	302,11 	301,98 	305,08 	305,56 	303,06 	298,99 	300,61
2007
	285,01 	286,45 	288,33 	289,79 	289,48 	289,95 	289,49 	289,41 	292,30 	293,85 	295,75 	296,32 	290,51
2006
	279,59 	280,90 	282,89 	284,32 	284,76 	284,68 	284,19 	284,38 	286,04 	286,07 	286,43 	286,43 	284,22
2005
	277,9 	279,2 	279,8 	280,2 	280,3 	280,4 	279,4 	279,9 	281,9 	282,4 	281,7 	281,8 	280,4
2004
	278,0 	277,3 	279,4 	279,4 	280,1 	278,9 	278,5 	278,2 	280,2 	281,0 	279,4 	279,4 	279,2
2003
	276,0 	278,4 	279,8 	278,8 	278,5 	277,7 	276,8 	276,7 	278,7 	278,9 	278,3 	278,6 	278,1
2002
	268,8 	269,4 	271,8 	272,9 	273,6 	273,2 	272,3 	272,4 	274,5 	275,4 	274,7 	275,1 	272,8
2001
	261,7 	262,6 	264,6 	266,9 	268,7 	268,3 	266,9 	267,6 	269,9 	269,1 	269,2 	269,5 	267,1
2000
	257,5 	258,7 	259,9 	260,0 	261,3 	261,2 	260,0 	260,2 	262,0 	262,6 	262,7 	262,5 	260,7
1999
	256,2 	256,3 	257,3 	257,9 	258,3 	258,7 	257,6 	257,6 	259,4 	259,7 	259,0 	259,6 	258,1
1998
	256,9 	256,6 	257,0 	257,7 	258,1 	257,6 	257,0 	255,7 	256,8 	257,3 	256,7 	256,2 	257,0
1997
	254,6 	254,2 	255,2 	257,0 	257,0 	257,4 	257,3 	257,4 	259,8 	259,6 	259,2 	259,1 	257,3
1996
	255,6 	255,8 	257,0 	257,6 	257,3 	256,3 	255,7 	254,5 	256,0 	255,9 	255,3 	254,9 	256,0
1995
	251,3 	252,3 	253,3 	255,0 	255,3 	255,1 	254,8 	254,5 	256,2 	256,9 	256,8 	256,0 	254,8
1994
	245,1 	245,9 	246,8 	247,8 	248,3 	248,4 	248,4 	248,5 	250,7 	251,0 	250,8 	250,4 	248,5
1993
	241,0 	241,6 	242,7 	243,7 	243,1 	242,3 	241,9 	242,3 	244,5 	245,2 	245,3 	244,3 	243,2
1992
	230,2 	230,3 	231,3 	231,9 	232,0 	231,5 	231,2 	231,3 	234,6 	235,1 	234,0 	234,9 	232,4
1991
	218,9 	225,0 	225,8 	227,1 	227,3 	227,0 	227,1 	226,7 	229,2 	230,1 	231,1 	230,8 	227,2
1990
	199,0 	199,9 	205,4 	205,2 	206,4 	206,2 	208,2 	209,6 	212,0 	213,4 	214,1 	213,9 	207,8
1989
	183,0 	184,0 	184,7 	186,5 	187,3 	187,9 	187,9 	188,7 	190,2 	191,8 	192,2 	192,8 	188,1
1988
	171,6 	172,9 	173,7 	175,2 	175,8 	176,3 	177,1 	177,5 	178,8 	180,2 	180,5 	180,9 	176,7
1987
	164,4 	164,4 	164,7 	165,1 	165,2 	164,9 	166,9 	167,8 	169,4 	170,1 	170,7 	170,7 	167,0
1986
	158,9 	159,0 	158,7 	159,7 	159,7 	159,7 	160,1 	159,9 	161,3 	161,9 	161,9 	162,3 	160,3
1985
	149,6 	151,0 	152,1 	152,7 	154,5 	153,9 	153,8 	153,8 	154,5 	155,5 	156,5 	157,1 	153,8
1984
	139,4 	138,9 	140,9 	141,8 	142,8 	142,4 	142,8 	143,9 	144,8 	145,5 	146,4 	148,8 	143,2
1983
	129,1 	128,8 	129,3 	130,3 	131,1 	131,8 	132,9 	133,5 	134,5 	135,6 	136,4 	137,5 	132,6
1982
	117,4 	119,0 	119,3 	120,1 	120,7 	121,1 	121,9 	122,2 	122,9 	124,6 	125,6 	125,9 	121,7
1981
	107,2 	109,3 	109,8 	110,5 	111,2 	111,6 	112,6 	113,5 	114,3 	115,0 	115,4 	114,9 	112,1
1980
	95,3 	96,8 	97,2 	97,9 	98,2 	98,5 	99,3 	99,9 	102,7 	104,2 	104,8 	105,2 	100,0
"""

class KPI:
    """A class for the swedish Konsumentprisindex"""
    def __init__(self):
        """Convert the kpi text to two arrays:
            - KpiMonthly starting 1980
            - KpiYearly starting at 1980
        """
        # Split on newlines and get rid of first empty line
        kpi_years_text = kpi_text.split('\n')[1:]
    
        # Get last year indexed
        last_year = int(kpi_years_text[0])
        num_years = last_year-1980+1
    
        # Build arrays for years and months
        kpi_years = [None]*num_years
        kpi_months = [None]*(num_years*12)
    
        # Loop over the year text and build the arrays
        for i in range(num_years):
            year = int(kpi_years_text[i*2])
            # Turn commas into period and get rid of spaces.
            # Finally split on tabs and skip first entry.
            kpi_year = re.sub(',','.',
                              re.sub(' ','',
                                     kpi_years_text[i*2+1])).split('\t')[1:]
            # Convert to floating point
            kpi_year = [float(f) for f in kpi_year if len(f)]

            # store the monthly averages
            for m in range(len(kpi_year)):
                if m==12:
                    break
                kpi_months[(year-1980)*12+m]=kpi_year[m]

            # store the yearly average
            if len(kpi_year)>12:
                kpi_years[year-1980]=kpi_year[12]
  
        # store as class members
        self.kpi_months=kpi_months
        self.kpi_years=kpi_years
  
    def get_monthly(self,year,month):
        """Get the average kpi for the requested month. Note that month is zero based"""
        return self.kpi_months[(year-1980)*12+month]
  
    def get_yearly(self,year):
        """Get the average kpi for the requested year"""
        idx = year-1980

        # Use precalculated
        if not self.kpi_years[idx] is None:
            return self.kpi_years[idx]

        # Else calculate average
        s=0
        n=0
        for i in range(12):
            kpi = self.kpi_months[idx*12+i]
            if not kpi is None:
                s+= kpi
                n+= 1
        return 1.0*s/n
  
    def get_latest_kpi(self):
        """Get the latest valid kpi from the database"""
        for kpi in reversed(self.kpi_months):
            if not kpi is None:
                return kpi

if __name__=='__main__':
    kpi = KPI()

    print kpi.get_monthly(1980,0)
    print kpi.get_latest_kpi()
