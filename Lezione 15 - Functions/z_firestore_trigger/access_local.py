from google.cloud import firestore

db = firestore.Client()

e = db.collection('persone').document('matteomamei')
if e.get().exists:
    e.update({'counter':firestore.Increment(1)})
else:
    e.set({'counter':1})

for doc in db.collection('persone').stream():
    print(f'{doc.id} --> {doc.to_dict()}')