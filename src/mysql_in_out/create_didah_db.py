from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode

cnx = mysql.connector.connect(user='igor', host='localhost', password='adelante')
cursor = cnx.cursor()



DB_NAME = 'didah'


# TABLES['salaries'] = (
#     "CREATE TABLE `salaries` ("
#     "  `emp_no` int(11) NOT NULL,"
#     "  `salary` int(11) NOT NULL,"
#     "  `from_date` date NOT NULL,"
#     "  `to_date` date NOT NULL,"
#     "  PRIMARY KEY (`emp_no`,`from_date`), KEY `emp_no` (`emp_no`),"
#     "  CONSTRAINT `salaries_ibfk_1` FOREIGN KEY (`emp_no`) "
#     "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE"
#     ") ENGINE=InnoDB")

TABLES = {}
TABLES['series_rr'] = (
    "CREATE TABLE `series_rr` ("
    "  `ser_id` smallint(4) NOT NULL DEFAULT '-9999',"
    # "  `ser_date` date NOT NULL DEFAULT '0000-00-00',"
    "  `ser_date` date NOT NULL,"
    "  `rr` smallint(5) NOT NULL DEFAULT '-9999',"
    "  `qc` tinyint(1) NOT NULL DEFAULT '-9',"
    "  `qcm` tinyint(1) NOT NULL DEFAULT '-9',"
    "  `qca` tinyint(1) NOT NULL DEFAULT '-9',"
    "  PRIMARY KEY (`ser_id`,`ser_date`)"
    ") ENGINE=MyISAM")

# | series_rr | CREATE TABLE `series_rr` (
#   `ser_id` smallint(4) NOT NULL DEFAULT '-9999',
#   `ser_date` date NOT NULL DEFAULT '0000-00-00',
#   `rr` smallint(5) NOT NULL DEFAULT '-9999',
#   `qc` tinyint(1) NOT NULL DEFAULT '-9',
#   `qcm` tinyint(1) NOT NULL DEFAULT '-9',
#   `qca` tinyint(1) NOT NULL DEFAULT '-9',
#   PRIMARY KEY (`ser_id`,`ser_date`)
# ) ENGINE=MyISAM DEFAULT CHARSET=latin1 |





# # Post creationg printout:
# | salaries | CREATE TABLE `salaries` (
#   `emp_no` int(11) NOT NULL,
#   `salary` int(11) NOT NULL,
#   `from_date` date NOT NULL,
#   `to_date` date NOT NULL,
#   PRIMARY KEY (`emp_no`,`from_date`),
#   KEY `emp_no` (`emp_no`),
#   CONSTRAINT `salaries_ibfk_1` FOREIGN KEY (`emp_no`) REFERENCES `employees` (`emp_no`) ON DELETE CASCADE
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8 |





def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cnx.database = DB_NAME  
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)



for name, ddl in TABLES.iteritems():
    try:
        print("Creating table {}: ".format(name), end='')
        cursor.execute(ddl)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.close()
cnx.close()


