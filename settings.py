import os, sys, appdirs
from pathlib import Path

from strings import Strings

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

DEFAULT_SETTINGS = """\
photodir={}
tree_expand_all=0
language=english"""

def getDirectory():
    dialog = Gtk.FileChooserDialog(
        title="Choose a folder with your photos",
        parent=None,
        action=Gtk.FileChooserAction.SELECT_FOLDER
    )
    dialog.add_buttons(
        Gtk.STOCK_CANCEL,
        Gtk.ResponseType.CANCEL,
        Gtk.STOCK_OPEN,
        Gtk.ResponseType.OK,
    )

    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        data = dialog.get_filename()
        dialog.destroy()
        return data
    else:
        dialog.destroy()
        return None

def getDirname():
    return os.path.dirname(os.path.abspath(__file__))

def getSettingsDir():
    dirname = appdirs.user_config_dir("Photosorter")
    Path(dirname).mkdir(parents=True, exist_ok=True)
    return dirname

def getSettingsFile():
    return os.path.join(getSettingsDir(), "config.cfg")

def getStringsFile(language):
    return os.path.join(getDirname(), f"lang/{language}.cfg")

class Settings:
    def __init__(self):
        filename = getSettingsFile()

        if not os.path.exists(filename):
            photodir = getDirectory()
            if not photodir:
                sys.exit(1)
            
            with open(filename, "w+") as f:
                f.write(DEFAULT_SETTINGS.format(photodir))
        
        data = ""
        with open(filename, "r") as f:
            data = f.read()
        
        self.settings = {}
        
        for line in data.splitlines():
            if not line or line.startswith("#"):
                continue
            
            key, value = line.split("=", 1)
            self.settings[key] = value
        
        self.strings = Strings(getStringsFile(self["language"] if "language" in self.settings else "english"))
    def __getitem__(self, key):
        return self.settings[key]
    def __setitem__(self, key, value):
        self.settings[key] = value
    def __delitem__(self, key):
        del self.settings[key]
