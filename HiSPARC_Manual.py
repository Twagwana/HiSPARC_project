#!/usr/bin/env python
# coding: utf-8

# In[ ]:


The HiSPARC_manual

get_ipython().set_next_input(u'WHY SAPPHIRE');get_ipython().magic(u'pinfo SAPPHIRE')
Because it simplifies data access, simulations and analysis for the HiSPARC experiment.

In this tutorial, we’ll try to give you a feeling for the things you can do with SAPPHiRE.

How can you download data? 
How can you analyze this data? 
How can you produce pulseheight histograms? 
get_ipython().set_next_input(u'How can you calculate the direction of cosmic rays');get_ipython().magic(u'pinfo rays')


# In[1]:


from pylab import *


# In[2]:


#In order to start using sapphire, we have to import the sapphire module


import sapphire


# In[3]:


# Downloading and accessing the Hisparc data
# To access the public data, we have to import the sapphire.esd module
# This module gives us access to the event summary database, 
# which is the raw HiSPARC data with preliminary analysis already included

# We first import the sapphire.esd module
# Then, we download data from station 40001 using the sapphire.esd.quick_download() function.
# 40001(Unam Station)



from sapphire import esd
data = esd.quick_download(40001)


# In[5]:


# The (sapphire.quick_download()) function downloads yesterday’s data, and creates a datafile on the fly.

print(data)


# In[6]:


# If we want to have more control on the date and time we have to import certain modules.
# We have to import the tables module-To save the data.
# We have to import the datatime module-To specify the date and time for which to download the data.

import tables
import datetime
from sapphire import esd


# In[7]:


# We have to create  an empty data file, with the name mydata.h4 to save data


data = tables.open_file('mydata.h5', 'w')

# 'w' means write-It creates an empty file for writing and reading.If there was a file with that name, it will be overwritten.
# Alternatively,
# 'a' means append- It means adding to an existing file without overwriting its contents.
# 'r' means read only- It means reading only, no changes or modifications can be made.


# In[8]:


# To download data, we have to specify the date/time range.
# If we want to download data from the July 24, 2019 all through to July 25, 2019, we can specify this by typing:

start = datetime.datetime(2019, 7, 24)
end = datetime.datetime(2019, 7,25 )

# We also have to specify the time of the day
# Because if we don't, the time is taken to be 12 am meaning there is no data included for July 25.
# Alternatively, we can download data from a two hour interval on July 24 by specifying the hour of day.

start = datetime.datetime(2019, 7 , 24, 20)
end = datetime.datetime(2019, 7 , 24, 22)

# You can specify the time up to second.


# We have stored our time window in two arbitrarily-named variables, start and end.
# To download data from station 40001 and store it in a group with name /s40001.
# We can use the sapphire.esd.download_data() function


esd.download_data(data, '/s40001', 40001, start, end)





# In[9]:


# The function esd.download_data() takes six arguments: file, group, station_number, start, end and type.
# The last one has the defaulet artgument'events', and may be omitted.
# In our example we have opened a file, mydata.h4, and have stored the file handler in the variable data.
# We basically passend data to the function. The group name is /s40001. Group names must start with a letter,
# hence the s for station
# Group names in Pytables are just like folders in directory hierarchy.
# We have specified /path/to/my/hisparc/data/files/for_station/s40001.This has absolutely nothing to do with the files.
# Whatever path you specify, it is all contained inside your data file.

# The station_number is simply the station number. Here we have chosen to download data for station 40001, located at UNAM. 
# The start and end parameters specify the date/time range.
# Finally, 'type', selects whether to download event or weather data.


# We have selected the default, which is events.

# We can also download the weather data by changing the type to 'weather' 

esd.download_data(data, '/s40001', 40001, start, end, type='weather')

# To access the raw data that includes the original detector traces the sapphire.publicdb.download_data() function can be used.
# However, downloading data that way will take much longer.



# In[10]:


# If you want to know what groups and tables are contained within the data file, just print it:

print(data)




# In[11]:


# The object tree gives an overview of all groups and tables. Above the /s40001 group contains two tables, events and weather.
# The events table contains the data from the HiSPARC scintillators,
# while the weather table contains data from (optional) weather station.


