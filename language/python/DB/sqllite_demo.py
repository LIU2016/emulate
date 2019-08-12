'''
        SQLite :
            可视化管理工具：www.sqlitebrowser.org

'''

import sqlite3
import os

data_path="./files/data1.sqlite"

if not os.path.exists(data_path):
    conn = sqlite3.connect(data_path);
    cursor = conn.cursor()
    cursor.execute('''
        create table persons 
        (
            id int primary key not null,
            name text not null,
            sex  int  not null
        )
    ''')
    conn.commit()
    conn.close()

conn = sqlite3.connect(data_path)
cursor = conn.cursor()
cursor.execute('''
        insert into persons (id ,name ,sex)
        values (005,'666真英雄',1)
''')
conn.commit()

personsList = cursor.execute('''
        select * from persons
''')
print(type(personsList))
result = []
for person in personsList:
    content = {}
    content['id']=person[0]
    content['name']=person[1]
    content['sex']=person[2]
    result.append(content)
conn.close()
print(result)

