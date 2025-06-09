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

    entry_title.delete(0, END)
    entry_location.delete(0, END)
    entry_date.delete(0, END)
    text_desc.delete("1.0", END)


def refresh_list():
    listbox.delete(0, END)
    for idx, i in enumerate(incidents):
        listbox.insert(idx, f"{i.date} - {i.title} ({i.incident_type})")


def show_details():
    idx = listbox.curselection()
    if not idx:
        return
    inc = incidents[idx[0]]
    details_frame.grid(row=7, column=0, columnspan=4, sticky=W, padx=10, pady=5)
    label_info.config(text=f"{inc.title}\n{inc.location}\n{inc.date}\n{inc.incident_type}\n{inc.description}")
    map_widget.set_position(inc.coordinates[0], inc.coordinates[1])
    map_widget.set_zoom(8)
    main_frame.grid_remove()

def return_to_main():
    details_frame.grid_remove()
    main_frame.grid(row=1, column=0, columnspan=4, sticky=W, padx=10)

def delete_incident():
    idx = listbox.curselection()
    if not idx:
        return
    incidents[idx[0]].marker.delete()
    del incidents[idx[0]]
    refresh_list()
    label_info.config(text="")
    return_to_main()

def filter_by_type():
    t = combo_filter_type.get()
    filtered = [i for i in incidents if i.incident_type == t]
    draw_markers(filtered)


def filter_by_date():
    d = entry_filter_date.get()
    filtered = [i for i in incidents if i.date == d]
    draw_markers(filtered)


def draw_markers(filtered_list):
    map_widget.delete_all_marker()
    for i in filtered_list:
        i.marker = map_widget.set_marker(i.coordinates[0], i.coordinates[1], text=i.title)


