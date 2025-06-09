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

root = Tk()
root.title("System śledzenia incydentów - Ukraina")
root.geometry("1100x700")
root.configure(bg="#C0D9D9")

map_widget = tkintermapview.TkinterMapView(root, width=900, height=400)
map_widget.set_position(48.3794, 31.1656)
map_widget.set_zoom(6)
map_widget.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

main_frame = Frame(root)
main_frame = Frame(root, bg="#C0D9D9")
main_frame.grid(row=1, column=0, columnspan=4, sticky=W, padx=10)

Label(main_frame, text="Tytuł").grid(row=0, column=0, sticky=W)
entry_title = Entry(main_frame, width=30)
entry_title.grid(row=0, column=1, sticky=W)

Label(main_frame, text="Lokalizacja").grid(row=1, column=0, sticky=W)
entry_location = Entry(main_frame, width=30)
entry_location.grid(row=1, column=1, sticky=W)

Label(main_frame, text="Data (YYYY-MM-DD)").grid(row=2, column=0, sticky=W)
entry_date = Entry(main_frame, width=30)
entry_date.grid(row=2, column=1, sticky=W)

Label(main_frame, text="Typ incydentu").grid(row=3, column=0, sticky=W)
combo_type = ttk.Combobox(main_frame, values=["Ostrzał", "Atak dronów", "Pomoc", "Zniszczenie", "Ofiary"])
combo_type.grid(row=3, column=1, sticky=W)
combo_type.current(0)

Label(main_frame, text="Opis").grid(row=4, column=0, sticky=NW)
text_desc = Text(main_frame, width=30, height=4)
text_desc.grid(row=4, column=1, sticky=W)

Button(main_frame, text="Dodaj incydent", command=add_incident).grid(row=5, column=1, pady=5)

listbox = Listbox(main_frame, width=50)
listbox.grid(row=0, column=2, rowspan=5, padx=10)
Button(main_frame, text="Pokaż szczegóły", command=show_details).grid(row=5, column=2)
Button(main_frame, text="Usuń", command=delete_incident).grid(row=5, column=3)

Label(main_frame, text="Filtruj wg typu").grid(row=6, column=0, sticky=W)
combo_filter_type = ttk.Combobox(main_frame, values=["Ostrzał", "Atak dronów", "Pomoc", "Zniszczenie", "Ofiary"])
combo_filter_type.grid(row=6, column=1, sticky=W)
combo_filter_type.current(0)
Button(main_frame, text="Filtruj", command=filter_by_type).grid(row=6, column=2)

Label(main_frame, text="Filtruj wg daty (YYYY-MM-DD)").grid(row=7, column=0, sticky=W)
entry_filter_date = Entry(main_frame, width=15)
entry_filter_date.grid(row=7, column=1, sticky=W)
Button(main_frame, text="Filtruj", command=filter_by_date).grid(row=7, column=2)

details_frame = Frame(root)
details_frame.grid_remove()
label_info = Label(details_frame, text="", justify=LEFT)
label_info.grid(row=0, column=0, sticky=W)
Button(details_frame, text="Powrót", command=return_to_main).grid(row=1, column=0, pady=5)

root.mainloop()
