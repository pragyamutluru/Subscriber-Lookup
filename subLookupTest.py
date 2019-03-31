from __future__ import print_function # In python 2.7
from flask import Flask, render_template, url_for, redirect, request

import sys
app = Flask(__name__)
# Connect to db
import pyodbc
conn = pyodbc.connect(
     'DRIVER={ODBC Driver 13 for SQL Server};'
     # 'UID=pragyamu;'
     #'WSID=PRAGYAMU02;'
    # 'APP={Microsoft® Windows® Operating System};'
     'Trusted_Connection=Yes;'
     'SERVER=localhost;'
    'MARS_Connection=Yes'
    #'DSN=SQLS;UID=pragyamu;'
)

cursor = conn.cursor()
posts=cursor

#Make a list of tables and the queries we need to execute in them
# queryList = ['SELECT * FROM ETE1ANF.dbo.s where SUBSCRIBER_NO = '
#              ,'SELECT * FROM ETE1ANF.dbo.agd1_RESOURCES where SUBSCRIBER_id = '
#              ,'Select * from ETE1ANF.dbo.subscriber_history where subscriber_no ='
#              ,'Select * from ETE1ANF.dbo.ape1_subscr_data where subscriber_id ='
#              ,'Select * from ETE1ANF.dbo.ape1_subscr_offers where subscriber_id ='
# ]

queryList = ['SELECT * FROM ETE1ANF.dbo.s where SUBSCRIBER_NO = '
             ,'SELECT * FROM ETE1ANF.dbo.agd1_RESOURCES where SUBSCRIBER_ID= '
             ,'Select * from ETE1ANF.dbo.APE1_SUBSCR_DATA where _SUBSCRIBER_id_  ='
             ,'Select * from ETE1ANF.dbo.APE1_SUBSCR_OFFERS where _SUBSCRIBER_id_  ='
]

postsList= [[[None]]]*4
columnsList=[[[None]]]*6
cursorList=[None]*4

def fetchPosts():
    global posts
    global columns
    cursor.execute('SELECT * FROM ETE1ANF.dbo.s')
    posts = cursor

    columns = [column[0] for column in posts.description]
    columns.insert(0,"#")
    # print(columns)

def fetchPosts2(data):
    global posts
    global columns
    cursor.execute('SELECT * FROM ETE1ANF.dbo.s where SUBSCRIBER_NO = '+data)
    posts = cursor

    columns = [column[0] for column in posts.description]
    columns.insert(0,"#")
    # print(columns)

def fetchByList( list, data):
    global postsList
    global columnsList
    global cursorList


    for i in range(0,len(list)):
        cursorList.insert(i, conn.cursor()  )

        # postsList.insert(list.index(item),cursor)
        postsList[i]= (cursorList[i].execute(list[i]+data))


        columnsList[i] =\
            [column[0] for column
             in postsList[i].description]
        columnsList[i].insert(0, "#")
        # cursorList[i].close()



@app.route("/home")
@app.route("/")
def home():
    fetchPosts()
    return render_template('home.html', posts=posts, columns=columns)

# @app.route('/button/')
# def searchFunction():
#     fetchPosts()
#     return render_template('home.html', posts=posts, columns=columns)

@app.route('/button', methods=['POST'])
def my_form_post():
    text = request.form['sub_no']
    #add a check to see if the number is valid or not
    # to be inserted

    fetchByList(queryList,text)
    print(postsList)
    print(columnsList)
    return render_template('home_test.html', postsList=postsList, columnsList=columnsList)


if __name__ == '__main__':
    app.run(debug=True)