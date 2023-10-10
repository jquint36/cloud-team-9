from google.cloud import datastore, storage


datastore_client = datastore.Client()
storage_client = storage.Client()

def list_db_entries(key):
    query = datastore_client.query(kind=key)
    
    for photo in query.fetch():
        print(photo.items())

def add_db_entry(object, key):
    # Create an entity key with the specified kind
    entity_key = datastore_client.key(key, key+"|"+object['Name'])

    # Create a new entity with the given key
    entity = datastore.Entity(key=entity_key)

    # Update the entity with the provided data
    entity.update(object)

    # Save the entity to Datastore
    datastore_client.put(entity)
    print("updated")

def fetch_db_entry(object,key):
    
    query = datastore_client.query(kind=key)
    
    for attr in object.keys():
        query.add_filter(attr, "=", object[attr])
    
    obj = list(query.fetch())
    
    return obj

def get_list_of_files(bucket_name):
    print("get_list_of_files: "+bucket_name)
    
    try:
        bucket = storage_client.create_bucket(bucket_name)

    except:
        print("BUCKET ALREADY EXISTS")

    try:
        
        blobs = storage_client.list_blobs(bucket_name)
        print(blobs)
        files = []
        for blob in blobs:
            files.append(blob.name)
        
        return files
    except:
        return

# Send file to bucket
def upload_file(bucket_name, file_name, file_data):
    print("upload_file: " + bucket_name + "/" + file_name)
    
    try:
        bucket = storage_client.create_bucket(bucket_name)

    except:
        print("BUCKET ALREADY EXISTS")

    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        file_data.seek(0)
        # Upload the file data directly instead of specifying a local file path
        blob.upload_from_file(file_data)
        
        return blob.size
    except:
        print("BUCKET NOT ACCESSABLE")
    return
    
def delete_file(bucket_name, file_name):
    print("delete_file: " + bucket_name + "/" + file_name)

    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        blob.delete()
    except:
        print("BUCKET NOT ACCESSABLE")
    return

def download_file(bucket_name, file_name):
    print("download_file: "+bucket_name+"/"+file_name)
    
    bucket = storage_client.bucket(bucket_name)
    
    blob = bucket.blob(file_name)
    blob.reload()
    
    return