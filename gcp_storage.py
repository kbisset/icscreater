#!/opt/local/bin/python3.7
import json

from google.cloud import storage

def get_field_map(form):
    storage_client = storage.Client()
    bucket_name = 'krb-dev.appspot.com'
    bucket = storage_client.get_bucket(bucket_name)
    blobname = 'forms/'+form+'.json'
    blob = bucket.get_blob(blobname)
    data = blob.download_as_string()
    field_map = json.loads(data)
    return field_map
    
def get_pdf(form):
    storage_client = storage.Client()
    bucket_name = 'krb-dev.appspot.com'
    bucket = storage_client.get_bucket(bucket_name)
    blobname = 'forms/'+form+'.pdf'
    data = bucket.get_blob(blobname)
    page = pdfrw.PdfReader(fdata=data)
    return page


def put_pdf(writer, blobname):
    print('Writing', blobname)
    storage_client = storage.Client()
    bucket_name = 'krb-dev.appspot.com'
    bucket = storage_client.get_bucket(bucket_name)
    filename = '/tmp/'+hash(blobname)
    writer.write(filename)
    blob = blob.Blob(blobname, bucket)
    blob.upload_from_filename(filename)
    url = blob.publilc_url()
    print('Wrote', blobname, 'to', url)
    return url