# To directly access any object in the hierarchy, you can make use of the data.root object, which points to the root group.
# Then you sspecify the remaining path, with dots instead of slashes.


# Accessing the events table can be done these way:

print(data.root.s40001.events)

# The event table can also be accessed by using its name as a string, by calling get_node on the file handler

print(data.get_node('/s40001/events'))


# Accessing the weather table can be done these way:

print(data.root.s40001.weather)



# The weather table can also be accessed by using its name as a string, by calling get_node on the file handler

print(data.get_node('/s40001/weather'))







# In[12]:


# Obtaining more information can be done by dropping the print statement, and just accessing the object directly.

# PyTables is set up such that it will give more detailed information whenever you specify the object directly.

# Events

data.root.s40001.events 


# In[13]:


# What does all that mean??

# First, this table contains 9957 rows. In total, there are fourteen columns: event_id, timestamp, nano seconds, ext_timestamp, 
# pulsheights, intergrals, n1-n4, t1-t4 and t_trigger. 


# Each event has a unique identifier,event_id. Each event has a Unix timestamp in GPS time, not UTC. 
# Unix timestamp is the number seconds that have paseed since january 1, 1970. 
# The sub-seconds part of the timestamp is given in nanoseconds.
# The ext_timestamp is the full timestamp in nanoseconds. There can't exist another event with the same timestamp, this field
# in combination with the station number uniquely identifies the event.
# The pulseheights and integrals fielids are values derived from the PMT traces by the HiSPARC DAQ.
# The n# columns are derived from the integrals, the t# and t_trigger fields are obtained after analyzing the event traces on 
# the server.


# For some fields there are four values, one for each detector. 
# If a station only has two detectors, the values for the missing detectors are -1.
# If the baseline of the trace could not be determined all these valies are -999.





# In[14]:


# Weather PyTables

data.root.s40001.weather


# In[15]:


# ACCESSING  DATA

# We can access the data in several ways.
# We can address the complete table, or just one or several rows from it.
# We can read out a single column, or select data based on a query.

# We can save us some typing by,

events = data.root.s40001.events 


# We have stired a short-hand reference to the events table.
# We can get the first event:

events[0]


# In[16]:


# That is the first event.It is not, however, immediately clear of what numbers correspong to which columns.
# They are in order, however, so you could find out.
# It is often easier to specify the column you're interested in:

events[0]['pulseheights']


# Which gives us the pulseheights of the first event. You can recognize the same numbers in the full event data above.
# The pulseheights are 16-bit intergers (thus-dtype=int16) and are determined after digitizing the events using an
# analog-digital converter (ADC).
# Each unit corresponds to about -0.57 mV.


# In[17]:


# If you’re interested in the pulseheights of all events, 
# The fastest way to do it is to make use of the Table.col method of the table:

events.col('pulseheights')



# In[18]:


# It is also possible to select data according to a query.
# For instance, to select all events between timestamps 1354320000 and 1354323600 (a one-hour time span).


t0 = 13543200004
t1 = t0 + 3600
sel_events = events.read_where('(t0 <= timestamp) & (timestamp < t1)')
len(sel_events)


# In[19]:


# Thus we have selected 0 events. The variable sel_events no longer points to a table.
# We can no longer make use of the Table.col method, but we can access all pulseheights in the following way:


sel_events['pulseheights']



# In[ ]:





# In[20]:


# The sapphire.time_until module.


# SAPPHIRE includes a handy module:sapphire.time_until.
# This saves you from the hassle of converting timestamps and confusing local time and GPS (or UTC) time.
# It is important to realize that the HiSPARC station uses a GPS clock, and thus saves all timestamps in GPS time,which is
# certainly not local time! You can look up GPS time, but suffice it to say that it is almost equal to UTC time.

# The difference is the leap seconds introduced after 1980. In January 2013, GPS time was ahead of UTC by 16 seconds. 
# Since July 2015, it is ahead by 17 seconds.We will not refer to UTC or local time, but instead always refer to GPS time!



# While you tell SAPPHiRE to download data using year, month, day, hour, minutes, seconds notation, the events table contains,
# timestamps.
# It is often hard to convert between the two.







