# training_data.py

training_records = []

def add_training_record(record):
    training_records.append(record)
    return {"message": "Training data submitted successfully"}

def get_all_records():
    return training_records

def delete_training_record(company_id, inss, calendar_year, training=None):
    for record in training_records:
        if (record["companyId"] == company_id and
            record["inss"] == inss and
            record["calendarYear"] == calendar_year):

            if training:
                before = len(record["trainings"])
                record["trainings"] = [
                    t for t in record["trainings"]
                    if not (t["denomination"] == training["denomination"] and t["startDate"] == training["startDate"])
                ]
                after = len(record["trainings"])
                return {"message": f"Removed {before - after} training(s)"}
            else:
                training_records.remove(record)
                return {"message": "Training record deleted successfully"}

    return {"message": "Training record not found"}



import secrets

api_key = secrets.token_hex(16)
print(api_key)

