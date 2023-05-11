from google.cloud import firestore

db = firestore.Client.from_service_account_json('credentials.json')

coll = 'sensors2'

def print_coll():
    print('Print collection')
    for doc in db.collection(coll).stream(): # select * from sensor2
        print(f'{doc.id} --> {doc.to_dict()}')


# creazione di un entity (document)
id = 'ciao'
doc_ref = db.collection(coll).document(id) #id can be omitted
doc_ref.set({'nome':'sensor','value': [{'val':1}]})
print(doc_ref.get().id)

# accesso a un documento specifico (dato l'id)
entity = db.collection(coll).document(id).get()
print(entity.id,'--->',entity.to_dict()['nome'])


# aggiungi un campo o modifica un campo esistente, se faccio di nuovo la set, sostituisco l'intero dizionario
doc_ref.update({'value2':5})

# incrementa un campo
doc_ref.update({'value2': doc_ref.get().to_dict()['value2']+1})
doc_ref.update({'value2': firestore.Increment(50)})

l = doc_ref.get().to_dict()['value']
l.append(3)
doc_ref.update({'value': l})

print_coll()

#cencellazione di un entità
doc_ref = db.collection(coll).document(doc_ref.get().id) # opzionale, reimposto doc_ref a partire da doc_ref.
doc_ref.delete()

print_coll()


print('###########################################')

for i in [1,2,3,4,5,6]:
    doc_ref = db.collection(coll).document()
    doc_ref.set({'nome':'sensor','value': i})

print_coll()

# where queries
print('Query')
for doc in db.collection(coll).where('value','>',2).stream():
    print(f'{doc.id} --> {doc.to_dict()}')

for doc in db.collection(coll).stream():
    db.collection(coll).document(doc.id).delete()

print_coll()

