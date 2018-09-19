#!/opt/local/bin/python2.7
# This Python file uses the following encoding: utf-8

from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from textwrap import TextWrapper
import pdfrw

# General
incident_name = 'Armageddon'
op_period = '1'
op_start_date = '4/7/2018'
op_start_time = '0800'
op_end_date = '4/7/9999'
op_end_time = '1500'
prepared_by = 'Keith'
page = '1/9'
ics_203 = '√'
ics_204 = '√'
ics_205 = '√'
ics_205A = '√'
ics_206 = '√'
ics_207 = '√'
ics_208 = '√'
ics_map = '√'
ics_weather = '√'

# ICS 200
objectives = ('''
The focus will be personal on-rope skills in the context of technical search.  
We will be working on rappelling and ascending a fixed line in the wilderness setting.
Beginners will work on standard rappels and ascents on increasingly steep slope while more experienced members will work on rappelling, searching an area, and then continuing the rappel or ascending.
Time permitting, we will work in some pickoffs, simulating the rescue of an injured searcher.
''')

command_emphasis = ('''
Carefully manage risk exposure at all times. 
This is a training. Do not take any unecesssary risks.
Wear proper PPE whenever activly participating in training.
''')

situational_awareness = ('''
Maintain adequate hydration at all times.
Watch for Posion Oak.
''')

canv = Canvas('test.pdf',
              pagesize=letter,
              cropMarks=True,
)
img = ImageReader('ics202-0.png')
#    registerFont(TTFont('arial','C:\\windows\\fonts\\arial.ttf'))
 
#now begin the work
#canv.drawImage(img,x,y,w,h,anchor='sw',anchorAtXY=True,showBoundary=False)
x = 0
y = 0
w, h = letter
canv.translate(-1*inch, -1*inch)

canv.drawImage(img, inch, inch, w, h, anchor='nw')
#    canv.setFont('arial',14)
canv.setFillColor((1,0,0)) #change the text color
canv.drawString(1.6*inch, h-0.18*inch, incident_name)
canv.drawString(5.0*inch, h-0.18*inch, op_period)

canv.drawString(6.7*inch, h+0.04*inch, op_start_date)
canv.drawString(6.7*inch, h-0.18*inch, op_start_time)

canv.drawString(8.1*inch, h+0.04*inch, op_end_date)
canv.drawString(8.1*inch, h-0.18*inch, op_end_time)

canv.drawString(3.15*inch, h-8.60*inch, prepared_by)

canv.drawString(3.70*inch, h-9.13*inch, page)

textobject = canv.beginText()
textobject.setTextOrigin(1.6*inch, h-0.6*inch)
wrapper = TextWrapper(width=100)
paras=objectives.splitlines()
for para in paras:
    lines = wrapper.wrap(para)
    textobject.textLines(lines)
    textobject.moveCursor(0,3)
canv.drawText(textobject)

textobject = canv.beginText()
textobject.setTextOrigin(1.6*inch, h-4.3*inch)
wrapper = TextWrapper(width=100)
paras=command_emphasis.splitlines()
for para in paras:
    lines = wrapper.wrap(para)
    textobject.textLines(lines)
    textobject.moveCursor(0,3)
canv.drawText(textobject)

textobject = canv.beginText()
textobject.setTextOrigin(1.6*inch, h-5.85*inch)
wrapper = TextWrapper(width=100)
paras=situational_awareness.splitlines()
for para in paras:
    lines = wrapper.wrap(para)
    textobject.textLines(lines)
    textobject.moveCursor(0,3)
canv.drawText(textobject)

canv.drawString(1.69*inch, h-7.52*inch, ics_203)
canv.drawString(1.69*inch, h-7.75*inch, ics_204)
canv.drawString(1.69*inch, h-7.96*inch, ics_205)
canv.drawString(1.69*inch, h-8.19*inch, ics_205A)
canv.drawString(1.69*inch, h-8.40*inch, ics_206)

canv.drawString(3.11*inch, h-7.53*inch, ics_207)
canv.drawString(3.11*inch, h-7.73*inch, ics_208)
canv.drawString(3.11*inch, h-7.95*inch, ics_map)
canv.drawString(3.11*inch, h-8.18*inch, ics_weather)

canv.save()

