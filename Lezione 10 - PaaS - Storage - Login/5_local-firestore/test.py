from google.cloud import firestore

db = 'test1'
coll = 'table1'

db = firestore.Client.from_service_account_json('credentials.json', database=db)

'''
# creazione di un entity (document)
id = 'ciao'
doc_ref = db.collection(coll).document() #id can be omitted
doc_ref.set({'nome':'sensor','value': [{'val':2}]})
print(doc_ref.get().id)
'''


# accesso a un documento specifico (dato l'id)
id = 'dghrthftf'
entity = db.collection(coll).document(id).get()
print(entity.exists)
if entity.to_dict() == None:
    print('non esiste')
else:
    print('esiste')

#print(entity.id,'--->',entity.to_dict()['nome'])
#print(entity.id,'--->',entity.to_dict()['value'])

'''
# aggiungi un campo o modifica un campo esistente, se faccio di nuovo la set, sostituisco l'intero dizionario

id = 'ciao'
doc_ref = db.collection(coll).document(id)
doc_ref.update({'value2':5})
# incrementa un campo
doc_ref.update({'value2': doc_ref.get().to_dict()['value2']+1})
doc_ref.update({'value2': firestore.Increment(50)})
l = doc_ref.get().to_dict()['value']
l.append(3)
doc_ref.update({'value': l})
entity = doc_ref.get()
for k,v in entity.to_dict().items():
    print(k,v)




# faccio di nuovo la set
id = 'ciao'
doc_ref = db.collection(coll).document(id)
doc_ref.set({'a':1})
for k,v in doc_ref.get().to_dict().items():
    print(k,v)



# query

def print_coll():
    print('Print collection')
    for entity in db.collection(coll).stream(): # select * from sensor2
        print(f'{entity.id} --> {entity.to_dict()}')

print_coll()





def print_coll():
    print('Print collection')
    for entity in db.collection(coll).stream(): # select * from sensor2
        print(f'{entity.id} --> {entity.to_dict()}')



#cencellazione di un entità
id = 'ciao'
doc_ref = db.collection(coll).document(id)
doc_ref.delete()

print_coll()




print('###########################################')

def print_coll():
    print('Print collection')
    for entity in db.collection(coll).stream(): # select * from sensor2
        print(f'{entity.id} --> {entity.to_dict()}')



for i in [1,2,3,4,5,6]:
    doc_ref = db.collection(coll).document()
    doc_ref.set({'nome':'sensor','value': i})

print_coll()

# where queries
print('Query')
for doc in db.collection(coll).where('value','>',2).stream():
    print(f'{doc.id} --> {doc.to_dict()}')

#for doc in db.collection(coll).stream():
#    db.collection(coll).document(doc.id).delete()

print_coll()

'''


