#import all library
import os
import time
from vectordb import get_or_create_collection
from loadpdfcontent import *
from openaiembed import get_insert_embed
#load a pdf

pdf_content = get_pdf_content('javascript1.pdf')
#print(len(pdf_content))
#chunk it using langchain text splitter
pdf_split_content=split_and_chunk(pdf_content)
#print(len(pdf_split_content))
#print(pdf_split_content[10])
#create vector database collection

collection = get_or_create_collection()
#embed on open ai
for i in range(len(pdf_split_content)):
    data={
        "id":(100+i),
        "category":"javascirpt",
        "text":pdf_split_content[i]
        }
    print('inserting..',i)
    ins = get_insert_embed(data)
    collection.insert(ins)
    time.sleep(3)


