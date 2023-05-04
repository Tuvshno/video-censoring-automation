import numpy as np
import win32gui, win32ui, win32con

class WindowCapture:
  w = 1920 
  h = 1080
  hwnd = None
  cropped_x = 0
  cropped_y = 0
  offset_x = 0
  offset_y = 0

  def __init__(self, window_name):
     
     self.hwnd = win32gui.FindWindow(None, window_name)
     if not self.hwnd:
        raise Exception('Window not found {}'.format(window_name))
     
     #get window size
     window_rect = win32gui.GetWindowRect(self.hwnd)
     self.w = window_rect[2] - window_rect[0]
     self.h = window_rect[3] - window_rect[1]

     #account for border
     border_pixels = 8
     titlebar_pixels = 30
     self.w = self.w - (border_pixels * 2)
     self.h = self.h - titlebar_pixels - border_pixels
     self.cropped_x = border_pixels
     self.cropped_y = titlebar_pixels

     #set coordinate offset for translation actual screen positions
     self.offset_x = window_rect[0] + self.cropped_x
     self.offset_y = window_rect[1] + self.cropped_y

  def get_screenshot(self):

    bmpfilenamename = "out.bmp" #set this

    #hwnd = None


    # get window img data
    wDC = win32gui.GetWindowDC(self.hwnd)
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(self.w, self.h) , dcObj, (self.cropped_x,self.cropped_y), win32con.SRCCOPY)

    #save data
    #dataBitMap.SaveBitmapFile(cDC, bmpfilenamename)
    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (self.h, self.w, 4)

    # Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(self.hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    #remove alpha channel
    img = img[...,:3]
    #make image contiguous to avoid errors that look alike
    img = np.ascontiguousarray(img)

 
    return img

  def list_window_names(self):
    def winEnumHandler( hwnd, ctx ):
        if win32gui.IsWindowVisible( hwnd ):
            print ( hex( hwnd ), win32gui.GetWindowText( hwnd ) )


#translate pixel position on a screenshot image to pixel position on screen
  def get_screen_position(self, pos):
      return (pos[0] + self.offset_x, pos[1] + self.cropped_y)

  #win32gui.EnumWindows( winEnumHandler, None )