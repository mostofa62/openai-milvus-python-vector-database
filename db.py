import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:64000/")
mydb = myclient["chatpdf"]

def my_col(name):
    return mydb[name]