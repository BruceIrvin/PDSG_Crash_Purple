# PDX Data Science Meetup: Crash Data Week 3
# 
# Our goal for this four-week meetup is to analyze Oregon Department of
# Transportation data for automobile collisions and use the data to
# forecast future collision behavior.
#
# the goal for this week is to reduce the large(r) original data set 
# to only data about crashes-with-injuries. this python code iterates
# through each year, filters rows, drops columns
# to create daily counts of crashes with injuries
#
# we store the data separately for each year so that we can easily 
# pick and choose years to use for analysis next week

import pandas as pd
import datetime

# clean up the dates
# the data files split the dates into month, day and year which is not very useful
# so this code joins these fields and creates a "Date" field
def to_datetime (row):
    month=row['Crash Month']
    day=row['Crash Day']
    year=row['Crash Year']
    dstr = str(month)+"/"+str(day)+"/"+str(year)
    dt = datetime.datetime.strptime(dstr, "%m/%d/%Y").date()
    return(dt)

datadir = 'data'
years = [2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015]

for year in years:
    print("Processing year", year)
    filename = datadir + "/" + "SW_Crashes_" + str(year) + "_CDS501.csv"
    df = (pd.read_csv(filename, low_memory=False))

#split the data by record type and cut the empty columns
    crashes = df.loc[df['Record Type'] == 1]
    crashes = crashes.dropna(axis='columns', how='all')

    num = crashes.shape[0]
    print (num,"crashes found")

# without the next three lines pandas treats these columns as
# floats which is not good
# not sure why it does this, they appear to be ints in the data files
# also not sure if there is a better way to handle this
    crashes['Crash Month'] = crashes['Crash Month'].astype(int)
    crashes['Crash Day'] = crashes['Crash Day'].astype(int)
    crashes['Crash Year'] = crashes['Crash Year'].astype(int)

    crashes['Date'] = crashes.apply(to_datetime, axis=1)

    print("Starting date for data set: ", crashes['Date'].min())
    print("Ending date for data set: ", crashes['Date'].max())

# reduce to crashes that have injuries
    injury_selector = crashes['Total Non-Fatal Injury Count'] >= 1
    winj = crashes[injury_selector]
    print (winj.shape[0], "crashes with injuries")

# sum to one bin per day
    date_counts = winj['Date'].value_counts()

# fix up the DataFrame
    df = date_counts.to_frame()
    df['ds'] = df.index
    df.columns = ['y','ds']
    df.sort_values('ds',inplace=True)
    df.reset_index(drop=True,inplace=True)

# write the simplified data to file for further analysis
    outfilename = "./"+datadir+"/"+"Counts_"+str(year)+".csv"
    df.to_csv(outfilename)

    print("*******************************\n\n")


