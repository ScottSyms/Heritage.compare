# from bert_score import score
from evaluate import load
from sqlalchemy import MetaData, Table, create_engine, inspect, update
from sqlalchemy.sql import select

def compare(text1, text2):
    return bertscore.compute(predictions=text1, references=text2, model_type="distilbert-base-uncased")["recall"][0]

bertscore = load("bertscore")

dbcon = create_engine(
    'sqlite:////Users/scottsyms/code/HeritageCanada/data/fish/sample2.db')

metadata = MetaData()
source = Table(
    'source', metadata, autoload=True, autoload_with=dbcon)

print("Beginning translation ...  ")

# Modify English
result = dbcon.execute(select(
    [source.c.id, source.c.english, source.c.french, source.c.spanish]).limit(5))
