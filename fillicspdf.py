#!/opt/local/bin/python3.7
import io, sys
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject, ArrayObject, TextStringObject, ByteStringObject, PdfObject
from PyPDF2.utils import string_type
import json
from pprint import pprint
from google.cloud import storage
from datetime import datetime

# Skip google clound stuff if we are running locally
local=False

# from reportlab.lib.utils import ImageReader
# from reportlab.pdfgen.canvas import Canvas
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.pdfbase.pdfmetrics import registerFont
# from reportlab.lib.pagesizes import letter
# from reportlab.lib.units import inch
# from textwrap import TextWrapper

# Why are there two checkboxes for a binary choice?
def set_stupid_checkboxes(data, name):
    name_yes = name+'_yes'
    name_no = name+'_no'
    if data[name].lower() == 'true' or data[name].lower() == 'yes':
        data[name_yes] = 'TRUE'
        data[name_no] = 'FALSE'
    elif data[name].lower() == 'false' or data[name].lower() == 'no':
        data[name_yes] = 'FALSE'
        data[name_no] = 'TRUE'
    else:
        data[name_yes] = ''
        data[name_no] = ''

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

# PyPDF2 doesn't produce checkboxes that show checks everywhere.
# Copy all the /Annots from the individual pages to the top level /AcroFrom./Fields
# /NeedAppearances may not be necessary, but shouldn't hurt
# This depends on internals of PdfWriter, but there doesn't appear to be a batter way
def enable_checkboxes(writer):
    # See 12.7.2 and 7.7.2 for more information:
    # http://www.adobe.com/content/dam/acom/en/devnet/acrobat/pdfs/PDF32000_2008.pdf
    if "/AcroForm" not in writer._root_object:
        print("Adding /AcroForm", len(writer._objects))
        writer._root_object.update({
            NameObject("/AcroForm"): IndirectObject(len(writer._objects), 0, writer)})
    if "/NeedAppearances" not in writer._root_object["/AcroForm"]:
        need_appearances = NameObject("/NeedAppearances")
        writer._root_object["/AcroForm"][need_appearances] = BooleanObject(True)
    if "/Fields" not in writer._root_object["/AcroForm"]:
        fields = NameObject("/Fields")
        writer._root_object["/AcroForm"][fields] = ArrayObject()
            
    for page in writer._root_object["/Pages"]["/Kids"]:
        writer._root_object["/AcroForm"][fields].extend(page.getObject()['/Annots'])
    return writer

# Write out exactly what is given with no translation
class PlainTextStringObject(string_type, PdfObject):
    def __init__(self, value):
        self.value = value
    def writeToStream(self, stream, encryption_key):
        bytes_ = self.value.encode()
        stream.write(bytes_)

# Handle checkboxs
def updatePageFormFieldValues(writer, page, fields):
    '''
        Update the form field values for a given page from a fields dictionary.
        Copy field texts and values from fields to page.

        :param page: Page reference from PDF writer where the annotations
            and field data will be updated.
        :param fields: a Python dictionary of field names (/T) and text
            values (/V)
        '''
    # Iterate through pages, update field values
    for j in range(0, len(page['/Annots'])):
        writer_annot = page['/Annots'][j].getObject()
        for field in fields:
            if writer_annot.get('/T') == field:
                if writer_annot.get('/FT') == '/Btn':
                    if fields[field].lower() == "true" or fields[field].lower() == "yes":
                        writer_annot.update({
                            NameObject("/V"): PlainTextStringObject('/0')
                        })
                    else:
                        writer_annot.update({
                            NameObject("/V"): PlainTextStringObject('/')
                        })
                else:
                    writer_annot.update({
                        NameObject("/V"): TextStringObject(fields[field])
                    })

def fill_pdf(data, filename):
    print("Writing pdf to:", filename)
    writer = PdfFileWriter()

    forms = ['ics200', 'ics202', 'ics203', 'ics205', 'ics205a', 'ics206', 'ics207', 'ics215a']
    #forms = ['ics215a']
    pagenum=1
    dt = datetime.now().strftime("%Y-%m-%d %H:%m")
    # TODO: Individual prepared dates for each form set whenever a form is changed
    data['prepared_datetime'] = dt
    # metadata - IAP-name-op_period_start_date_time
    dt = datetime.now().strftime("%Y-%m-%d %H:%m:%S")
    metadata = ( "IAP-" + data['200_incident_name']
                 + "-OP" + data['200_op_num']
                 + "-" + dt)
    data['metadata'] = metadata
    field_map = {}
    for form in forms:
        print("Filling ", form)
        ics_map = get_field_map(form)
        if form == 'ics202':
            custom_ics202(data, ics_map)
        if form == 'ics206':
            custom_ics206(data, ics_map)

        data['pagenum_'+form] = str(pagenum)+"/"+str(len(forms))
        for field in ics_map:
            if ics_map[field] in data:
                #print("Field '%s' '%s' '%s'"%(field, ics_map[field], data[ics_map[field]]))
                field_map[field] = data[ics_map[field]]

        pdf = get_pdf(form)
        #page = create_pdf(data, ics_map, pdf.getPage(0))
        page = pdf.getPage(0)
        writer.addPage(page)
        # print("Field Map")
        # pprint(field_map)
        # print("Document Fields Before")
        # fields = pdf.getFields();
        # pprint(fields)

        updatePageFormFieldValues(writer, pdf.getPage(0), field_map)
        # print("Document Fields After")
        # fields = pdf.getFields();
        # pprint(fields)

        pagenum += 1
        
    enable_checkboxes(writer)
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
        #page = pdfrw.PdfReader(fdata=data)
        page = PdfFileReader(fdata=data)
    else:
        page = PdfFileReader(blobname)
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
        outfile = open(blobname, "wb")
        writer.write(outfile)
        outfile.close
        url = blobname
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

