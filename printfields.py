#!/opt/local/bin/python2.7
# This Python file uses the following encoding: utf-8
import io, sys
import pdfrw
import json
from pprint import pprint
 
# data - map between data names and value
# field - map between pdf field names and data names
# template - pdf to be filled in
def print_fields(template):
    print "{"
    for page in template.Root.Pages.Kids:
        for field in page.Annots:
            #print field.T, field.Type, field.Subtype, "T: ", field.T, "V: ", field.V, "AS: ", field.AS
            print '"' + str(field.T) + '": "",'
    print "}"


def main(argv):
    # print "*** 202 start"
    # template = pdfrw.PdfReader('ics202-0.pdf')
    # print_fields(template)

    template = pdfrw.PdfReader('ics205-0.pdf')
    print_fields(template)

if __name__ == '__main__':
    main(sys.argv[1:])
