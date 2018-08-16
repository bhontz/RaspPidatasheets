**Hi Raspberry Pi Seattle Group A Educators!**

Pleasure to meet and work with you week of August 6th in Seattle!

During the week, "Google Sheets" was mentioned at multiple occassions.   I'm actively using Google Sheets with Python so I thought I'd share info on a Python module I'm using that was developed by the folks at [SquareSpace](https://www.squarespace.com).

The two main reasons why I like this module are (a) super easy to use in practice (b) it integrates python's data science module "pandas" which can serve as a stepping stone for future data science projects (e.g. applying statistical analysis of your Pi collected data).

*One time setup steps*

The one time setup is actually more difficult than using this module!  To get started you'll need to install the *datasheets* and *pandas* python packages on your Raspberry Pi.   I wrestled with this install at first as there are actually two versions of Python installed on our Picademy Pi's - python 2.7 and python3.5.   We used Thonny in our Picademy session, and Thonny uses python3.5, so the instructions provided below pertain to setup for running these modules from Thonny.

So on to the setup!  From the "Terminal" (i.e. the black prompt icon on the toolbar) of the Raspberry Pi, type each of these lines in succession:

	sudo apt install python3-sklearn-pandas
	sudo pip3 install datasheets

You'll see a number of messages flying by as each one of these packages installs.  Don't worry about the details unless you see a very obvious indication of errrors occurring (and then post the problem here within GitHub issues).

After installing the supporting packages as per the step above, you'll additionally need to follow a **one time** authentication process to provide the appropriate permissions for your Google account (if you're using Google Sheets then by definition you already have a Google account).   

The Google authentication process entails filling out a few forms on Google's website which will create a "permissions file" that you can then copy to your Pi.   [The entire one-time Google authentication process is documented in step-by-step form HERE](https://datasheets.readthedocs.io/en/latest/getting_oauth_credentials.html#getting-oauth-credentials).       

The outcome of this process is the creation of two JSON files with filenames *client_secrets.json* and *service_key.json*.  You need to copy these two files into a ~/.datasheets folder on your Pi.  You can create this folder from the Raspberry Pi's Terminal application, using the command:

	mkdir ~/.datasheets 

There are many different ways to copy the two JSON files from your computer to Raspberry Pi.  At the end of our 2nd class day, (Canadian) Tom pointed out that VNC can be used to connect a computer to the Raspberry Pi, and that the VNC app additionally supports copying files back and forth.  You could put the files in dropbox or Google Drive and then access the files from the Raspberry Pi's web browser.   You can email the files to yourself and then get your email from the Raspberry Pi.  [Or you can use Filezilla as per this blog post](http://trevorappleton.blogspot.com/2014/03/remotely-copy-files-to-and-from-your.html).  

*Now the code...*

Within this GitHub repository I'm sharing two different python modules that will illustrate how to use datasheets.  The first "datasheets_newbie.py" module shows the basic usage of datasheets; how to create a new Google Sheet, create tabs on the sheet, dump data in, append data to, etc.  I've tried to be liberal in my commenting to help you follow along.  **Pay particular attention to the SHARING of the sheets, as you really need to share each newly created sheet WITH YOURSELF to begin using it (this initially resulted in some serious head scratching on my part).**

The second module "datasheets_pandas.py" illustrates how to utilize the pandas module to do some very basic statistics of the columns within the data sheets you'll create.  The datasheets package uses the python pandas dataframe object as the means of moving data around, and when data is held within a pandas dataframe, you can relatively easily apply all sorts of statistical testing via the panda's package!  I found some data from the IIS's AstroPi program to use as an illustration (astro-pi-flight-data.csv) and included it within this GitHub repo.  The datasheets_pandas.py module will look for this file.

If you have any interest in data science or statistical analysis, python pandas is a **HUGE** subject on its own, and I'd encourage you to visit https://pandas.pydata.org if you'd like to learn more.  There's a getting starting video on this page if you want to get a quick feel for what pandas is all about.  Pandas and the [R package](https://www.r-project.org) are the two of the most popular "core" tools used by data scientists today.  As a retired data scientist, I'm always looking for ways to promote data science teaching as component of STEM education ;)

Lastly, if you're a "don't help me", self-serving kind of user,  [the underlying original Squarespace GitHub page supporting datasheets can be found here](https://github.com/Squarespace/datasheets).

Good luck fellow Pi certified educators!

*Footnote (disclaimer!):*

While putting this example together I noted that Google "throttles" the use of the GoogleSheets API, meaning they allow a limited number of calls to the API a second (I believe 100).  If you are adding data from a sensor to a GoogleSheet every second (or less) it is VERY EASY to meet this limit.  Note however, that there isn't a limit to just dumping a bunch of data into a sheet in one go, as we do within the datasheets_pandas.py module example.  Just a note to be aware of this limitation and use this tool accordingly.  In my own usage I typically dump data in one go and hadn't run across this issue prior.
