#!/usr/bin/env python

import csv
import sys

class DataFields:
    WEO_COUNTRY_CODE,                                       \
    ISO,                                                    \
    WEO_SUBJECT_CODE,                                       \
    COUNTRY,                                                \
    SUBJECT_DESCRIPTOR,                                     \
    SUBJECT_NOTES,                                          \
    UNITS,                                                  \
    SCALE,                                                  \
    COUNTRY_SPECIFIC_NOTES,                                 \
    Y1980, Y1981, Y1982, Y1983, Y1984, Y1985, Y1986, Y1987, \
    Y1988, Y1989, Y1990, Y1991, Y1992, Y1993, Y1994, Y1995, \
    Y1996, Y1997, Y1998, Y1999, Y2000, Y2001, Y2002, Y2003, \
    Y2004, Y2005, Y2006, Y2007, Y2008, Y2009, Y2010, Y2011, \
    Y2012, Y2013, Y2014, Y2015,                             \
    ESTIMATES_START_AFTER = range(0, 46)

def main(args):
    try:
        path = args[1]
        outfile = args[2]
    except IndexError:
        sys.stderr.write("Usage: %s <data file path> <csv output file>\n" % args[0])
        return True

    generate(path, outfile)
    return False

def generate(path, outfile):
    "Parse the tab separated value file and generates the CSV file"
    fd = open(path, "r")
    fd.readline() # skip the header

    out = csv.writer(open(outfile, "w"))
    out.writerow(["country_code", "time", "value"])

    for line in fd:
        analyze_row(line, out)

def analyze_row(row, csvfile):
    if not row.strip(): return # skip empty lines
    if row.startswith("International Monetary Fund, World Economic Outlook Database"):
        # last row, ignore
        return

    item = row.split("\t")

    if item[DataFields.SUBJECT_DESCRIPTOR] != "Gross domestic product, current prices":
        # we're interested only in this type of subject descriptor
        return
    if item[DataFields.UNITS] != "U.S. dollars" or item[DataFields.SCALE] != "Billions":
        # only consider dollar values
        return

    csvfile.writerow([item[DataFields.ISO], 2005, gdp_to_number(item[DataFields.Y2005])])
    csvfile.writerow([item[DataFields.ISO], 2006, gdp_to_number(item[DataFields.Y2006])])
    csvfile.writerow([item[DataFields.ISO], 2007, gdp_to_number(item[DataFields.Y2007])])
    csvfile.writerow([item[DataFields.ISO], 2008, gdp_to_number(item[DataFields.Y2008])])
    csvfile.writerow([item[DataFields.ISO], 2009, gdp_to_number(item[DataFields.Y2009])])
    csvfile.writerow([item[DataFields.ISO], 2010, gdp_to_number(item[DataFields.Y2010])])

def gdp_to_number(gdp):
    """
    Convert a GDP string (that contains points and commas as decimal
    separators) to a "real" python number
    """
    if gdp == "n/a":
        # if the data isn't available, just set it to 0
        return 0
    billions, rest = gdp.split(".")
    billions = "".join(billions.split(","))
    return float("%s.%s" % (billions, rest))

if __name__ == '__main__':
    sys.exit(main(sys.argv))
