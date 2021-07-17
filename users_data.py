import sqlite3
import pandas
database=sqlite3.connect('user_data')
cur=database.cursor()

#create_table='create table user_db(username varchar(20),password varchar(20),mobile varchar(20))'

#cur.execute(create_table)




login="select * from user_db"
cur.execute(login)
data=cur.fetchall()
for i in data:
    print(i)
database.commit()