# It It is easy, however, to screw up and inadvertently convert to local time. 
# For your benefit, we have included the sapphire.time_util.GPSTime class. 
# You instantiate the class by giving it a GPS time to work with. It can either be in date/time notation, or as a timestamp.

# For example, the exact same result is obtained by these two last lines of code:

#import sapphire.time_util
#sapphire.time_until.GPSTime(1354320000)


import sapphire.time_util
sapphire.time_util.GPSTime(2019, 7, 24)
sapphire.time_util.GPSTime(1354320000)







# In[21]:


# If you store the instance, you can then call several methods to convert the date/time to whatever you want.
gpstime = sapphire.time_util.GPSTime(2019, 7, 24)
gpstime.datetime()


# In[22]:



gpstime.description()


# In[23]:



gpstime.gpstimestamp()


# In[24]:


# Or we can do this another way:


gpstime = sapphire.time_util.GPSTime(1563926400)
gpstime.datetime()


# In[25]:


gpstime.description()


# In[26]:


gpstime.gpstimestamp()


# In[ ]:





# In[27]:


# It is now easy to select events occurring between 20:00 and 22:00 hours GPS time on July 24, 2019:

t0 = sapphire.time_util.GPSTime(2019, 7, 24, 20).gpstimestamp()
t1 = sapphire.time_util.GPSTime(2019, 7, 24, 22).gpstimestamp()
t0, t1


# In[28]:



sel_events = events.read_where('(t0 <= timestamp) & (timestamp < t1)')
len(sel_events)


# In[ ]:





# In[29]:


# PLOTTING DATA


# Now that we can access the data, we want to visualize it. Plotting data is a great way to do that.
# And of course, the venerable histogram is still very useful to condense thousands of events into one display.
# Pylab contains an easy function to do just that: hist. Let’s try to recreate a few graphs as seen on the HiSPARC data display.

#The plotting part

ph = events.col('pulseheights')
hist(ph)


# In[ ]:





# In[30]:


# This will not do.
# Firstly, data from the four detectors is pictured as four side-by-side colored bars.
# Secondly, the number of the bins is very low, thirdly the data range continues up to very high values with hardly any events.


# To fix To fix this, we’ll make use of several arguments that can be passed to the hist function. 
# We’ll also make use of some NumPy (documentation) functionality.
# For Pylab documentation, see the Matplotlib site. Try this:

bins = linspace(0, 2000, 101)
hist(ph, bins, histtype='step', log=True)
xlabel("Pulseheight [ADC]")
ylabel("Counts")
title("Pulseheight histogram (log scale)")


# The linspace function returns an array with range from 0 to 2000 with a total number of 101 values.
# The first value is 0, the last is 2000. These are the edges of the bins
# So, 101 values means exactly 100 bins between 0 and 2000.
# The hist function will then plot a stepped histogram with a log scale.
# Finally, we add some labels and titles. 


# In[ ]:


# In the plot above, the gamma and charged particle part of the spectrum are easy to distinguish.


# In[ ]:





# In[31]:


# Obtaining Coincidences

# If you work with HiSPARC data, consistently you’ll be interested in coincidences between HiSPARC stations.
# That is, are there showers which have been observed by multiple stations? 
# To find out, we’ll make use of the sapphire.analysis.coincidences module.

# Performing the Search

import datetime
import tables

from sapphire import download_data, CoincidencesESD


STATIONS = [501, 502, 40001]
START = datetime.datetime(2019, 7, 24)
END = datetime.datetime(2019, 7, 25)

if __name__ == '__main__':
    station_groups = ['/s%d' % u for u in STATIONS]
    data = tables.open_file('data.h5', 'a')
    for station, group in zip(STATIONS, station_groups):
        download_data(data, group, station, START, END)        
        



# In[32]:


# We have downloaded data for three stations. Note that we used the sapphire.esd for downloading.
# Thus, we have no traces and the download is quick. 
# In order to see what the datafile contains: We have to do the foolowing

print(data)


# In[33]:


# It contains three groups, one for each station. To search for coincidences between these stations, 
# We first initialize the sapphire.analysis.coincidences.CoincidencesESD class like so:

