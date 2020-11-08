from settings import Settings
from gui import GUI
from photolib import Image

settings = Settings()
strings = settings.strings
gui = GUI(strings, int(settings["tree_expand_all"]))

image = Image(gui, settings, strings)

gui.set_callback("prev_image",  image.prevImage)
gui.set_callback("next_image",  image.nextImage)
gui.set_callback("del_image",   image.delImage)
gui.set_callback("sort_image",  image.sortImage)
gui.set_callback("sortl_image", image.sortLastImage)
gui.set_callback("rotl_image", image.rotateLeft)
gui.set_callback("rotr_image", image.rotateRight)

gui.set_callback("create_group", image.createGroup)

gui.start()
