import mysql.connector

#variable
dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'Metallic@3'
)

#prepare a cursor object
cursorObject = dataBase.cursor()

#create the database db_dcrm
cursorObject.execute("CREATE DATABASE db_dcrm")

print("DATABASE CREATED !")  