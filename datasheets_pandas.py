"""
    datasheets_pandas.py
    
    This module illustrates how to use the python pandas module to
    perform basic statistical operations from a GoogleSheet.
    
    Keeping in the Raspberry Pi SenseHat theme of datasheets_newbie.py,
    I found some SenseHat data here: https://www.raspberrypi.org/learning/astro-pi-flight-data-analysis/worksheet/
    that was collected from the ISS.
    
    Be sure to place the astro-pi-flight-data.csv file found within this GitHub repo in the same folder
    as this python module, as we'll use this data to populate your GoogleSheet and then perform some elementary statistics.
    Note that you should run datasheets_newbie.py FIRST as that will create the RaspberryPiSenseHatReadings GoogleSheet
    that is referenced within this module.
    
    Testing this module on the Raspberry Pi Model 3 B+ we received at
    Picademy Certified Educator training August 6-7 2018 (Seattle)
    
    Author: Brad Hontz, Raspberry Pi Certified Educator
"""
import os, sys, time
import datasheets
import pandas as pd

"""
    This is the "main" part of the module, where the execution actually begins.  This is a common style for python modules; i.e. placing functions above and the
    main executable part below.  As a practice I normally bound the main program in a few lines that track how long it ran (i.e. Start/End of Process)
"""
if __name__ == '__main__':    
    print ("hello from module %s. Python version: %s" % (sys.argv[0], sys.version))
    sys.stdout.write("--------------------------------------------------------------\n")
    sys.stdout.write("Start of %s Process: %s\n\n" % (sys.argv[0], time.strftime("%H:%M:%S", time.localtime())))

    strPathFileName = "/home/pi/astro-pi-flight-data.csv"   # or whatever folder you've placed this code
    strSheetName = "RaspberryPiSenseHatReadings" # The name of the sheet you wish to create / populate goes here

    client = datasheets.Client(service = True)   # this line returns the client object that we'll use from here on
    workbook = client.fetch_workbook(strSheetName)
    try:
        tab = workbook.create_tab("AstroPi")  # let's create a new tab in our GoogleSheet to hold the data from our CSV file
    except:
        workbook.delete_tab("AstroPi")   # ... if there's already an AstroPi tab, delete it and replace it with a new one.
        tab = workbook.create_tab("AstroPi")
    
    df = pd.read_csv(strPathFileName)   # pandas provides a method to import data from a CSV into a dataframe in one easy step
    tab.insert_data(df, index=False, autoformat=True)  # now we push the data into our the AstroPi tab in our GoogleSheet in one step
    
    del df   # just for kicks let's delete the DataFrame containing the data we read from our CSV file and ...
    df = tab.fetch_data()  # ... fetch it back from our GoogleSheet to illustrate how to read all the data from an entire GoogleSheet tab
        
    """
        Now that we have our Panda's DataFrame loaded with data from our GoogleSheet (tab AstroPi), 
        let's experiment with statistical analysis of our Panda's DataFrame        
    """
    # Here's a handy grab bag of basic statistics for column you specify, using the DataFrame describe() method
    print ("|------------------ Using Describe Method -------------------------|")
    print (df["TEMP"].describe())   
    print (df["HUMIDITY"].describe())
    print (df["PRESSURE"].describe())
    
    print ("|----------------- Correlation Matrix -----------------------------|")
    print (df.corr())   # here's how you'd print a correlation matrix of your data
    
    # within this particular example data set, it doesn't really make sense to "sum" anything, but here's how you'd do it!
    print ("|--------------------Example Summation ----------------------------|")
    print (df["TEMP"].sum())

    print ("|---------------------Means and Medians ----------------------------|")
    print (df.mean(axis=0))  # Here's how you can concurrently create just the means for all columns in your DataFrame
    print (df.median(axis=0)) # ... and the median and mode methods works the same way

    print ("|---------------------Count of Non NA Items------------------------|")
    print (df.count(axis=0))  # sometimes just getting a count is useful, in particular if your data includes missing values    
    
    # See: https://pandas.pydata.org/pandas-docs/stable/ for further documentation of Panada's methods
    
    del df  # clean up some memory before we depart!
    
    sys.stdout.write("\n\nEnd of %s Process: %s\n" % (sys.argv[0], time.strftime("%H:%M:%S", time.localtime())))
    sys.stdout.write("-------------------------------------------------------------\n")

