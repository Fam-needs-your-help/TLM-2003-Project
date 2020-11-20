import PySimpleGUI as gui
import sys
import pandas
import folium
import webbrowser
import numpy as np
from folium import plugins
from folium.plugins import HeatMap

# layout of first window for filename input
layout1 = [[gui.Text('Enter file name (e.g. include.csv)')],
           [gui.Text('Ensure file is in same directory as program')],
           [gui.InputText('juneroute.csv')],
           [gui.Button('Proceed')]]

# open first window for filename input
window1 = gui.Window('Accident Prone Mapper', layout1)

# check user input in window
while True:
    event, values = window1.read()
    if event == gui.WIN_CLOSED: sys.exit()
    if event == 'Proceed':
        csvName = values[0]
        break

# close the first window
window1.close()

# extract info from csv files
csvFile = pandas.read_csv(csvName)


# INSERT DATA CLEANSING HERE
originalDriver = ["Ali", "Chong", "George", "Gerald", "Keith", "Lim", "Ridwan", "Siva", "Yeo"]
originalVehicle = ["SBS6431D", "SBS8657E", "SG8625P", "SBS7539M", "SBS2235P", "SG1369L",
                   "SG8189H", "SBS1915P", "SBS6289D", "SBS1895G", "SBS6583R"]
df = pandas.read_csv(csvName)               # Reading the excel file using pandas library
df.replace(r'^\s*$', np.nan, regex=True)    # checking for empty cell  and Making it as to a NAN value
df.fillna(0, inplace=True)                  # fill value O at cells that are NAN

for index, row in df.iterrows():                # Iterate through the rows
    if row['Driver'] not in originalDriver:     # Checking if each row of driver matches the list of original drivers
        df.replace(to_replace=row['Driver'], value=0, inplace=True)
        # If the driver name in the cell does not match the original driver list, cell value = 0
    if row['Vehicle'] not in originalVehicle:   # Checking if each row of Vehicle matches the list of original Vehicle
        df.replace(to_replace=row['Vehicle'], value=0, inplace=True) # Same principle

df.drop(df[df['Event'] == 0].index, inplace=True)         # drop the whole row when the event cell is zero
df.drop(df[df['Driver'] == 0].index, inplace=True)        # drop the whole row when the Driver cell is zero
df.drop(df[df['Vehicle'] == 0].index, inplace=True)       # drop the whole row when the Vehicle cell is zero
df.drop(df[df['Latitude'] == 0].index, inplace=True)      # drop the whole row when the Latitude cell is zero
df.drop(df[df['Longitude'] == 0].index, inplace=True)     # drop the whole row when the Longitude cell is zero
df.to_csv("cleanedRouteFile.csv")                         # write a new csv file with cleaned excel data
new_df = pandas.read_csv('cleanedRouteFile.csv')          # read the cleaned file for Data visualization
newCSV = new_df

# strings and sets used to collect unique values for dropdown lists
drivers = ''
allDriver = set()
vehicles = ''
allVehicle = set()
events = ''
allEvent = set()

# scan through csv for unique values and create statements for dropdown lists
for index, row in newCSV.iterrows():
    if row['Driver'] not in allDriver:
        drivers = drivers + str(row['Driver']) + ','
        allDriver.add(row['Driver'])

    if row['Vehicle'] not in allVehicle:
        vehicles = vehicles + str(row['Vehicle']) + ','
        allVehicle.add(row['Vehicle'])

    if row['Event'] not in allEvent:
        events = events + str(row['Event']) + ','
        allEvent.add(row['Event'])

# empty sets to save memory?
allDriver.clear()
allVehicle.clear()
allEvent.clear()

# layout of second window for user selections
layout2 = [[gui.Text('Select options to display on map (ensure driver and vehicle match)')],
          [gui.Text('Driver: '), gui.Combo(drivers.split(","))],
          [gui.Text('Vehicle: '), gui.Combo(vehicles.split(","))],
          [gui.Text('Event: '), gui.Combo(events.split(","))],
          [gui.Text('Map Type: '), gui.Combo(['Markers', 'Heatmap'])],
          [gui.Button('Create Map')]]

# open second window for user selections
window2 = gui.Window('Accident Prone Mapper', layout2)

# check user input in window and create query statement
while True:
    event, values = window2.read()
    if event == gui.WIN_CLOSED:
        sys.exit()
    if event == 'Create Map':
        dvr = "Driver in " + str(values[0].split(","))
        veh = "Vehicle in " + str(values[1].split(","))
        evt = "Event in " + str(values[2].split(","))
        if values[0] == "" and values[1] == "" and values[2] == "":
            selection = None
        if values[0] != "" and values[1] == "" and values[2] == "":
            selection = str(dvr)
        if values[0] == "" and values[1] != "" and values[2] == "":
            selection = str(veh)
        if values[0] == "" and values[1] == "" and values[2] != "":
            selection = str(evt)
        if values[0] != "" and values[1] != "" and values[2] == "":
            selection = str(dvr) + " and " + str(veh)
        if values[0] != "" and values[1] == "" and values[2] != "":
            selection = str(dvr) + " and " + str(evt)
        if values[0] == "" and values[1] != "" and values[2] != "":
            selection = str(veh) + " and " + str(evt)
        if values[0] != "" and values[1] != "" and values[2] != "":
            selection = str(dvr) + " and " + str(veh) + " and " + str(evt)
        mapType = values[3] # Multiple variables joined by 'and' in middle
        break

# close second window
window2.close()

# filter csv based on user selection
if selection is not None:   # if there is a specific query, obey the query, else just spam everything
    newCSV = (newCSV.query(str(selection)))

# create map object and zoom into Singapore
SG_Map = folium.Map(location=[1.36, 103.85], zoom_start=12)

# WIDGETS via folium plugins: minimapEN, minimap, scrollzoom, fullscreen
minimap = plugins.MiniMap(toggle_display=True)
SG_Map.add_child(minimap)
plugins.ScrollZoomToggler().add_to(SG_Map)
plugins.Fullscreen(position='topright').add_to(SG_Map)


# ad csv data as heatmap to MAP
# https://www.kaggle.com/daveianhickey/how-to-folium-for-maps-heatmaps-time-data
if mapType == 'Heatmap':
    heat_data = [[row['Latitude'],row['Longitude']] for index, row in newCSV.iterrows()]
    HeatMap(heat_data).add_to(SG_Map)

# add csv data as markers to MAP
# 19/17/2020: expand window to visualize comment data more clearly
if mapType == 'Markers':
    for index, row in newCSV.iterrows():
        folium.Marker([row['Latitude'], row['Longitude']],
                      popup=row['Driver'] + '\n' + row['Vehicle'] + '\n' + row['Event'] + '\n' + row['Address']).add_to(SG_Map)

else:
    for index, row in newCSV.iterrows():
        folium.Marker([row['Latitude'], row['Longitude']],
                      popup=row['Driver'] + '\n' + row['Vehicle'] + '\n' + row['Event'] + '\n' + row['Address']).add_to(SG_Map)

# generate html file of map
SG_Map.save('SGMap.html')

# open html in browser
webbrowser.open_new('SGMap.html')