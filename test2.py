#!/opt/local/bin/python2.7
# This Python file uses the following encoding: utf-8
import io
import pdfrw
 
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from textwrap import TextWrapper

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

template = pdfrw.PdfReader('ics205-0.pdf')
print template

for page in template.Root.Pages.Kids:
    for field in page.Annots:
        print field.T, field.Type, field.Subtype, "T: ", field.T, "V: ", field.V
        if field.T == '(Date From)':
            print field.T, field.V
            field.update(pdfrw.PdfDict(V=op_start_date))
        if field.T == '(3 Objectives)':
            print field.T, field.V
            field.update(pdfrw.PdfDict(V=objectives))
        if field.T == '(ICS 203)' :
            field.update(pdfrw.PdfDict(V='Yes'))
            print field.T, field.V
        if field.T == '(ICS 204)' :
            field.update(pdfrw.PdfDict(V=''))
            print field.T, field.V
            # field.update(pdfrw.PdfDict(V=objectives))
pdfrw.PdfWriter().write('test2.pdf', template)
