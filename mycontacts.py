# This is a script to read through my iPhone contacts exported to a csv file
import csv
cfile = 'data/contacts.csv'


def contacts_reader(contacts_file):
	# Open the file and import contacts data using DictReader
	reader = csv.DictReader(contacts_file, delimiter=',')
	contact_list = []
	
	# Loop through the contacts data and create a dictionary
	for line in reader:
		contact = {}
		contact['First Name'] = line["First Name"]
		contact['Last Name'] = line["Last Name"]
		contact['Mobile'] = line["Mobile"]
		contact['iPhone'] = line["iPhone"]
		# Build a list of the contacts using the specified keys
		contact_list.append(contact)
	print contact_list
	
with open(cfile,"rU") as f_contacts:
	contacts_reader(f_contacts)
