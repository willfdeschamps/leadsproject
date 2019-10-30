from flask import Flask
from flask import request as req

import pymongo
from datetime import datetime, timezone

from repositories.lead import count_leads, upsert_lead, aggregate_lead


def _loadLead(req):
    email = req.form.get('email')
    telefone = req.form.get('telefone')
    cargo = req.form.get('cargo')
    material = req.form.get('material')
    return {
        "email" : req.form.get('email'), 
        "telefone" : req.form.get('telefone'), 
        "cargo" : req.form.get('cargo'),
        "material" : req.form.get('material')
        }

def _mountLeadsClusteredByConversion(initialDate, finalDate):
    pipeline = [
    {"$match" : {'created' : {"$gte": initialDate, "$lte": finalDate}}},
    {"$project": { "_id": 0, "conversions": 1 } },
    {"$unwind": "$conversions" },
    {"$group": { "_id": "$conversions", "qty": { "$sum": 1 } }},
    {"$project": { "_id": 0,"conversions": "$_id", "qty": 1 } },
    {"$sort": { "qty": -1 } }
    ]

    leadsClusteredByConversion = {}
    for doc in aggregate_lead(pipeline):
         leadsClusteredByConversion[doc['conversions']['material']] = doc['qty']
    return leadsClusteredByConversion

def lead():
    if (req.form is None):
        return "Invalid form"

    lead = _loadLead(req)
    upsert_lead({'email': lead['email']}, lead)
    return "Lead saved"

def data():
    initialDate = req.args.get('initialDate')
    finalDate = req.args.get('finalDate') + " 23:59:59"
    
    try:
        initialDate = datetime.strptime(initialDate, '%d/%m/%Y')
        finalDate = datetime.strptime(finalDate, '%d/%m/%Y %H:%M:%S')
    except:
        return "Invalid date format", 400  
    
    initialDateIsoFormat = initialDate.astimezone().isoformat()
    finalDateIsoFormat = finalDate.astimezone().isoformat()
    
    print(datetime.now(timezone.utc).astimezone().isoformat())
    totalLeads = count_leads({'created' : {"$gte": initialDateIsoFormat, "$lte": finalDateIsoFormat}})
    leadsClusteredByConversion = _mountLeadsClusteredByConversion(initialDateIsoFormat, finalDateIsoFormat)
    totalLeadsWithConversions = count_leads({'created' : {"$gte": initialDateIsoFormat, "$lte": finalDateIsoFormat}, "conversions":{"$exists":"true","$ne":[]}})

    return {"totalLeads" : totalLeads,
            "totalLeadsWithConversions" : totalLeadsWithConversions,
            "leadsClusteredByConversion": leadsClusteredByConversion}