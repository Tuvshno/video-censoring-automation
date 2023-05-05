from control import Control
from captions import Captions

caption = Captions("test6.txt")

if not caption.getKeys():
    print("No Profanity Found")
    quit()

control = Control(caption.getKeys())
control.cut_all()