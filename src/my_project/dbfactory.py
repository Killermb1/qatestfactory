from dbutils import get_connection
import dbfunctions as db
from faker import Faker
import random

fake = Faker()

def createFakeBankEmployeeRecords(count):
    """Generates synthetic employee records adhering to the bank_employees schema."""
    print("We are creating faker records")
    records = []
    
    # Fetch existing bank IDs from the database
    bankIds = [att["bank_id"] for att in db.getBanksDetails()]
        
    for _ in range(count):
        records.append(
             (
                 f"{fake.first_name()} {fake.last_name()}",  # fullname
                 fake.unique.email(),                         # email_id
                 round(fake.pyfloat(min_value=30000, max_value=150000, right_digits=2), 2),  # salary
                 fake.random_int(min=22, max=60),             # age
                 random.choice(bankIds),                      # bank_id (dynamically chosen from fetched IDs)
                 fake.city(),                                 # branch
                 fake.address().replace('\n', ', '),          # address
                 fake.boolean(chance_of_getting_true=90),     # indian (True/False or 1/0)
                 fake.phone_number()[:20]                     # mobile_number
             )
        )
    return records

print(createFakeBankEmployeeRecords(2))
