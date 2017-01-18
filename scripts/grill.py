#!/usr/bin/python

"""
    Grill.py G-Code Generator
    Version 1.0
    Copyright (C) <2008>  <Lawrence Glaister> <ve7it at shaw dot ca>
    based on work by <John Thornton>  -- thanks John!

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    To make it a menu item in Ubuntu use the Alacarte Menu Editor and add
    the command python YourPathToThisFile/grill.py
    make sure you have made the file executable by right
    clicking and selecting properties then Permissions and Execute

    To use with EMC2 see the instructions at:
    http://wiki.linuxcnc.org/cgi-bin/emcinfo.pl?Simple_EMC_G-Code_Generators

"""

from Tkinter import *
from math import *
import os


IN_AXIS = os.environ.has_key("AXIS_PROGRESS_BAR")

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        self.DoIt()


    def createWidgets(self):
        self.HoleID = []
        self.gcode = []
        self.PreviewFrame = Frame(self,bd=5)
        self.PreviewFrame.grid(row=0, column=0)
        self.PreviewCanvas = Canvas(self.PreviewFrame,width=300, height=300, bg='white', bd='3', relief = 'raised')
        self.PreviewCanvas.grid(sticky=N+S+E+W)
        self.XLine = self.PreviewCanvas.create_line(15,150,285,150, fill = 'green')
        self.YLine = self.PreviewCanvas.create_line(150,15,150,285, fill = 'green')

        self.EntryFrame = Frame(self,bd=5)
        self.EntryFrame.grid(row=0, column=1)

        self.st00 = Label(self.EntryFrame, text='Peck Drill a Speaker Grill Pattern\n')
        self.st00.grid(row=0, column=0, columnspan=2)

        self.st01 = Label(self.EntryFrame, text='Preamble')
        self.st01.grid(row=2, column=0)
        self.PreambleVar = StringVar()
        self.PreambleVar.set('G17 G20 G90 G64 P0.003 M3 S3000 M7')
        self.Preamble = Entry(self.EntryFrame, textvariable=self.PreambleVar ,width=35)
        self.Preamble.grid(row=2, column=1)

        self.st02 = Label(self.EntryFrame, text='X Center of Grill')
        self.st02.grid(row=3, column=0)
        self.XGrillCenterVar = StringVar()
        self.XGrillCenterVar.set('3.0')
        self.XGrillCenter = Entry(self.EntryFrame, textvariable=self.XGrillCenterVar ,width=15)
        self.XGrillCenter.grid(row=3, column=1)

        self.st03 = Label(self.EntryFrame, text='Y Center of Grill')
        self.st03.grid(row=4, column=0)
        self.YGrillCenterVar = StringVar()
        self.YGrillCenterVar.set('4.0')
        self.YGrillCenter = Entry(self.EntryFrame, textvariable=self.YGrillCenterVar ,width=15)
        self.YGrillCenter.grid(row=4, column=1)

        self.st04 = Label(self.EntryFrame, text='Diameter of Grill')
        self.st04.grid(row=5, column=0)
        self.GrillDiameterVar = StringVar()
        self.GrillDiameterVar.set('3.0')
        self.GrillDiameter = Entry(self.EntryFrame, textvariable=self.GrillDiameterVar ,width=15)
        self.GrillDiameter.grid(row=5, column=1)

        self.st05 = Label(self.EntryFrame, text='Hole Spacing')
        self.st05.grid(row=6, column=0)
        self.HoleSpaceVar = StringVar()
        self.HoleSpaceVar.set('0.3')
        self.HoleSpace = Entry(self.EntryFrame, textvariable=self.HoleSpaceVar ,width=15)
        self.HoleSpace.grid(row=6, column=1)

        self.st06 = Label(self.EntryFrame, text='Final Hole Depth')
        self.st06.grid(row=7, column=0)
        self.HoleDepthVar = StringVar()
        self.HoleDepthVar.set('-0.25')
        self.HoleDepth = Entry(self.EntryFrame, textvariable=self.HoleDepthVar ,width=15)
        self.HoleDepth.grid(row=7, column=1)

        self.st07 = Label(self.EntryFrame, text='Q - peck incr')
        self.st07.grid(row=8, column=0)
        self.PeckVar = StringVar()
        self.PeckVar.set('0.1')
        self.Peck = Entry(self.EntryFrame, width=15, textvariable = self.PeckVar)
        self.Peck.grid(row=8, column=1)

        self.st08 = Label(self.EntryFrame, text='R - Safe Z')
        self.st08.grid(row=9, column=0)
        self.SafeZVar = StringVar()
        self.SafeZVar.set('0.05')
        self.SafeZ = Entry(self.EntryFrame, width=15, textvariable = self.SafeZVar)
        self.SafeZ.grid(row=9, column=1)

        self.st09 = Label(self.EntryFrame, text='Feedspeed')
        self.st09.grid(row=10, column=0)
        self.FeedspeedVar = StringVar()
        self.FeedspeedVar.set('5.0')
        self.Feedspeed = Entry(self.EntryFrame, textvariable=self.FeedspeedVar ,width=15)
        self.Feedspeed.grid(row=10, column=1)

        self.st10 = Label(self.EntryFrame, text='Drill Size')
        self.st10.grid(row=11, column=0)
        self.DrillVar = StringVar()
        self.DrillVar.set('0.1875')
        self.Drill = Entry(self.EntryFrame, textvariable=self.DrillVar ,width=15)
        self.Drill.grid(row=11, column=1)

        self.st11 = Label(self.EntryFrame, text='Postamble')
        self.st11.grid(row=12, column=0)
        self.PostambleVar = StringVar()
        self.PostambleVar.set('M5 M9 M2')
        self.Postamble = Entry(self.EntryFrame, textvariable=self.PostambleVar ,width=15)
        self.Postamble.grid(row=12, column=1)

        self.DoItButton = Button(self.EntryFrame, text='Recalculate', command=self.DoIt)
        self.DoItButton.grid(row=13, column=0)

        self.ToClipboard = Button(self.EntryFrame, text='To Clipboard', command=self.CopyClipboard)
        self.ToClipboard.grid(row=13, column=1)

        if IN_AXIS:
            self.quitButton = Button(self, text='Write to AXIS and Quit',command=self.WriteToAxis)
        else:
            self.quitButton = Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(row=13, column=0, sticky=S)

    def DoIt(self):
        # rough guess at number of holes each direction from centerpoint
        holes = int(((float(self.GrillDiameterVar.get())/float(self.HoleSpaceVar.get()))+3.0)/2.0)

        # erase old holes/display objects as needed
        for hole in self.HoleID:
            self.PreviewCanvas.delete(hole)
        self.HoleID = []

        # erase old gcode as needed
        self.gcode = []
        self.gcode.append('( Code generated by grill.py widget )')
        self.gcode.append('( by Lawrence Glaister VE7IT - 2008 )')
        self.gcode.append(self.PreambleVar.get())
        self.gcode.append( 'G0 Z%.4f F%s' %(float(self.SafeZVar.get()), self.FeedspeedVar.get()))

        RadSQ = float(self.GrillDiameterVar.get()) / 2.0
        RadSQ *= RadSQ;
        Scale = float(self.GrillDiameterVar.get()) * 1.2 / 300.0
        DrillRad = float(self.DrillVar.get()) / 2.0
        GrillRadius = float(self.GrillDiameterVar.get())/2.0
        Spacing = float(self.HoleSpaceVar.get())

        # circular guide
        self.HoleID.append(self.PreviewCanvas.create_oval(
            150-GrillRadius/Scale,
            150-GrillRadius/Scale,
            150+GrillRadius/Scale,
            150+GrillRadius/Scale, outline='green'))

        first = 1;
        numholes = 0;
        for x in range(-holes,holes):
            for y in range(-holes,holes):
                CurY = y * Spacing
                CurX = x * Spacing

                # the selection criterion for holes is that the center has to be inside
                # the requested grill diameter
                if (( CurY * CurY + CurX * CurX ) < RadSQ):
                    numholes += 1
                    self.HoleID.append( self.PreviewCanvas.create_oval(
                        150+(CurX-DrillRad)/Scale,
                        150+(CurY-DrillRad)/Scale,
                        150+(CurX+DrillRad)/Scale,
                        150+(CurY+DrillRad)/Scale, fill='grey'))

                    # generate the G code
                    if first:
                        self.gcode.append( 'G83 X%.4f Y%.4f Z%.4f Q%.4f R%.4f'
                            %( CurX + float(self.XGrillCenterVar.get()),
                            CurY + float(self.YGrillCenterVar.get()),
                            float(self.HoleDepthVar.get()),
                            float(self.PeckVar.get()),
                            float(self.SafeZVar.get())))
                        first = 0
                    else:
                        self.gcode.append( 'G83 X%.4f Y%.4f'
                            %( CurX + float(self.XGrillCenterVar.get()),
                               CurY + float(self.YGrillCenterVar.get())))

        self.HoleID.append(self.PreviewCanvas.create_text(150, 295, text='%d holes'%(numholes)))
        self.gcode.append(self.PostambleVar.get())

    def CopyClipboard(self):
        self.clipboard_clear()
        for line in self.gcode:
            self.clipboard_append(line+'\n')

    def WriteToAxis(self):
        for line in self.gcode:
            sys.stdout.write(line+'\n')
        self.quit()

app = Application()
app.master.title("Grill.py 1.0 by Lawrence Glaister ")
app.mainloop()
