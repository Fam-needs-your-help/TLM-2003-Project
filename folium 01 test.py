import folium
from folium import plugins
import pandas
import tkinter
# CSV for <1K rows, specialized for parsing datasets
from datetime import datetime

def sentenceGenerator():      #lo-fi method
      inputA1 = input("Would you like to find a specific Driver? (YES/NO): ")
      if inputA1 == "YES":
            inputA2 = input("Please enter their names separately. (e.g. Nigel Ridzuan Ali etc..)")
      else:
            inputA2 = None
      inputB1 = input("Would you like to find a specific Vehicle? (YES/NO): ")
      if inputB1 == "YES":
            inputB2 = input("Please enter the vehicle numbers separately. (e.g. SBS6289D SBS6009W SBS1234Q etc...)")
      else:
            inputB2 = None
      inputC1 = input("Would you like to find a specific Event? (YES/NO): ")
      if inputC1 == "YES":
            inputC2 = input("Please enter the specific event. (e.g. Sudden brake in turn)")
      else:
            inputC2 = None
      # query generator
      if inputA2 != None:
            inputA2 = str(inputA2.split())
            inputA2 = "Driver in " + inputA2
      if inputB2 != None:
            inputB2 = str(inputB2.split())
            inputB2 = "Vehicle in " + inputB2
      if inputC2 != None:
            inputC2 = str(inputC2.split())
            inputC2 = "Event in " + inputC2
      # sentence generator
      if inputA2 != None and inputB2 != None and inputC2 != None:
            sentence = inputA2 + " and " + inputB2 + " and " + inputC2
      elif inputA2 != None and inputB2 != None:sentence = inputA2 + " and " + inputB2
      elif inputA2 != None and inputC2 != None:sentence = inputA2 + " and " + inputC2
      elif inputB2 != None and inputC2 != None:sentence = inputB2 + " and " + inputC2
      elif inputA2 != None:sentence = inputA2
      elif inputB2 != None:sentence = inputB2
      elif inputC2 != None:sentence = inputC2
      else: sentence = "Speed > 0"
      return sentence

def eventIndicator(input):
    if input == 'Braking': output = str('glyphicon-bold')
    elif input == 'Acceleration': output = str('glyphicon-font')
    elif input == 'Lane Change': output = str('glyphicon-random')
    elif input == 'Turning': output = str('glyphicon-share-alt')
    else: output = str('glyphicon-flag')
    return output

# insert code here to extract info from .csv files
#   https://www.youtube.com/watch?v=Xi52tx6phRU
#   https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
csvFile = pandas.read_csv('juneroute.csv')

# create map object and save stats
SG_Map = folium.Map(location=[1.38, 103.8], zoom_start=12)

# aesthe-THICC
folium.raster_layers.TileLayer('Open Street Map').add_to(SG_Map)
folium.raster_layers.TileLayer('Stamen Terrain').add_to(SG_Map)
folium.raster_layers.TileLayer('Stamen Toner').add_to(SG_Map)
folium.LayerControl().add_to(SG_Map)

# WIDGETS via folium plugins: minimapEN, minimap, scrollzoom, fullscreen
minimap = plugins.MiniMap(toggle_display=True)
SG_Map.add_child(minimap)
plugins.ScrollZoomToggler().add_to(SG_Map)
plugins.Fullscreen(position='topright').add_to(SG_Map)

# filter function w/test values
csvFile = (csvFile.query(sentenceGenerator()))

# adding markers to MAP
for index, row in csvFile.iterrows():
    folium.Marker([row['Latitude'], row['Longitude']],
                  popup=row['Driver'] + ' ' + row['Address'] + ' '+ row['Vehicle'] + ' ' + row['Event'],
                  icon=folium.Icon(icon=eventIndicator(row['Event']), prefix='glyphicon')).add_to(SG_Map)

# generate html file with map
SG_Map.save('SGMap.html')
webbrowser.open_new('SGMap.html')
