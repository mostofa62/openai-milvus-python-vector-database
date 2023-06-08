from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)
COLLECTION_NAME = 'pdf_data'
MILVUS_HOST = 'localhost'  # Milvus server URI
MILVUS_PORT = '19530'

def connect_db():
    connections.connect(
    "default", 
    host=MILVUS_HOST, 
    port=MILVUS_PORT)
    print('...connected....')


#fields
DIMENSION = 1536  # Embeddings size
COUNT = 100  # How many category to embed and insert.
fields = [
    FieldSchema(name='id', dtype=DataType.INT64, descrition='Ids', is_primary=True, auto_id=False),
    FieldSchema(name='category', dtype=DataType.VARCHAR, description='Category', max_length=200),
    FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, description='Embedding vectors or pdf contents', dim=DIMENSION),
    FieldSchema(name='content', dtype=DataType.VARCHAR, description='pdf contents', max_length=20000)
]

schema = CollectionSchema(fields=fields, description='Category wise pdf collection')


# Create collection
def create_collection(name: str = "pdf_data"):
   collection = Collection(name=name, schema=schema, using="default", shards_num=2)
   return collection



# Create an index for the collection.
# Create an index for the collection.
index_params = {
    'index_type': 'IVF_FLAT',
    'metric_type': 'L2',
    'params': {'nlist': 32}
}

INDEX_DATA = {
   "field_name": "embedding",
   "index_params": index_params,
   "index_name": "pdf_data_search",
}

def get_or_create_collection(
   name: str = "pdf_data",
   create_index: bool = True,
   index_data: dict = INDEX_DATA,
   load_data: bool = False,
):
    

    try:
       # Connect to the database
       connect_db()

       # Fetch the collection object by name
       collection = Collection(name)
    except Exception as excetion:
       print(excetion)
       print("Creating Collection...")
       
       # If collection is not available, create a collection
       collection = create_collection(name=name)

       # Create index if unavailable
       # Here we will provide index_data (INDEX_DATA) that we have defined above.
       if create_index and index_data:
           collection.create_index(**index_data)
       

    finally:
       #collection.load()
       return collection