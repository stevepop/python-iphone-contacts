import json
import csv

class PhoneContacts:
    es = None
    cfile = 'data/contacts.csv'
    export_file = 'data/contacts_export.csv'

    def __init__(self, es):
        self.es = es

    def checkElasticSearch(self):
        if self.es is None:
            return false
        else:
            return True

    # Check if the contact has any phone number
    def contact_has_number(self, contact):
        if contact["Mobile"] or contact["iPhone"] or contact["Home no"] or contact["Work"]:
             return True
        return False

    # Covert local numbers to International format (Only Nigeria and UK numbers)
    def convert_telephone_number(self, mobile):
        mobile_no = str(mobile)
        if (mobile_no[:3] == '080'):
            convert_no = '+234' + mobile_no[1:]
        elif (mobile_no[:2] == '07'):
            convert_no = '+44' + mobile_no[1:]
        else:
            convert_no = mobile_no
        return convert_no

    def index_contact_data(self):
        if self.checkElasticSearch():
          with open(self.export_file,"rU") as es_contacts:
            fieldnames = ['First Name','Last Name', 'Mobile','iPhone','Home no','Work']
            reader = csv.DictReader( es_contacts, fieldnames)
            id = 1
            for row in reader:
                data = json.dumps(row)
                self.es.index(index='contacts', doc_type='phone_numbers',id=id,body=data)
                id = id + 1
        else:
            print "Unable to connect to Elasticsearch instance"

    # Read the contact file and create a list of dictionaries with selected data
    def contacts_reader(self,contacts_file):
        # Open the file and import contacts data using DictReader
        reader = csv.DictReader(contacts_file, delimiter=',')
        contact_list = []
        
        # Loop through the contacts data and create a dictionary
        for line in reader:
            contact = {}
            if  self.contact_has_number(line):
                contact['First Name'] = line["First Name"]
                contact['Last Name'] = line["Last Name"]
                contact['Mobile'] = self.convert_telephone_number(line["Mobile"])
                contact['iPhone'] = self.convert_telephone_number(line["iPhone"])
                contact['Home no'] = self.convert_telephone_number(line["Home no"])
                contact['Work'] = self.convert_telephone_number(line["Work"])
                # Build a list of the contacts using the specified keys
                contact_list.append(contact)
        return contact_list

    def contacts_write(self,contacts_data):
     with open(self.export_file,'wb') as exportfile:
        fieldnames = ['First Name','Last Name', 'Mobile','iPhone','Home no','Work']
        writer = csv.DictWriter(exportfile, fieldnames=fieldnames)
        writer.writeheader()

        for item in contacts_data:
           writer.writerow(item)
        exportfile.close()   


    def index(self):
     with open(self.cfile,"rU") as f_contacts:
        contacts = self.contacts_reader(f_contacts)
        self.contacts_write(contacts)
        self.index_contact_data()
        print 'Export completed. Contacts Indexed in Elasticsearch!'





