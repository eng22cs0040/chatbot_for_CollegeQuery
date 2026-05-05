import sqlite3

from sqlite3 import Error

def sql_connection():

    try:

        con = sqlite3.connect('mydatabase.db')

        return con

    except Error:

        print(Error)

def sql_table(con):

    cursorObj = con.cursor()

    cursorObj.execute("CREATE TABLE BotResponse(Answer text)")
    cursorObj.execute("INSERT INTO BotResponse VALUES('test answer1')")
    cursorObj.execute("INSERT INTO BotResponse VALUES('test answer2')")

    con.commit()

con = sql_connection()

sql_table(con)