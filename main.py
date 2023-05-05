from control import Control
from captions import Captions

caption = Captions("captions.txt")

control = Control(caption.getKeys())
control.cut_all()