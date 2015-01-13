# This is a script to read through my iPhone contacts exported to a csv file
import csv
cfile = 'data/contacts.csv'

def convert_telephone_number(mobile):
	mobile_no = str(mobile)
	print mobile_no
	if (mobile_no[:3] == '080'):
		convert_no = '+234' + mobile_no[1:]
	elif (mobile_no[:2] == '07'):
		convert_no = '+44' + mobile_no[1:]
	else:
		convert_no = mobile_no
	return convert_no

# Read the contact file and create a list of dictionaries with selected data
def contacts_reader(contacts_file):
	# Open the file and import contacts data using DictReader
	reader = csv.DictReader(contacts_file, delimiter=',')
	contact_list = []
	
	# Loop through the contacts data and create a dictionary
	for line in reader:
		contact = {}
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



	
with open(cfile,"rU") as f_contacts:
	contacts = contacts_reader(f_contacts)
	contacts_write(contacts)
print 'Export completed'
