from tkinter import *
from tkinter import ttk
import tkintermapview
import requests
from bs4 import BeautifulSoup
from datetime import datetime


incidents = []


class Incident:
    def __init__(self, title, location, date, incident_type, description):
        self.title = title
        self.location = location
        self.date = date
        self.incident_type = incident_type
        self.description = description
        self.coordinates = self.get_coordinates()
        self.marker = None

    def get_coordinates(self):
        try:
            url = f"https://pl.wikipedia.org/wiki/{self.location}"
            response = requests.get(url).text
            soup = BeautifulSoup(response, "html.parser")
            lat = float(soup.select(".latitude")[1].text.replace(",", "."))
            lon = float(soup.select(".longitude")[1].text.replace(",", "."))
            return [lat, lon]
        except:
            return [48.3794, 31.1656]

def add_incident():
    title = entry_title.get()
    location = entry_location.get()
    date = entry_date.get()
    incident_type = combo_type.get()
    description = text_desc.get("1.0", END).strip()

    if not title or not location or not date or not incident_type:
        return

    inc = Incident(title, location, date, incident_type, description)
    inc.marker = map_widget.set_marker(inc.coordinates[0], inc.coordinates[1], text=title)
    incidents.append(inc)
    refresh_list()

