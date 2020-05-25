import pandas as pd
import folium

#Use Volcanoes data for first layer.
data = pd.read_csv('Volcanoes.txt')
pd.set_option('display.max_columns',None,'display.max_rows',None,\
              'display.max_colwidth',None)
lat = list(data['LAT'])
lon = list(data['LON'])
values = data.loc[:,['LAT','LON','ELEV','NAME']].values

#This is to style the way popup appears.
html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

def color_func(elev):
    """
    Function returns the color for the marker based upon the values 
    given as argument.
    """
    if elev < 1000:
        return 'green'
    elif 1000 <= elev < 3000:
        return 'orange'
    else:
        return 'red'

map = folium.Map(location=values[0][:2],zoom_start=4,\
                 tiles='Stamen Terrain')

#This msg will be displayed if you hover over the marker.                  
tooltip = "Click!" 

#Feature Group for Volcanoes data.
fgv = folium.FeatureGroup(name="Volcanoes")
for val in values:
    iframe = folium.IFrame(html=html % (val[-1], val[-1], str(val[-2])),\
             width=200, height=70)
    # fg.add_child(folium.Marker(location=val[:2],popup=folium.Popup(iframe),\
                #  icon=folium.Icon(color=color_func(val[-2])),tooltip=tooltip))
    fgv.add_child(folium.CircleMarker(location=val[:2],popup=folium.Popup(iframe),\
                radius=5, fill_color= color_func(val[-2]), color='grey',\
                fill_opacity =0.7,))

#Feature Group for Population data.
fgp = folium.FeatureGroup(name="Population")
fgp.add_child(folium.GeoJson(data=open('world.json','r',\
    encoding='utf-8-sig').read(),style_function=lambda x:{'fillColor':'green'\
            if x['properties']['POP2005']<10000000 else 'orange'\
            if 10000000 <= x['properties']['POP2005']<20000000 else 'red'}))

map.add_child(fgv)
map.add_child(fgp)
#To control the three layers, helps in hiding and visualising one or 
#more at a time.
map.add_child(folium.LayerControl())
map.save('Map.html')