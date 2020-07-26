import mysql.connector
import random
import codecs
import json
from mysql.connector import errorcode
import hashlib
import uuid
from faker import Faker
import time

User = 'DBS_User'
Password = 'DBS_user123'
DB_NAME = 'DBS_CLIMBING_CENTER'

fake = Faker()
numberOfEmployees = 1000
numberOfWork_days = 1000
numberOfInstructors = int(numberOfEmployees - numberOfEmployees/3)
numberOfWorkshops = 40
numberOfRegistrations = numberOfWorkshops * 20
numberOfEquipments = 1000
numberOfRents = 1000
numberOfCostumer = 1000
numberOfCard = 1000

salt = uuid.uuid4().hex
password = 'passworsssssd'
hashed_password = hashlib.sha512((password+salt).encode()).hexdigest()
print(hashed_password, salt)