coincidences = CoincidencesESD(data, '/coincidences', station_groups, 'w')
 


# In[34]:


# From the documentation it is clear that we have to,
# specify the datafile (data), the destination group (/coincidences) and the groups containing the station data (station_groups). 
# Once that’s done, there is an easy way to search for coincidences, 
# process the events making up the coincidences, and store them in the destination group:


coincidences.search_and_store_coincidences(station_numbers=STATIONS)




# In[35]:


# If you want to tweak the process using non-default parameters, 
# see the module documentation (sapphire.analysis.coincidences). 
# For now, let us turn to the results:

print(data)
    


# In[36]:


# The new addition is the /coincidences group. It contains three tables, which are c_index, coincidences and s_index. 
# Information about the coincidences is stored in the coincidences table.

# Here are the columns below



# Column                          # Description

# id                               an index number identifying the coincidence
# timestamp                        the unix timestamp
# nanoseconds                      the nanosecond part of the timestamp
# ext_timestamp                    the timestamp in nanoseconds
# N                                the number of stations taking part in the coincidence
# x                                compatibility reasons
# y                                compatibility reasons
# azimuth                          compatibility reasons
# zenith                           compatibility reasons
# size                             compatibility reasons
# energy                           compatibility reasons
# s501                             flag to indicate if the first station is in coincidence
# s502                             flag to indicate if the second station is in coincidence
# s40001                           flag to indicate if the third station is in coincidence


# The columns included for compatibility reasons are used by the event simulation code. 
# In that case, the x, y columns give the position in cartesian coordinates. 
# Furthermore, the size and energy give the so-called shower size, 
# and zenith and azimuth contain the direction of the (simulated) shower.
# These are not known for certain when working with HiSPARC data, but are included nonetheless. 
# These columns are all set to 0.0.

# The c_index array is used as an index to look up the tables and individual events making up a coincidence. 
# The second coincidence is accessed by:


data.root.coincidences.coincidences[1]




# In[37]:


#Remember, the indexes are zero-based. The coincidence id is also 2:

data.root.coincidences.coincidences[2]['id']


# In[38]:


# The number of stations[2] participating can be obtained by:
data.root.coincidences.coincidences[2]['N']


# In[39]:


# To lookup the indexes of the events taking part in this coincidence, access the c_index array using the same id:
data.root.coincidences.c_index[2]


# In[40]:


# Event id 1 for station 0, event id 1054 is from station 2 and they are part of this coincidence.
# The event obsercables are still stored in their original location and can be accessed using ids.
# The location of the station group can be found using the s_index which conations paths to the station groups.


data.root.coincidences.s_index[0]



data.get_node('/s40001', 'events')[1]




# In[ ]:





# In[41]:


# Downloading coincidences


# Just like events or weather data for a single station the ESD provides coincidence data. 
# This means that you can directly download coincidences from the server. 
# In most cases this can save a lot of disc space, because only events in a coincidence will be stored


# Downloading coincidences is very similar to downloading data. 
# First import the required packages, open a PyTables file, and specify the date/time range.
# With coincidences two additional options are available, first you can select which stations you want to consider.
# This can be all stations in the network, by not specifying any. 
# It can be a subset of stations by listing those stations (upto 30 stations), or a cluster of stations by giving the name of the cluster.



# First, we import the following packages:

import datetime
import tables
from sapphire import esd






# In[42]:


# Setting up the date/time:

start = datetime.datetime(2020, 7, 24)
end = datetime.datetime(2020, 7, 26)



# In[43]:


# We have to open a datafile(but in our case we have to creat one):

data = tables.open_file('data_coincidences.h5', 'a')


# In[44]:


# Then downloading the coincidences. 
# Here we specify the cluster 'Enschede' to select all stations in that cluster.
# We set n to 3, requiring that a coincidence has at least 3 events.

esd.download_coincidences(data, cluster='Enschede', start=start, end=end, n=3)



# In[45]:


# If you now look in the data file it will contain event tables for all stations with at least one event in a coincidence,and 
# a coincidence table for the coincidence data. 
# Just like when coincidences were searched manually:

print(data)


