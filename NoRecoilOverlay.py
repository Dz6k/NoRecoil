import wx
import keyboard
import mouse
import keyboard, mouse
import win32api
import random
import threading
from time import sleep
import win32con

#################################################################################################################################################
#                                                                                                                                               #
#                                                                                                                                               #
# IF YOU WANT TO USE IT IN YOUR GAME AND ALL THE TIME WHEN YOU ACTIVATE YOUR GAME KEEP MINIMIZING, CHANGE THE GAME RESOLUTION TO WINDOW MODE    #
#                                                                                                                                               #
#                                                                                                                                               #
#################################################################################################################################################


class Mouse:
    RIGHTC = 0x02  # right click
    LEFTC = 0x01  # left click


# Overlay
class OverlayMessageBox(wx.Frame):
    def __init__(self, initial_message, position=(135, 0)):
        style = (wx.CLIP_CHILDREN | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR |
                 wx.NO_BORDER | wx.FRAME_SHAPED)
        wx.Frame.__init__(self, None, size=(90, 18), style=style)

        self.SetBackgroundColour(wx.NullColour)
        self.Show(True)
        self.SetPosition(position)
        self.static_text = wx.StaticText(
            self, label=initial_message, pos=(0, 0))
        font = wx.Font(10, wx.FONTFAMILY_DEFAULT,
                       wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.static_text.SetFont(font)


# No Recoil Class
class NoRecoil(OverlayMessageBox):
    def __init__(self) -> None:
        super().__init__("Loading...")
        self._horizontal_range = 5
        self._enable = False
        self._last_state = False
        self._last_state_left = False
        self._last_state_right = False
        self._last_state_up = False
        self._last_state_down = False
        self._vertical_o = 0
        self._min_vertical = 3
        self._max_vertical = 5
        self._min_firerate = 0.03
        self._max_firerate = 0.04

    @staticmethod
    def is_leftmouse_down():
        lmb_state = win32api.GetKeyState(Mouse.LEFTC)
        return lmb_state < 0

    @staticmethod
    def is_rightmouse_down():
        lmb_state = win32api.GetKeyState(Mouse.RIGHTC)
        return lmb_state < 0

    def start(self):
        # keyboard.on_press(self.update_message)
        self.static_text.SetLabel("Script started")
        thread = threading.Thread(target=self._run)

        thread.daemon = True
        thread.start()

    @staticmethod
    def is_key_up(key_code):
        return win32api.GetAsyncKeyState(key_code) & (1 << 15) != 0

    @staticmethod
    def is_key_down(key_code):
        return win32api.GetAsyncKeyState(key_code) & (1 << 15) == 0

    def _run(self):
        middle_click = False
        while True:
            key_home = keyboard.is_pressed('home')

            if self.is_key_down(win32con.VK_LEFT) and not self._last_state_left:
                if self._vertical_o >= 1:
                    self._vertical_o -= 1
                    self.SetSize(70, 18)
                    self.static_text.SetLabel(f"Force: {self._vertical_o}")

            self._last_state_left = self.is_key_down(win32con.VK_LEFT)

            if self.is_key_down(win32con.VK_RIGHT) and not self._last_state_right:
                if self._vertical_o < 101:
                    self._vertical_o += 1
                    self.SetSize(70, 18)
                    self.static_text.SetLabel(f"Force: {self._vertical_o}")

            self._last_state_right = self.is_key_down(win32con.VK_RIGHT)

            if key_home != self._last_state:
                self._last_state = key_home
                if self._last_state:
                    self._enable = not self._enable
                    if self._enable:
                        self.Show(True)
                    else:
                        self.Show(False)

            # run if press left click and right click together
            if (self.is_leftmouse_down()) and (self.is_rightmouse_down()) and (self._enable):
                _offset_const = 100
                _horizontal_offset = random.randrange(-self._horizontal_range * _offset_const,
                                                      self._horizontal_range * _offset_const, 1) / _offset_const
                _vertical_offset = random.randrange(self._min_vertical * _offset_const,
                                                    self._max_vertical * _offset_const, 1) / _offset_const
                _vertical_offset = self._vertical_o
                win32api.mouse_event(0x0001, int(
                    _horizontal_offset), int(_vertical_offset))
                time_offset = random.randrange(int(self._min_firerate * _offset_const),
                                               int(self._max_firerate * _offset_const), 1) / _offset_const
                if not middle_click:
                    #  USE THIS LINE IF YOU PLAY COD (PING FOR SPOT ENEMYS)
                    mouse.double_click('middle')
                    middle_click = True
                sleep(time_offset)

            else:
                middle_click = False

            sleep(0.001)
    # update overlay

    def update_message(self, event):
        key_pressed = event.name

        if key_pressed in ['left', 'right', 'up', 'down']:

            sleep(0.15)
            self.SetSize(70, 18)
            self.static_text.SetLabel(f"Force: {self._vertical_o}")


if __name__ == '__main__':
    app = wx.App()
    no_recoil = NoRecoil()
    no_recoil.start()
    app.MainLoop()
