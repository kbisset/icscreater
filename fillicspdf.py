#!/opt/local/bin/python2.7
# This Python file uses the following encoding: utf-8
import io, sys
import pdfrw
import json
from pprint import pprint

# from reportlab.lib.utils import ImageReader
# from reportlab.pdfgen.canvas import Canvas
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.pdfbase.pdfmetrics import registerFont
# from reportlab.lib.pagesizes import letter
# from reportlab.lib.units import inch
# from textwrap import TextWrapper

# print template

#pprint(ics202)

# data - map between data names and value
# field - map between pdf field names and data names
# template - pdf to be filled in
def create_pdf(data, fields, page):
    for field in page.Annots:
        if field.T != None:
            if field.T in fields and fields[unicode(field.T, "utf-8")] in data:
                if (field.AS == '/Yes' and data[fields[unicode(field.T, "utf-8")]] != u'Yes'):
                    field.update(pdfrw.PdfDict(AS='/Off'))
                    field.update(pdfrw.PdfDict(V=''))
                    a=1
                else:
                    field.update(pdfrw.PdfDict(V=data[fields[unicode(field.T, "utf-8")]]))
                    # print field.T, field.Type, field.Subtype, "T: ", field.T, "V: ", field.V, "AS: ", field.AS
            else:
                print "Not found: " + field.T
                # pprint(field.T)
    return page

    
    # canv = Canvas('test2.pdf', pagesize=letter)
    # w, h = letter
    # canv.drawString(5.0*inch, h-0.18*inch, data[u'op_period'])
#    canv.save()

def main(argv):
    with open(argv[0]) as data_file:    
        data = json.load(data_file)
    #pprint(data)
    writer = pdfrw.PdfWriter()

    # TODO: Pass in page number so it can be added automatically
    print "*** 202 start"
    with open('forms/ics202.json') as data_file:    
        ics202_map = json.load(data_file)
    template = pdfrw.PdfReader('forms/ics202-0.pdf')
    ics202 = create_pdf(data, ics202_map, template.Root.Pages.Kids[0])
    writer.addpage(ics202)

    print "*** 203 start"
    with open('forms/ics203.json') as data_file:    
        ics203_map = json.load(data_file)
    template = pdfrw.PdfReader('forms/ics203.pdf')
    ics203 = create_pdf(data, ics203_map, template.Root.Pages.Kids[0])
    writer.addpage(ics203)

    print "*** 205 start"
    with open('forms/ics205.json') as data_file:    
        ics205_map = json.load(data_file)
    template = pdfrw.PdfReader('forms/ics205-0.pdf')
    ics205 = create_pdf(data, ics205_map, template.Root.Pages.Kids[0])
    writer.addpage(ics205)

    print "*** 206 start"
    with open('forms/ics206.json') as data_file:    
        ics206_map = json.load(data_file)
    template = pdfrw.PdfReader('forms/ics206-0.pdf')
    ics206 = create_pdf(data, ics206_map, template.Root.Pages.Kids[0])
    writer.addpage(ics206)

    writer.write('test2.pdf')


if __name__ == '__main__':
    main(sys.argv[1:])
