import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, Keybinder

import re

def is_year(text):
    return re.match(r"^\d{4}$", text)

def create_group(parent, strings):
    dialog = Gtk.MessageDialog(parent,
                               Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                               Gtk.MessageType.QUESTION,
                               Gtk.ButtonsType.OK_CANCEL,
                               strings["groups.create_new"])
    
    # dialog.set_title("Create new group")

    dialogBox = dialog.get_content_area()

    yearLabel = Gtk.Label(label=strings["groups.create_new.year"])
    dialogBox.pack_start(yearLabel, False, False, 0)

    yearEntry = Gtk.Entry()
    yearEntry.set_size_request(100, 0)

    dialogBox.pack_start(yearEntry, False, False, 0)

    nameLabel = Gtk.Label(label=strings["groups.create_new.name"])
    dialogBox.pack_start(nameLabel, False, False, 0)

    nameEntry = Gtk.Entry()
    nameEntry.set_size_request(250, 0)

    dialogBox.pack_start(nameEntry, False, False, 0)

    dialog.show_all()
    response = dialog.run()
    year = yearEntry.get_text()
    name = nameEntry.get_text()
    dialog.destroy()
    if (response == Gtk.ResponseType.OK):
        if year and name and is_year(year):
            return [True, year, name]
        return [False, year, name]
    return [None, None, None]

def select_language(parent):
    pass
