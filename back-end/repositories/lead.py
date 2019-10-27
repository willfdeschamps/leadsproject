from repositories import mongo_db
import datetime

def count_leads(filter):
    return mongo_db.people.count_documents(filter)

def upsert_lead(filter, lead):
    insertLead = {
        "email" : lead['email'],
        "created": datetime.datetime.utcnow(),
    }
    updateLead = {
        "telefone" : lead['telefone'],
        "cargo" : lead['cargo']
    }
    mergeConversions = {"conversions": {"material" : lead['material']}} if lead['material'] is not None and lead['material'] != "" else None
    
    upsertJSON = {
        "$set" : updateLead,
        "$setOnInsert": insertLead
    }

    if mergeConversions is not None:
        upsertJSON['$addToSet'] = mergeConversions

    return mongo_db.people.update_one(filter, upsertJSON, upsert=True)

def aggregate_lead(pipeline):
    return mongo_db.people.aggregate(pipeline)