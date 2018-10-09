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
                if field.AS != None and data[fields[unicode(field.T, "utf-8")]] == 'TRUE':
                    print "Checkbox: ", field.T, field.V, field.AS
                    field.update(pdfrw.PdfDict(AS='Yes'))
                    field.update(pdfrw.PdfDict(V='Yes'))
                else:
                    field.update(pdfrw.PdfDict(V=data[fields[unicode(field.T, "utf-8")]]))
            else:
                print "Not found: '" + field.T + "'"
            # pprint(field.T)
    return page

def set_stupid_checkboxes(data, name):
    if data[name] == 'TRUE' or data[name] == 'Yes':
        data[name+'_yes'] = 'TRUE'
        data[name+'_no'] = 'FALSE'
    elif data[name] == 'FALSE' or data[name] == 'No':
        data[name+'_yes'] = 'FALSE'
        data[name+'_no'] = 'TRUE'
    else:
        data[name+'_yes'] = ''
        data[name+'_no'] = ''

def set_stupid_checkboxes_level(data, name):
    if data[name] == 'ALS':
        data[name+'_als'] = 'TRUE'
        data[name+'_bls'] = 'FALSE'
    elif data[name] == 'BLS':
        data[name+'_als'] = 'FALSE'
        data[name+'_bls'] = 'TRUE'
    else:
        data[name+'_als'] = ''
        data[name+'_bls'] = ''

def set_stupid_checkboxes_trauma(data, name):
    if data[name] == "Level 1" or data[name] == "Level 2" or data[name] == "Level 3" or data[name] == "Level 4":
        data[name+'_yes'] = 'TRUE'
    else:
        data[name+'_yes'] = 'FALSE'

def custom_ics202(data, fields):
    set_stupid_checkboxes(data, u'202_site_safety_plan')
    set_stupid_checkboxes(data, u'206_medical_aid_paramedic_1')

def custom_ics206(data, fields):
    set_stupid_checkboxes(data, u'206_medical_aid_paramedic_1')
    set_stupid_checkboxes(data, u'206_medical_aid_paramedic_2')
    set_stupid_checkboxes(data, u'206_medical_aid_paramedic_3')
    set_stupid_checkboxes(data, u'206_medical_aid_paramedic_4')
    set_stupid_checkboxes(data, u'206_medical_aid_paramedic_5')
    set_stupid_checkboxes(data, u'206_medical_aid_paramedic_6')

    set_stupid_checkboxes_level(data, u'206_transport_level_1')
    set_stupid_checkboxes_level(data, u'206_transport_level_2')
    set_stupid_checkboxes_level(data, u'206_transport_level_3')
    set_stupid_checkboxes_level(data, u'206_transport_level_4')

    set_stupid_checkboxes(data, u'206_hospital_burn_center_1')
    set_stupid_checkboxes(data, u'206_hospital_burn_center_2')
    set_stupid_checkboxes(data, u'206_hospital_burn_center_3')
    set_stupid_checkboxes(data, u'206_hospital_burn_center_4')
    set_stupid_checkboxes(data, u'206_hospital_burn_center_5')

    set_stupid_checkboxes(data, u'206_hospital_helipad_1')
    set_stupid_checkboxes(data, u'206_hospital_helipad_2')
    set_stupid_checkboxes(data, u'206_hospital_helipad_3')
    set_stupid_checkboxes(data, u'206_hospital_helipad_4')
    set_stupid_checkboxes(data, u'206_hospital_helipad_5')

    set_stupid_checkboxes_trauma(data, u'206_hospital_trauma_level_1')
    set_stupid_checkboxes_trauma(data, u'206_hospital_trauma_level_2')
    set_stupid_checkboxes_trauma(data, u'206_hospital_trauma_level_3')
    set_stupid_checkboxes_trauma(data, u'206_hospital_trauma_level_4')
    set_stupid_checkboxes_trauma(data, u'206_hospital_trauma_level_5')

def main(argv):
    with open(argv[0]) as data_file:    
        data = json.load(data_file, 'test2.pdf')
    fill_pdf(data)

def fill_pdf(data, filename):
        #pprint(data)
    print "Writing pdf to:", filename
    writer = pdfrw.PdfWriter()

    # TODO: Pass in page number so it can be added automatically
    #print "*** 202 start"
    with open('forms/ics202.json') as data_file:    
        ics202_map = json.load(data_file)
        # need to do this differently to capture defs to make checkboxes work
    first_page = pdfrw.PdfReader('forms/ics202-0.pdf')
    custom_ics202(data, ics202_map)
    ics202 = create_pdf(data, ics202_map, first_page.Root.Pages.Kids[0])
    writer.addpage(ics202)
    print first_page.numPages
    print "*** 203 start"
    with open('forms/ics203.json') as data_file:    
        ics203_map = json.load(data_file)
    template = pdfrw.PdfReader('forms/ics203.pdf')
    ics203 = create_pdf(data, ics203_map, template.Root.Pages.Kids[0])
    writer.addpage(ics203)
    first_page.Root.Pages.Kids.append(ics203)
    print first_page.numPages
    
    print "*** 205 start"
    with open('forms/ics205.json') as data_file:    
        ics205_map = json.load(data_file)
    template = pdfrw.PdfReader('forms/ics205-0.pdf')
    ics205 = create_pdf(data, ics205_map, template.Root.Pages.Kids[0])
    writer.addpage(ics205)

    print "*** 205a start"
    with open('forms/ics205a.json') as data_file:    
        ics205a_map = json.load(data_file)
    template = pdfrw.PdfReader('forms/ics205a.pdf')
    ics205a = create_pdf(data, ics205a_map, template.Root.Pages.Kids[0])
    writer.addpage(ics205a)

    print "*** 206 start"
    with open('forms/ics206.json') as data_file:    
        ics206_map = json.load(data_file)
    custom_ics206(data, ics206_map)
    template = pdfrw.PdfReader('forms/ics206-0.pdf')
    ics206 = create_pdf(data, ics206_map, template.Root.Pages.Kids[0])
    writer.addpage(ics206)

    print "*** 207 start"
    with open('forms/ics207.json') as data_file:    
        ics207_map = json.load(data_file)
    template = pdfrw.PdfReader('forms/ics207.pdf')
    ics207 = create_pdf(data, ics207_map, template.Root.Pages.Kids[0])
    writer.addpage(ics207)

    #writer.write('test2.pdf', first_page)
    writer.write('IAPs/'+filename)


if __name__ == '__main__':
    main(sys.argv[1:])
