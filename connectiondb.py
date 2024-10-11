import pymongo

def connection():
    try:
        client = pymongo.MongoClient("mongodb+srv://brunolcnregistrazioni:q98uPkbgFaTmSkI6@sakebo.vs61e.mongodb.net/")
        
        db = client["data"]
        return db
    
    except pymongo.errors.ConnectionError as e:
        print(f"Errore di connessione: {e}")
        return None