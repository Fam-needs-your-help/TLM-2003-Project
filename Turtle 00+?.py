import folium
from folium import plugins
import pandas

#ANT PATH
# map
map_plot_route = folium.Map(location=[38, -98], zoom_start=4)
# can use list of lists or list of tuples
route_lats_longs = [[34.041008,-118.246653],
                    [36.169726,-115.143996],
                    [39.739448,-104.992450],
                    [41.878765,-87.643267],
                    [40.782949,-73.969559]]
# add route to map
folium.PolyLine(route_lats_longs).add_to(map_plot_route)
# ant path route
# uses import - from folium import plugins
# map
map_ant_route = folium.Map(location=[38, -98], zoom_start=4)
# add ant path route to map
plugins.AntPath(route_lats_longs).add_to(map_ant_route)
# display map
map_ant_route

#MEASUREMENT TOOL
# map
map_measure = folium.Map([40, -100], zoom_start=4)
# measure control
measure_control = plugins.MeasureControl(position='topleft',
                                         active_color='red',
                                         completed_color='red',
                                         primary_length_unit='miles')
# add measure control to map
map_measure.add_child(measure_control)
# display map
map_measure

#DUAL MAPS
# dual map
map_dual = plugins.DualMap(location=[40, -98], tiles=None, zoom_start=4)
# map tiles
folium.TileLayer('Stamen Terrain').add_to(map_dual)
folium.TileLayer('CartoDB Positron').add_to(map_dual)
# add layer control to maps
folium.LayerControl().add_to(map_dual)
# display map(s)
map_dual

#DRAWING
# map
map_draw = folium.Map(location=[40, -99], zoom_start=4)
# draw tools
draw = plugins.Draw(export=True)
# add draw tools to map
draw.add_to(map_draw)
# display map
map_draw
