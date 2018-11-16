#!/opt/local/bin/python3.7
# This Python file uses the following encoding: utf-8
import io, sys
import pdfrw
import json
from pprint import pprint
from google.cloud import storage
from datetime import datetime

local=False
#import gcp_storage

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
            if field.T in fields and fields[field.T] in data:
                if field.AS != None and data[fields[field.T]] == 'TRUE':
#                    print("Checkbox: ", field.T, field.V, field.AS)
                    field.update(pdfrw.PdfDict(AS='Yes'))
                    field.update(pdfrw.PdfDict(V='Yes'))
                else:
                    field.update(pdfrw.PdfDict(V=data[fields[field.T]]))
#                    print("Update: ", field.T, field.V, field.AS, fields[field.T], data[fields[field.T]])
            else:
                print("Not found: '" + field.T + "'")
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

def fill_pdf(data, filename):
    print("Writing pdf to:", filename)
    writer = pdfrw.PdfWriter()

    forms = ['ics200', 'ics202', 'ics203', 'ics205', 'ics205a', 'ics206', 'ics207', '215a']
    #forms = ['ics215a']
    # Coversheet is unnumbered, so this will number 202 as page 1
    pagenum=0
    dt = datetime.now().strftime("%Y-%m-%d %H:%m")
    data['prepared_datetime'] = dt
    # metadata - IAP-name-op_period_start_date_time
    dt = datetime.now().strftime("%Y-%m-%d %H:%m:%S")
    metadata = ( "IAP-" + data['200_incident_name']
                 + "-OP" + data['200_op_num']
                 + "-" + dt)
    data['metadata'] = metadata
    for form in forms:
        print("Filling ", form)
        ics_map = get_field_map(form)
        pdf = get_pdf(form)
        data['pagenum'] = str(pagenum)
        page = create_pdf(data, ics_map, pdf.Root.Pages.Kids[0])
        writer.addpage(page)
        pagenum += 1
        
    url = put_pdf(writer, 'IAPs/'+filename)
    return url

def get_field_map(form):
    print('Getting map for', form)
    blobname = 'forms/'+form+'.json'

    if not local:
        storage_client = storage.Client()
        bucket_name = 'krb-dev.appspot.com'
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.get_blob(blobname)
        data = blob.download_as_string()
        field_map = json.loads(data)
    else:
        with open(blobname) as data_file:
            field_map = json.load(data_file)

    print('Done Getting map for', form)
    return field_map
    
def get_pdf(form):
    print('Getting pdf for', form)
    blobname = 'forms/'+form+'.pdf'
    if not local:
        storage_client = storage.Client()
        bucket_name = 'krb-dev.appspot.com'
        bucket = storage_client.get_bucket(bucket_name)
        #print("blob", blobname)
        blob = bucket.get_blob(blobname)
        #print("got blob", blob.id)
        data = blob.download_as_string()
        #print("blob size", data.len)
        page = pdfrw.PdfReader(fdata=data)
    else:
        page = pdfrw.PdfReader(blobname)
    print('Done Getting pdf for', form)
    return page


def put_pdf(writer, blobname):
    print('Storing', blobname)
    if not local:
        storage_client = storage.Client()
        bucket_name = 'krb-dev.appspot.com'
        bucket = storage_client.get_bucket(bucket_name)
        filename = '/tmp/'+str(hash(blobname))
        #print("Writing pdf to", filename)
        writer.write(filename)
        #print("getting blob", blobname)
        blob = bucket.blob(blobname)
        #print("uploading blob", blobname)
        blob.upload_from_filename(filename, content_type='application/pdf')
        #print("making public")
        blob.make_public()
        #print("getting url", blobname)
        url = blob.public_url
    else:
        writer.write(blobname)
        url = 'none'
    print('Stored', blobname, 'to', url)
    return url

def main(argv):
    print("local", local)
    with open(argv[0]) as data_file:
       data = json.load(data_file)
    fill_pdf(data, 'test2.pdf')

if __name__ == '__main__':
    local=True
    main(sys.argv[1:])

