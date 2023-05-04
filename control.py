import pyautogui
import time
# pyautogui.moveTo(100,100, duration=0)
# pyautogui.dragRel(0,50,duration=1)

#00:00:01:26
#00:00:04:17

class Control():
    
    keys = {}

    def __init__(self, keys):
        self.keys = keys
    
    def cut_all(self):
       for key, value in self.keys.items():
          self.__cut_section(key, value)
          time.sleep(0.5)


    def __cut_section(self, beg, end):
       self.__cut(beg)
       time.sleep(0.5)
       self.__cut(end)
       self.__delete()

    def __cut(self, time):
      pyautogui.click(350,550, duration=0)
      pyautogui.typewrite(time)
      pyautogui.typewrite(["enter"])
      pyautogui.hotkey("ctrlleft", "k")

    def __delete(self):
      pyautogui.press('left')
      pyautogui.press('delete')

    def check(self):
      beg = list(self.keys.keys())[0]
      end = self.keys[beg]
      self.cut_section(beg, end)
