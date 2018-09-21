#!/opt/local/bin/python2.7
# This Python file uses the following encoding: utf-8
import io, sys
import pdfrw
import json
from pprint import pprint
 
def print_fields(page):
    print("{")
    if page.Annots != None:
        for field in page.Annots:
            #print field.T, field.Type, field.Subtype, "T: ", field.T, "V: ", field.V, "AS: ", field.AS
            if field.T != None:
                print('"' + str(field.T) + '": "",')
    print("}")


def main(argv):
    # print "*** 202 start"
    # template = pdfrw.PdfReader('ics202-0.pdf')
    # print_fields(template)

    print ("Reading", argv[0])
    template = pdfrw.PdfReader(argv[0])
    print("Pages ", template.numPages)
    #    if template.numpages != None:
    print_fields(template.Root.Pages.Kids[0])
    # for page in template.Root.Pages.Kids:
    #     print_fields(page)

if __name__ == '__main__':
    main(sys.argv[1:])
