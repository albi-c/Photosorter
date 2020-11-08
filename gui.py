import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Keybinder", "3.0")
from gi.repository import Gtk, GdkPixbuf, Keybinder, Gdk

class GUI(Gtk.Window):
    def __init__(self, strings, tree_expand_all=False):
        Gtk.Window.__init__(self, title=strings["name"])

        self.callbacks = {}
        self.tree_expand_all = tree_expand_all
        self.strings = strings

        self.grid = Gtk.Grid()
        self.add(self.grid)

        self.buttonPrev = Gtk.Button(label=self.strings["button.prev_image"])
        self.buttonPrev.connect("clicked", self.run_callback, "prev_image")
        self.grid.attach(self.buttonPrev, 0, 0, 1, 1)

        self.buttonRotL = Gtk.Button(label=self.strings["button.rotl_image"])
        self.buttonRotL.connect("clicked", self.run_callback, "rotl_image")
        self.grid.attach(self.buttonRotL, 1, 0, 1, 1)

        self.buttonDel = Gtk.Button(label=self.strings["button.del_image"])
        self.buttonDel.connect("clicked", self.run_callback, "del_image")
        self.grid.attach(self.buttonDel, 2, 0, 1, 1)

        self.buttonRotR = Gtk.Button(label=self.strings["button.rotr_image"])
        self.buttonRotR.connect("clicked", self.run_callback, "rotr_image")
        self.grid.attach(self.buttonRotR, 3, 0, 1, 1)

        self.buttonNext = Gtk.Button(label=self.strings["button.next_image"])
        self.buttonNext.connect("clicked", self.run_callback, "next_image")
        self.grid.attach(self.buttonNext, 4, 0, 1, 1)

        self.image = Gtk.Image()
        self.grid.attach(self.image, 0, 1, 5, 1)

        self.buttonGroup = Gtk.Button(label=self.strings["button.group_create"])
        self.buttonGroup.connect("clicked", self.run_callback, "create_group")
        self.grid.attach(self.buttonGroup, 4, 4, 1, 1)

        self.buttonSort = Gtk.Button(label=self.strings["button.group_add"])
        self.buttonSort.connect("clicked", self.run_callback, "sortl_image")
        self.grid.attach(self.buttonSort, 4, 5, 1, 1)
        self.set_sortl_button(False)

        self.statusbar = Gtk.Label()
        self.grid.attach(self.statusbar, 0, 2, 5, 1)

        self.progressbar = Gtk.ProgressBar()
        self.grid.attach(self.progressbar, 0, 3, 5, 1)

        # Keybinder.init()
        # Keybinder.bind("Left", self.run_callback, "prev_image")
        # Keybinder.bind("Right", self.run_callback, "next_image")
        # Keybinder.bind("Delete", self.run_callback, "del_image")
        # Keybinder.bind("Enter", self.run_callback, "sortl_image")
        # Keybinder.bind("<Ctrl>n", self.run_callback, "create_group")
        # Keybinder.bind("r", self.run_callback, "rotr_image")
        # Keybinder.bind("e", self.run_callback, "rotl_image")

        self.connect("key-press-event", self.key_press_event)

        self.progressbar_running = False
    def key_press_event(self, widget, event):
        keyval = event.keyval
        keyval_name = Gdk.keyval_name(keyval)
        state = event.state
        
        ctrl = bool(state & Gdk.ModifierType.CONTROL_MASK)

        keybinds = [
            [0, "Left", "prev_image"],
            [0, "Right", "next_image"],
            [0, "Delete", "del_image"],
            [0, "Return", "sortl_image"],
            [1, "n", "create_group"],
            [0, "r", "rotr_image"],
            [0, "e", "rotl_image"]
        ]

        for kb in keybinds:
            if bool(kb[0]) == ctrl and keyval_name == kb[1]:
                self.run_callback(None, kb[2])
    def update(self):
        if self.progressbar_running:
            self.progressbar.pulse()
    def set_progressbar_running(self, running):
        self.progressbar_running = running
        if running:
            self.progressbar.pulse()
        else:
            self.progressbar.set_fraction(0.0)
    def set_progressbar_text(self, text=None):
        self.progressbar.set_text(text)
        self.progressbar.set_show_text(bool(text))
    def start_progressbar_task(self, text):
        self.set_progressbar_running(True)
        self.set_progressbar_text(text)
    def stop_progressbar_task(self):
        self.set_progressbar_running(False)
        self.set_progressbar_text()
    def set_sortl_button(self, state):
        self.buttonSort.set_sensitive(state)
    def row_activated(self, widget, row, col):
        model = widget.get_model()
        text1 = model[row[0]][0]
        text2 = model[row][0]
        self.run_callback(widget, "sort_image", (text1, text2))
    def set_grouptree(self, data):
        self.grouptree = Gtk.TreeStore(str)

        self.treebox = Gtk.VBox(False, 5)
        self.grouptree = Gtk.TreeStore(str)
        for year in data:
            row = self.grouptree.append(None, [year])
            for group in data[year]:
                self.grouptree.append(row, [group])

        self.treeview = Gtk.TreeView(self.grouptree)
        self.tvcolumn = Gtk.TreeViewColumn(self.strings["groups"])
        self.treeview.append_column(self.tvcolumn)
        if self.tree_expand_all: self.treeview.expand_all()
        self.treeview.connect("row-activated", self.row_activated)

        cell = Gtk.CellRendererText()
        self.tvcolumn.pack_start(cell, True)
        self.tvcolumn.add_attribute(cell, 'text', 0)
        self.treebox.add(self.treeview)

        self.grid.attach(self.treebox, 0, 4, 4, 20)
    def update_grouptree(self, data):
        self.grouptree.clear()

        for year in data:
            row = self.grouptree.append(None, [year])
            for group in data[year]:
                self.grouptree.append(row, [group])
        
        if self.tree_expand_all: self.treeview.expand_all()
    def set_statusbar(self, text):
        self.statusbar.set_text(text)
    def set_callback(self, action, func):
        self.callbacks[action] = func
    def run_callback(self, widget, action, params=[]):
        if action in self.callbacks:
            self.callbacks[action](*params)
    def set_image(self, filename):
        if not filename:
            return
        
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=filename,
            width=800,
            height=600,
            preserve_aspect_ratio=True
        )
        self.image.set_from_pixbuf(pixbuf)
    def start(self, destroy_action=Gtk.main_quit):
        self.connect("destroy", destroy_action)
        self.show_all()

        Gtk.main()
    def about_dialog(self, *args, **kwargs):
        dialog = Gtk.AboutDialog()

        authors = ["Albert Csontos"]
        documenters = ["Albert Csontos"]

        dialog.set_program_name(self.strings["name"])
        dialog.set_copyright("Copyright \xa9 2020 Albert Csontos")
        dialog.set_authors(authors)
        dialog.set_documenters(documenters)
        # dialog.set_website("")
        # dialog.set_website_label("")

        dialog.set_title("")

        dialog.show()
