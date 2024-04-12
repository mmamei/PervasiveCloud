from google.cloud import firestore

db_name = 'test'
db = firestore.Client.from_service_account_json('credentials.json',
                                                database=db_name)

def print_coll(coll):
    print('Print collection')
    for doc in db.collection(coll).stream(): # select * from sensor2
        print(f'{doc.id} --> {doc.to_dict()}')


coll = 'sensor4'
for i in range(10):
    doc_ref = db.collection(coll).document(f'id{i}')  # id can be omitted
    doc_ref.set({'year': 2020+i, 'value': 10})

print_coll(coll)
