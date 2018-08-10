"""
    datasheets_newbie.py
    
    Module to illustrate how to utilize the SquareSpace python datasheets package
    to capture data into a GoogleSheet from the Raspberry Pi SenseHat.
    
    More information on the datasheets package here: https://github.com/Squarespace/datasheets.
    
    Testing this module on the Raspberry Pi Model 3 B+ we received at
    Picademy Certified Educator training August 6-7 2018 (Seattle)
    
    Author: Brad Hontz, Raspberry Pi Certified Educator
"""

import sys, os, time   # you use this modules so often I usually just import them as a habit
from datetime import datetime  # used for timestamping our data
import datasheets
import pandas as pd  # here I use an alias for pandas (pd) as I know I'll be typing this alot
from sense_hat import SenseHat   # the Raspberry Pi SenseHat module we'd used in class

def CreateNewGoogleSheet(strSheetName, strYourEmailAddress, lstTabs):
    """
        It's relatively difficult to generalize the creation of a brand new sheet into a function,
        so I'll just list the steps within this function as an illustrative example.
        NOTE YOU ONLY NEED TO EXECUTE THIS FUNCTION ONE TIME, as you'll see in the main section of this module.
        
        In this example we're creating a four column table.  I'm providing an initial row of data to help GoogleSheets
        identify what sort (type) of data I'm planning to populate within the four columns.  One of the columns will hold a DATE and some
        of the code below illustrates how to add an actual date (as opposed to a string) into your GoogleSheet.
        
        You can delete this default row from within GoogleSheets when you first access the sheet.
        
        The arguments to this function are:
            strSheetName : What you'll be calling the GoogleSheet this function creates
            strYourEmailAddress:  e.g. "me@gmail.com"
            lstTabs: a python list containing the name of the tabs you want in the sheet, e.g. ["GroupA", "GroupB"].  Note that all tabs will have the same column format
    """
    date_value = pd.to_datetime(str(datetime.now()))  # gets the current datetime stamp from the Raspberry Pi
    df = pd.DataFrame([(date_value, 99.99999,99.99999,99.99999)], columns=['DATETIME','TEMP','HUMIDITY','PRESSURE'])   # 4 example data values and 4 column labels
    workbook = client.create_workbook(strSheetName)
    workbook.share(strYourEmailAddress, role='writer', notify=True, message="I'm sharing this GoogleSheet with you!")  # ! IMPORTANT ! You need to share this with your GoogleSheets email account!
    
    for item in lstTabs:   # for each of the tab names in the list lstTabs, create a new tab within this sheet and populate that tab with the same data
        tab = workbook.create_tab(item)
        tab.insert_data(df, index=False, autoformat=True)
        del tab  # This is cleanup of memory, not physical deletion of the worksheet tab
        
    workbook.delete_tab("Sheet1")   # delete the GoogleSheet tab that is created by default
        
    return workbook

def FetchColumnHeaderFromTab(workbook, strTabName):
    """
        The "append_data" function provided in this module just assumes you'll always be appending your data into the sheet
        in the order of the sheet's columns.  I added this function to make sure that really happens.
        Basically, after the sheet is open, you call this function which returns a list of the column header labels (lstColumnHeader).
        We can then use this list to reorder the data we're going to append to the spreadsheet to be sure that it
        really matches the spreadsheet's column ordering.
    """
    tab = workbook.fetch_tab(strTabName)
    df = tab.fetch_data()   # sadly you need to pull all of the data from the sheet just to determine the column headers
    lstColumnHeader = list(df.columns.values)
    del df   # lets clean up this big block of memory ....
    
    return lstColumnHeader  # now return a list of the column headers in the spreadsheet's column ordering        

def GetSenseHatData(pd, sense):
    """
        Returns a single reading from the SenseHat which we append as a single row within our GoogleSheet.
        
        I don't own a SenseHat (!) but I've used code here from our class as an illustration
        
        This function returns a python dictionary which will look something like this example:
        {'DATETIME':2018-08-06 16:49:42.940120, 'TEMP':28.6293258667, 'HUMIDITY':34.62345886232, 'PRESSURE':1021.213123121121}        
    """
    dt = pd.to_datetime(str(datetime.now())) # return the current datetime to the second as a pandas datetime value
    d = {'DATETIME':dt, 'TEMP':28.6293258667, 'HUMIDITY':34.62345886232, 'PRESSURE':1021.213123121121}  # uncomment this line if you don't have a sense hat
    ### comment out the next 5 lines if you don't have a SenseHat!  If you do have a SenseHat, comment out the single line immediately above
    ####d = {}  # initialize a blank dictionary which this function will then return
    ####d["DATETIME"] = dt  
    ####d["TEMP"] = sense.get_temperature()
    ####d["HUMIDITY"] = sense.get_humidity()
    ####d["PRESSURE"] = sense.get_pressure()

    return d

