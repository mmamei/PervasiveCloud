from google.cloud import firestore

db = firestore.Client()

#creazione di un entity (document)
entity = db.collection('persone').document('marcomamei')
#entity.set({'nome':'marco','cognome':'mamei'})

# posso non mettere un id, e automaticamente fare il set di proprietà (chaining)
#db.collection('persone').document().set({'nome':'matteo','cognome':'mamei'})

#update
#entity.update({'nome':'Marco'})


#for doc in db.collection('persone').stream():
#    print(f'{doc.id} --> {doc.to_dict()}')

for doc in db.collection('persone').where('nome','==','matteo').stream():
    print(f'{doc.id} --> {doc.to_dict()}')