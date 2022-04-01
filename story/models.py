from django.db import models

# Create your models here.
import folium
import json
# from pynput import mouse
from shapely.geometry import shape, Point
from bs4 import BeautifulSoup
from folium.plugins import LocateControl, MarkerCluster
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
# from pymouse import PyMouse
# from pynput.mouse import Listener, Button, Controller


# def is_clicked(x, y, button, pressed):
 #   if pressed:
 #       print('Clicked!')
 #       text = models.TextField()
 #       image_url = models.TextField()
  #      return False


class StoryCluster():
    pass

class Node(models.Model):
    def __init__(self, title, thumbnail, text, image ):
        self.nodeMade = []
        self.title = title
        self.thumbnail = thumbnail
        self.text = text
        self.image = image

    def graph(self):
        nxG = nx.Graph()
        # single node
        nxG.add_node(2)
        nx.draw(nxG)
        demoStory = [1,2,3,4,5]
        nxG.add_nodes_from(demoStory)
        plt.savefig("visual.png")
        plt.savefig('MyMap.html')
        contains = {"Title": "user input","Text": "user input"}
        nx.set_node_attributes(nxG, contains)
     #   nxG.nodes[0]["Title"]


class NodeStory(folium.Map):

    # Create the map
    MyMap = folium.Map(location=[39.2760, -76.6471], tiles='OpenStreetMap', zoom_start=10, max_zoom=19,
                       control_scale=True)

    # Save the map
    MyMap.save('MyMap.html')

    # Create custom story icon for map markers
    # story_img = 'story.png'

    # Create marker cluster to help define cluster of stories. Cluster will separate into individual markers at zoom level 13.
   # story_cluster = MarkerCluster(options={'showCoverageOnHover': False,
                                           # 'zoomToBoundsOnClick': True,
                                           # 'spiderfyOnMaxZoom': False,
                                           # 'disableClusteringAtZoom': 13})

    # lat and lon should be given when the user clicks on the map
   # story_made = {'Story Name 1': [(39.2263, -75.9848), 'instagram_post_URL', 'pub_website_URL', 'google_maps_directions_URL'],
   #               'Story Name 2': [(39.4371, -77.3835), 'instagram_post_URL', 'pub_website_URL', 'google_maps_directions_URL'],
   #               'Story Name 3': ...}

    # Create markers for each pub in the pub dictionary
  # for node, details in story_made.items():
        # Define marker variables
   #     name = node
   #     coordinates = details[0] where the user clicks
   ###     thumbnail = details[1] options on thumbnail
   ###     text = details[2] input a text
   ###     image = details[3] or image

        # Create custom icon with story image
   # custom_icon = folium.CustomIcon(story_img, icon_size=(35, 35), popup_anchor=(0, -22))
        # Define html inside marker pop-up

    ##    click_html = folium.Html(
    ##        f"""<p style="text-align: center;"><span style="font-family: Didot, serif; font-size: 21px;">{name}</span></p>
    ##    <p style="text-align: center;"><iframe src={thumbnail}embed width="240" height="290" frameborder="0" scrolling="auto" allowtransparency="true"></iframe>
    ##    <p style="text-align: center;"><a href={text} target="_blank" title="{name} Text media"><span style="font-family: Didot, serif; font-size: 17px;">{name} Website</span></a></p>
    ##    <p style="text-align: center;"><a href={image} target="_blank" title="Image media {name}"><span style="font-family: Didot, serif; font-size: 17px;">Directions to {name}</span></a></p>
    ##    """, script=True)
        # Create pop-up with html content
    # if user clicks on map story prompt pops up
    #popup = folium.Popup(click_html, max_width=700)
        # Create marker with custom icon and pop-up.
   # custom_marker = folium.Marker(location=[39.2263, -75.9848], icon=custom_icon, tooltip='story')#, popup=popup)

        # If story is within Vicinity, add to Area marker cluster
    #    if area_boundary.contains(Point((coordinates[1], coordinates[0]))):
   # custom_marker.add_to(story_cluster)
    #    else:
            # Else add marker to map
   # custom_marker.add_to(MyMap)
   # MyMap.save('MyMap.html')
    # Add story cluster to the map
   #story_cluster.add_to(MyMap)

    # Enable geolocation button on map.
   # LocateControl(auto_start=False).add_to(MyMap)

    # Define webpage title html and add to script.
   # tab_title = """<title>Tell me a Story</title>"""
   # MyMap.get_root().html.add_child(folium.Element(tab_title))

    # Save map to HTML
   #MyMap.save('MyMap.html')
