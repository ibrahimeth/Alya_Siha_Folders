import tkinter as tk
from tkinter import ttk
import math

class DrawMeter(tk.Canvas):

    def __init__(self, parent, *args, **kwargs):
        tk.Canvas.__init__(self, parent, *args, **kwargs)
        self.config(bg = "grey")
        if (int(self['height']) * 2 > int(self['width'])):
            boxSide = int(self['width'])
        else:
            boxSide = int(self['height']) * 2
        self.boxX = boxSide / 2
        self.boxY = boxSide / 2
        self.boxRadius = int(0.40 * float(boxSide))
        self.start = 0
        self.end = 1

        self.drawBackground()
        self.drawTicks()
        self.drawNeedle()

    def drawBackground(self):
        bgColour = "black"
        self.create_arc((self.boxX - self.boxRadius,
                         self.boxY - self.boxRadius,
                         self.boxX * 4,
                         self.boxY * 4),
                        fill = bgColour, start = 90)

    def drawTicks(self):
        length = self.boxRadius / 8
        for deg in range(5, 85, 6):
            rad = math.radians(deg)
            self.Tick(rad, length)
        for deg in range(5, 91, 18):
            rad = math.radians(deg)
            self.Tick(rad, length * 2)

    def Tick(self, angle, length):
        cos = math.cos(angle)
        sin = math.sin(angle)
        radius = self.boxRadius * 2
        X = self.boxX * 2
        Y = self.boxY * 2
        self.create_line((X - radius * cos,
                          Y - radius * sin,
                          X - (radius - length) * cos,
                          Y - (radius - length) * sin),
                         fill = "white", width = 2)

    def drawText(self, start = 0, end = 100):
        interval = end / 5
        value = start
        length = self.boxRadius / 2
        for deg in range(5, 91, 18):
            rad = math.radians(deg)
            cos = math.cos(rad)
            sin = math.sin(rad)
            radius = self.boxRadius * 2
            self.create_text(self.boxX * 2 - (radius - length - 1) * cos,
                             self.boxY * 2 - (radius - length - 1) * sin,
                             text = str("{0:.1f}".format(value)),
                             fill = "white",
                             font = ("Arial", 12, "bold"))
            value = value + interval

    def setRange(self, start, end):
        self.start = start
        self.end = end
        self.drawText(start, end)

    def drawNeedle(self):
        X = self.boxX * 2
        Y = self.boxY * 2
        length = self.boxRadius - (self.boxRadius / 4)
        self.meterHand = self.create_line(X / 2, Y / 2, X + length, Y + length,
                                          fill = "red", width = 4)
        self.create_arc(X - 30, Y - 30, X + 30, Y + 30,
                        fill = "#c0c0c0", outline = "#c0c0c0", start = 90)

    def updateNeedle(self, value):
        length = self.boxRadius - (self.boxRadius / 4)
        deg = 80 * (value - self.start) / self.end - 180
        rad = math.radians(deg)
        self.coords(self.meterHand, self.boxX * 2, self.boxY * 2,
                    self.boxX + length * math.cos(rad),
                    self.boxY + length * math.sin(rad))

value = 0

def update_frame():
    global value
    if value < 1:
        value = value + 0.01
    print(value)
    meter.updateNeedle(value)
    container.after(200, update_frame)

root = tk.Tk()
container = tk.Frame(root)
container.pack()
meter = DrawMeter(container, height = 200, width = 200, bg = "red")
meter.setRange(0, 90)
meter.pack()
update_frame()
root.mainloop()