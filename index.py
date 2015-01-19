import elasticsearch
import PhoneContacts

es = elasticsearch.Elasticsearch("es1.stevepop.dev:9200")

contacts = PhoneContacts.PhoneContacts(es)
contacts.index()
