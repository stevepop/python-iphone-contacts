# This is a script to read through my iPhone contacts exported to a csv file
import csv
import json
import elasticsearch

cfile = 'data/contacts.csv'
export_file = 'data/contacts_export.csv'

def index_contact_data(es):
	with open(export_file,"rU") as es_contacts:
		fieldnames = ['First Name','Last Name', 'Mobile','iPhone','Home no','Work']
		reader = csv.DictReader( es_contacts, fieldnames)
		id = 1
		for row in reader:
			data = json.dumps(row)
			es.index(index='contacts', doc_type='phone_numbers',id=id,body=data)
			id = id + 1

def convert_telephone_number(mobile):
	mobile_no = str(mobile)
	if (mobile_no[:3] == '080'):
		convert_no = '+234' + mobile_no[1:]
	elif (mobile_no[:2] == '07'):
		convert_no = '+44' + mobile_no[1:]
	else:
		convert_no = mobile_no
	return convert_no

# Check if the contact has any phone number
def contact_has_number(contact):
	if contact["Mobile"] or contact["iPhone"] or contact["Home no"] or contact["Work"]:
		return True
	return False


# Read the contact file and create a list of dictionaries with selected data
def contacts_reader(contacts_file):
	# Open the file and import contacts data using DictReader
	reader = csv.DictReader(contacts_file, delimiter=',')
	contact_list = []
	
	# Loop through the contacts data and create a dictionary
	for line in reader:
		contact = {}
		if contact_has_number(line):
			contact['First Name'] = line["First Name"]
			contact['Last Name'] = line["Last Name"]
			contact['Mobile'] = convert_telephone_number(line["Mobile"])
			contact['iPhone'] = convert_telephone_number(line["iPhone"])
			contact['Home no'] = convert_telephone_number(line["Home no"])
			contact['Work'] = convert_telephone_number(line["Work"])
			# Build a list of the contacts using the specified keys
			contact_list.append(contact)
	return contact_list

def contacts_write(contacts_data):
	with open('data/contacts_export.csv','wb') as exportfile:
		fieldnames = ['First Name','Last Name', 'Mobile','iPhone','Home no','Work']
		writer = csv.DictWriter(exportfile, fieldnames=fieldnames)

		writer.writeheader()
		for item in contacts_data:
			writer.writerow(item)
	exportfile.close()


def index():
	es = elasticsearch.Elasticsearch()
	with open(cfile,"rU") as f_contacts:
		contacts = contacts_reader(f_contacts)
		contacts_write(contacts)
		index_contact_data(es)
	print 'Export completed. Contacts Indexed in Elasticsearch!'


if __name__ == '__main__':
    index()


