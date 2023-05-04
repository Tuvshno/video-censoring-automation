from control import Control

keys = {
    "00:00:01:26":"00:00:04:17",
    "00:00:05:20":"00:00:05:35",
    "00:00:07:17":"00:00:07:35"
}

control = Control(keys)
control.cut_all()