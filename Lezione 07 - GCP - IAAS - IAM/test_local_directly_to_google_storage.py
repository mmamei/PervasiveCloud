from google.cloud import storage
client = storage.Client.from_service_account_json('mamei-lezione8-1187f0d1db4b.json')
#bucket = client.create_bucket('upload-mamei-1')
bucket = client.bucket('mamei-lezione8')
source_file_name = 'test.jpg'
destination_blob_name = source_file_name
blob = bucket.blob(destination_blob_name)
blob.upload_from_filename(source_file_name)
print("File {} uploaded to {}.".format(source_file_name, destination_blob_name))