def AppendDataToTab(workbook, strTabName, lstColumnHeader, dictData):
    """
        Append a single row of data in python's dictionary format as represented by argument dictData
        Given a SINGLE ROW of data in python's dictionary format represented by argument dictData
        e.g. {'DATETIME':2018-08-06 16:49:42.940120, 'TEMP':38.2124212312123, 'HUMIDITY':76.12312412312112, 'PRESSURE':1021.213123121121}
        add this ROW (represented by dictData) to the existing tab represented by argument strTabName.
        
        Note that we are not validating the columns we're inserting, we're assuming they match the columns in the worksheet tab.
        We are however assuring that the new row's columns are added into the sheet in the correct ordering
        by way of the lstColumnHead argument.
    """
    tab = workbook.fetch_tab(strTabName)
    df = pd.DataFrame.from_dict([dictData])
    tab.append_data(df[lstColumnHeader], index=False, autoformat=True)  # reorder the new row's data to match the sheets column ordering before appending
    
    return

"""
    This is the "main" part of the module, where the execution actually begins.  This is a common style for python modules; i.e. placing functions above and the
    main executable part below.  As a practice I normally bound the main program in a few lines that track how long it ran (i.e. Start/End of Process)
"""
if __name__ == '__main__':    
    print "hello from module %s. Python version: %s" % (sys.argv[0], sys.version)
    sys.stdout.write("--------------------------------------------------------------\n")
    sys.stdout.write("Start of %s Process: %s\n\n" % (sys.argv[0], time.strftime("%H:%M:%S", time.localtime())))

    client = datasheets.Client(service = True)   # this line returns the client object that we'll use from here on
      
    boolFirstRun = False  # ! IMPORTANT ! After running this THE FIRST TIME and verifying that your Google Sheet was created, change this value to FALSE
    strSheetName = "RaspberryPiSenseHatReadings" # The name of the sheet you wish to create / populate goes here
    strMyEmailAddress = "myemail@gmail.com"   # The google account you typically use for GoogleSheet work goes here (doesn't have to be the same account you registered)
    lstOfTabs = ["GroupA", "GroupB"]   # these are the tabs we will create within our new sheet. We'll create two as an illustration, but we're really only going to write to one here
    
    if boolFirstRun == True:
        workbook = CreateNewGoogleSheet(strSheetName, strMyEmailAddress, lstOfTabs)   # first time we run this module, we create our Google Sheet and add data from the SenseHat.
    else:
        workbook = client.fetch_workbook(strSheetName)  # On subsequent runs (after changing boolFirstRun to False) we append SenseHat data to the same GoogleSheet.

    lstColumnHeader = FetchColumnHeaderFromTab(workbook, "GroupA")   # get the ordering of the sheet's column header labels

    ### this last little block gets data from the Raspberry Pi SenseHat and appends it to the Google Sheet we'd created in our first run of this module
    #sense = SenseHat()  # comment out this line if you don't have a sense hat
    sense = False   #  ... and then add this line in place of the one above (if you don't have a SenseHat).  If you do have a sense hat, just use the line sense = SenseHat() 
    for i in range(100):    # read 100 observations, or you could use while True: and just let the sensor read forever and ever ...
       AppendDataToTab(workbook, "GroupA", lstColumnHeader, GetSenseHatData(pd, sense))   # nesting a call to a function within a function. Note we're only updating GoogleSheet tab "GroupA" 
       time.sleep(1)   # in this example we'll read the sensor every second.  GoogleSheets API limits the number of calls you can make in a second, so this is a good idea
    #sense.clear()  # comment out this line if you don't have a sense hat, but do included it if you have one.

    sys.stdout.write("\n\nEnd of %s Process: %s\n" % (sys.argv[0], time.strftime("%H:%M:%S", time.localtime())))
    sys.stdout.write("-------------------------------------------------------------\n")
    
"""
    APPENDIX: Quick documentation regarding other useful datasheet module methods:
    
    client.delete_workbook(strNameOfWorkbook)    # deletes a workbook by name
    workbook.delete_tab(strNameofTab)  # deletes a tab within a workbook, we do use this above
    client.fetch_workbooks_info()  # creat a pandas dataframe of various info regarding the workbooks this account has created
    workbook.fetch_tab_names()    # create a list of the tabs within this workbook

    For a complete set of documentation, see: https://datasheets.readthedocs.io/en/latest/
"""

