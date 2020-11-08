import os, exif, re, datetime, shutil, time, sys
from pathlib import Path
from send2trash import send2trash
from PIL import Image as PILImage

from dialogs import create_group

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GLib

def getDirname():
    return os.path.dirname(os.path.abspath(__file__))

def listFiles(path):
    files = sorted(Path(path).rglob("*"))
    return [f for f in files if any([str(f).endswith(ext) for ext in "png jpg jpeg gif bmp ico tiff".split(" ")])]

def listDirs(path, exclude=[]):
    return sorted([x for x in os.listdir(path) if (x not in exclude) and os.path.isdir(os.path.join(path, x))])

def isYear(text):
    return re.match(r"^\d{4}$", text)

def rotateImage(filename, angle):
    im = PILImage.open(filename)

    with open(filename, "rb") as f:
        img = exif.Image(f)
    if img.has_exif:
        date = img.datetime
    else:
        date = None
    
    im = im.rotate(angle, expand=True)

    im.save(filename)

    with open(filename, "rb") as f:
        img = exif.Image(f)
    if date != None: img.set("datetime", date)
    with open(filename, "wb") as f:
        f.write(img.get_file())

class Image:
    def __init__(self, gui, settings, strings):
        self.gui = gui
        self.settings = settings
        self.strings = strings
        self.dirname = settings["photodir"]
        self.newdir = os.path.join(self.dirname, "new")

        self.imageArray = listFiles(self.newdir)
        self.imageIndex = 0

        self.updateImage()

        years = listDirs(self.dirname, ["new"])
        self.grouptree = {}

        for year in years:
            self.grouptree[year] = listDirs(os.path.join(self.dirname, year))

        self.gui.set_grouptree(self.grouptree)

        self.lgroup_init = False

        self.timeout_id = GLib.timeout_add(50, self.update, None)
    def update(self, *args):
        self.gui.update()
    def rotateLeft(self):
        self.rotateImage(90)
    def rotateRight(self):
        self.rotateImage(270)
    def rotateImage(self, angle):
        try:
            rotateImage(self.imageArray[self.imageIndex], angle)
        except IndexError:
            pass

        self.updateImage()
    def prevImage(self):
        if self.imageIndex > 0:
            self.imageIndex -= 1
            self.updateImage()
    def nextImage(self):
        if self.imageIndex < len(self.imageArray) - 1:
            self.imageIndex += 1
            self.updateImage()
    def delImage(self):
        try:
            send2trash(str(self.imageArray[self.imageIndex]))
            self.removeImageArrayItem(self.imageArray[self.imageIndex])
        except IndexError:
            pass
        
        self.updateImage()
    def sortImage(self, group1, group2):
        if isYear(group2):
            return
        
        self.lgroupInit(group1, group2)

        try:
            self.moveImage(self.imageArray[self.imageIndex], os.path.join(self.dirname, group1, group2))
        except IndexError:
            self.updateImage()
    def sortLastImage(self):
        if not self.lgroup_init:
            return
        
        self.sortImage(self.lgroup[0], self.lgroup[1])
    def lgroupInit(self, g1, g2):
        self.lgroup = [g1, g2]
        self.lgroup_init = True
        self.gui.set_sortl_button(True)
    def createGroup(self):
        data = create_group(self.gui, self.strings)
        if data[0] == None:
            return
        elif data[0] == False:
            createGroup(self)
        elif data[0] == True:
            year = data[1]
            name = data[2]
            Path(os.path.join(self.dirname, year, name)).mkdir(parents=True, exist_ok=True)

            if year in self.grouptree and name not in self.grouptree[year]:
                self.grouptree[year].append(name)
            elif name in self.grouptree[year]:
                pass
            else:
                self.grouptree[year] = [name]
            
            self.gui.update_grouptree(self.grouptree)
    def removeImageArrayItem(self, filename):
        filename = os.path.abspath(filename)

        i = 0
        for f in self.imageArray:
            fn = os.path.abspath(str(f))

            if fn == filename:
                self.imageArray.pop(i)
                if self.imageIndex >= len(self.imageArray):
                    self.imageIndex -= 1
                self.updateImage()
                break
            
            i += 1
    def moveImage(self, src, dst):
        src = os.path.abspath(src)

        self.removeImageArrayItem(src)

        shutil.move(src, dst)
    def updateImage(self):
        filename = None
        try:
            filename = str(self.imageArray[self.imageIndex])
            self.gui.set_image(filename)
        except IndexError:
            self.gui.set_image(os.path.join(getDirname(), "res", "placeholder.png"))

        self.updateStatusbar(filename)
    def updateStatusbar(self, filename=None):
        sbtext = ""
        if filename:
            with open(filename, "rb") as f:
                img = exif.Image(f)
            if img.has_exif:
                date = datetime.datetime.strptime(img.datetime, "%Y:%m:%d %H:%M:%S")
                date_string = date.strftime(self.strings["dateformat"])
                sbtext += f"{date_string}        "
        sbtext += f"{self.imageIndex + 1}/{len(self.imageArray)}"
        self.gui.set_statusbar(sbtext)
