from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode

User = 'DBS_User'
Password = 'DBS_user123'

connection = mysql.connector.connect(user=User, password=Password)
cursor = connection.cursor()


DB_NAME = 'DBS_CLIMBING_CENTER'

TABLES = {}
TABLES['customer'] = (
    "CREATE TABLE `customer` ("
    "   `id` INT AUTO_INCREMENT PRIMARY KEY,"
    "   `name` VARCHAR(64) NOT NULL,"
    "   `surname` VARCHAR(64) NOT NULL,"
    "   `sex` ENUM('Female','Male') NOT NULL,"
    "   `birth` DATE NOT NULL,"
    "   `settlment` VARCHAR(248) NOT NULL"
    ");")

TABLES['employee'] = (
    "CREATE TABLE `employee` ("
    "   `id` INT AUTO_INCREMENT PRIMARY KEY,"
    "   `admin` boolean default false NOT NULL,"
    "   `name` VARCHAR(64) NOT NULL,"
    "   `surname` VARCHAR(64) NOT NULL,"
    "   `username` VARCHAR(64) NOT NULL,"
    "   `password` VARCHAR(248) NOT NULL,"
    "   `salt` VARCHAR(248) NOT NULL,"
    "   `salary` INT NOT NULL,"
    "    CONSTRAINT `user` UNIQUE (`username`,`password`)"
    ");")

TABLES['work_day'] = (
    "CREATE TABLE `work_day` ("
    "  `id` INT AUTO_INCREMENT PRIMARY KEY,"
    "  `employee_id` INT,"
    "  `from` DATETIME,"
    "  `to` DATETIME,"
    "   CONSTRAINT fk_employee_wd FOREIGN KEY (`employee_id`) REFERENCES employee(`id`)"
    ");")

TABLES['instructor'] = (
    "CREATE TABLE `instructor` ("
    "  `id` INT AUTO_INCREMENT PRIMARY KEY,"
    "  `employee_id` INT,"
    "  `focus` VARCHAR(124) NOT NULL,"
    "   CONSTRAINT fk_employee_in FOREIGN KEY (`employee_id`) REFERENCES employee(`id`)"
    ");")

TABLES['workshop'] = (
    "CREATE TABLE `work_shop` ("
    "  `id` INT AUTO_INCREMENT PRIMARY KEY,"
    "  `instructor_id` INT,"
    "  `text` TINYTEXT NOT NULL,"
    "  `capacity` SMALLINT DEFAULT 1,"
    "  `date` DATETIME NOT NULL,"
    "  `cost` SMALLINT,"
    "  CONSTRAINT fk_instructor FOREIGN KEY (`instructor_id`) REFERENCES instructor(`id`) ON UPDATE CASCADE ON DELETE CASCADE"
    ");")

TABLES['registration'] = (
    "CREATE TABLE `registration` ("
    "  `id` INT AUTO_INCREMENT PRIMARY KEY,"
    "  `customer_id` INT,"
    "  `workshop_id` INT,"
    "  CONSTRAINT fk_customer_reg FOREIGN KEY (`customer_id`) REFERENCES customer(`id`) ON UPDATE CASCADE ON DELETE CASCADE,"
    "  CONSTRAINT fk_workshop FOREIGN KEY (`workshop_id`) REFERENCES work_shop(`id`) ON UPDATE CASCADE ON DELETE CASCADE"
    ");")

TABLES['equipment'] = (
    "CREATE TABLE `equipment` ("
    "  `id` INT AUTO_INCREMENT PRIMARY KEY,"
    "  `sex` ENUM('male', 'female'),"
    "  `type` ENUM('trousers', 't-shirt', 'shoes', 'helmet', 'harness', 'rope', 'chalk-bag', 'belay'),"
    "  `size` VARCHAR(24),"
    "  `detrition` ENUM('1', '2', '3', '4', '5')"
    ");")

TABLES['renting'] = (
    "CREATE TABLE `renting` ("
    "  `id` INT AUTO_INCREMENT PRIMARY KEY,"
    "  `customer_id` INT,"
    "  `equipment_id` INT,"
    "  `from` DATETIME,"
    "  `to` DATETIME,"
    "  CONSTRAINT fk_customer_ren FOREIGN KEY (`customer_id`) REFERENCES customer(`id`),"
    "  CONSTRAINT fk_equipment FOREIGN KEY (`equipment_id`) REFERENCES equipment(`id`)"
    ");")


TABLES['card'] = (
    "CREATE TABLE `card` ("
    "   `id` INT AUTO_INCREMENT PRIMARY KEY,"
    "   `customer_ID` INT,"
    "   `valid_from` DATETIME,"
    "   `valid_to` DATETIME,"
    "   `entries` INT,"
    "    CONSTRAINT fk_customer FOREIGN KEY (`customer_ID`) REFERENCES customer(`id`) ON UPDATE CASCADE ON DELETE SET NULL"
    ");")

TABLES['price'] = (
    "CREATE TABLE `price` ("
    "   `id` INT AUTO_INCREMENT PRIMARY KEY,"
    "   `entrie_cost` JSON NOT NULL,"
    "   `subscription` JSON NOT NULL,"
    "   `rent_price` JSON NOT NULL"
    ");")

TABLES['size'] = (
    "CREATE TABLE `size` ("
    "   `id` INT AUTO_INCREMENT PRIMARY KEY,"
    "   `sizes` JSON NOT NULL"
    ");")


def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        connection.database = DB_NAME
    else:
        print(err)
        exit(1)
for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")
