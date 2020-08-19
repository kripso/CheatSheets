import time
from faker import Faker
from mysql.connector import errorcode
import mysql.connector
import random
import codecs
import json
import uuid
import hashlib


User = 'DBS_User'
Password = 'DBS_user123'
DB_NAME = 'DBS_CLIMBING_CENTER'

fake = Faker()
numberOfEmployees = 1000
numberOfWork_days = 2000000
numberOfInstructors = int(numberOfEmployees - numberOfEmployees/3)
numberOfWorkshops = 100
numberOfRegistrations = numberOfWorkshops * 20
numberOfEquipments = 10000000
numberOfRents = 1000
numberOfcustomer = 10000
numberOfCard = 1000000

mydb = mysql.connector.connect(
    host="localhost",
    user=User,
    passwd=Password,
    database=DB_NAME
)

mycursor = mydb.cursor()

# create Employees
login = {}

for i in range(numberOfEmployees):
    fakeUser = fake.simple_profile()
    sql = "INSERT INTO employee VALUES (%s, %s, %s, %s,%s, %s, %s, %s)"
    username = fakeUser['username']
    login['username{}'.format(i)] = username
    password = fake.word()
    login['password{}'.format(i)] = password
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512((password+salt).encode()).hexdigest()
    val = (0, 0, fakeUser['name'].split()[0], fakeUser['name'].split()[1], username, hashed_password, salt, random.randint(1000, 2000))
    mycursor.execute(sql, val)
    mydb.commit()

with open('ktour.json', 'w+') as jsonfile:
    json.dump(login, jsonfile)

# create Instructors
focus = ['Bouldering', 'Top Rope', 'Sport Climbing', 'Traditional Climbing', 'Belaying']
for i in range(numberOfInstructors):
    sql = "INSERT INTO instructor VALUES (%s, %s,%s)"
    val = (0, i+1, focus[random.randint(0, 4)])
    mycursor.execute(sql, val)
    mydb.commit()

# create work day
hours = [6, 7, 8, 9, 10, 11, 12, 13, 14]
for i in range(numberOfWork_days):
    month = fake.month()
    day = fake.day_of_month()
    randomHour = random.randint(0, 8)
    date = fake.date_this_decade(before_today=True, after_today=False)
    time1 = '{} {}{}:00:00'.format(date, '' if randomHour > 3 else 0, hours[randomHour])
    time2 = '{} {}:00:00'.format(date, hours[randomHour]+8)

    timeFrom = time1
    timeTo = time2

    sql = "INSERT INTO work_day VALUES (%s, %s,%s, %s)"
    val = (0, fake.pyint(min_value=1, max_value=numberOfEmployees-1, step=1), time1, time2)

    mycursor.execute(sql, val)
    mydb.commit()

# create work_shop
for i in range(numberOfWorkshops):
    date = fake.date_this_decade(before_today=False, after_today=True)
    randomHour = random.randint(0, 8)
    time1 = '{} {}{}:00:00'.format(date, '' if randomHour > 3 else 0, hours[randomHour])

    sql = "INSERT INTO work_shop VALUES (%s, %s, %s, %s,%s, %s)"
    val = (0, fake.pyint(min_value=1, max_value=numberOfInstructors-1, step=1), fake.sentence(nb_words=10,
                                                                                              variable_nb_words=True, ext_word_list=None), random.randint(1, 20), time1, random.randint(20, 100))
    mycursor.execute(sql, val)
    mydb.commit()

# create customer
for i in range(numberOfcustomer):
    sql = "INSERT INTO customer VALUES (%s, %s, %s, %s,%s, %s)"
    sexes = ['Female', 'Male']
    rndSex = random.randint(0, 1)
    name = fake.first_name_female() if rndSex == 0 else fake.first_name_male()
    val = (0, name, fake.last_name(), sexes[rndSex], fake.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=80), fake.address())
    mycursor.execute(sql, val)
    mydb.commit()

# create Registrations
for i in range(numberOfRegistrations):
    fakeUser = fake.simple_profile()
    sql = "INSERT INTO registration VALUES (%s, %s, %s)"
    val = (0, random.randint(1, numberOfcustomer-1), random.randint(1, numberOfWorkshops-1))
    mycursor.execute(sql, val)
    mydb.commit()

# create card
for i in range(numberOfCard):
    sql = "INSERT INTO card (id, customer_ID,entries) VALUES (%s, %s,%s)"
    val = (0, fake.pyint(min_value=1, max_value=numberOfcustomer-1, step=1), random.randint(0, 10))
    mycursor.execute(sql, val)
    mydb.commit()

# create prices
entrieCost = '{ "adultEntry": "7€","studentEntry": "6€", "childEntry": "3€","familyEntry": "11€" }'
subscription = '{ "week": "20€","month": "50€","threeMonths": "120€","sixMonths": "200€","year": "360€"}'
rent_price = '{"trousers": "2€", "t-shirt": "2€", "shoes": "2€", "helmet": "1€", "harness": "2€", "rope": "4€", "chalk-bag": "1€", "belay": "1€"}'
sql = "INSERT INTO price VALUES (%s, %s, %s, %s)"
val = (0, entrieCost, subscription, rent_price)
mycursor.execute(sql, val)
mydb.commit()

# create size
size = '{"trousers": ["Small","Medium","Large","X-Large"],"t-shirt": ["Small","Medium","Large","X-Large"], "shoes":[40 ,40.5 ,41 ,41.5 ,42 ,42.5 ,43 ,43.5 ,44 ,44.5 ,45 ,45.5 ,46 ,46.5 ,47 ,47.5 ,48 ,48.5], "helmet": ["Small","Medium","Large","X-Large"], "harness": ["Small","Medium","Large","X-Large"] }'
sql = "INSERT INTO size VALUES (%s, %s)"
val = (0, size)
mycursor.execute(sql, val)
mydb.commit()

sizeTable = json.loads(size)
# create equipment
for i in range(numberOfEquipments):
    sexes = ['Female', 'Male']
    rndSex = random.randint(0, 1)
    types = ['trousers', 't-shirt', 'shoes', 'helmet', 'harness', 'rope', 'chalk-bag', 'belay']
    rndType = random.randint(0, len(types)-1)
    if types[rndType] not in sizeTable:
        sizeToType = 'NULL'
    else:
        sizeToType = sizeTable[types[rndType]][random.randint(0, len(sizeTable[types[rndType]])-1)]
    sql = "INSERT INTO equipment VALUES (%s, %s,%s,%s, %s)"
    val = (0, sexes[rndSex], types[rndType], sizeToType, random.randint(1, 5))
    mycursor.execute(sql, val)
    mydb.commit()

# create renting
for i in range(numberOfRents):
    date = fake.date_this_decade(before_today=True, after_today=False)
    hour = random.randint(6, 19)
    time1 = '{} {}{}:00:00'.format(date, '' if hour > 9 else 0, hour)
    time2 = '{} {}{}:00:00'.format(date, '' if hour+4 > 9 else 0, hour+4)
    sql = "INSERT INTO renting VALUES (%s, %s, %s, %s, %s)"
    val = (0, fake.pyint(min_value=1, max_value=numberOfcustomer-1, step=1), fake.pyint(min_value=1, max_value=numberOfEquipments-1, step=1), time1, time2)
    mycursor.execute(sql, val)
    mydb.commit()

mycursor.close()
mydb.close()
