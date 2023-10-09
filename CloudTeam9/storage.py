from google.cloud import datastore, storage


datastore_client = datastore.Client()
storage_client = storage.Client()

def list_db_entries():
    query = datastore_client.query(kind="photos")
    
    for photo in query.fetch():
        print(photo.items())

def add_db_entry(object):
    entity = datastore.Entity(key=datastore_client.key("photos"))
    entity.update(object)

def fetch_db_entry(object):
    
    query = datastore_client.query(kind="photos")
    
    for attr in object.keys():
        query.add_filter(attr, "=", object[attr])
    
    obj = list(query.fetch())
    
    return obj

def get_list_of_files(bucket_name):
    print("get_list_of_files: "+bucket_name)
    
    blobs = storage_client.list_blobs(bucket_name)
    print(blobs)
    files = []
    for blob in blobs:
        files.append(blob.name)
    
    return files

# Send file to bucket
def upload_file(bucket_name, file_name, file_data):
    print("upload_file: " + bucket_name + "/" + file_name)
    
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    
    file_data.seek(0)
    # Upload the file data directly instead of specifying a local file path
    blob.upload_from_file(file_data)

def download_file(bucket_name, file_name):
    print("download_file: "+bucket_name+"/"+file_name)
    
    bucket = storage_client.bucket(bucket_name)
    
    blob = bucket.blob(file_name)
    blob.reload()
    
    return

#print(get_list_of_files("testkey1"))


try:
    bucket = storage_client.create_bucket("testing12312312312312312")

except:
    print("BUCKET ALREADY EXISTS")

try:
    print(storage_client.get_bucket("testing12312312312312312"))
    blob = bucket.blob("test1")
    print(blob)
except:
    print("BUCKET NOT ACCESSABLE")
