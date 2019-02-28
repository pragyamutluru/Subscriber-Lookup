from flask import Flask, render_template, url_for
app = Flask(__name__)
# Connect to db
import pyodbc
conn = pyodbc.connect(
     'DRIVER={ODBC Driver 13 for SQL Server};'
     # 'UID=pragyamu;'
     #'WSID=PRAGYAMU02;'
    # 'APP={Microsoft® Windows® Operating System};'
     'Trusted_Connection=Yes;'
     'SERVER=localhost'
    #'DSN=SQLS;UID=pragyamu;'
)

cursor = conn.cursor()
posts=cursor


def fetchPosts():
    global posts
    global columns
    cursor.execute('SELECT * FROM ETE1ANF.dbo.AC_SOURCE')
    posts = cursor

    columns = [column[0] for column in posts.description]
    columns.insert(0,"#")
    # print(columns)

@app.route("/home")
@app.route("/")
def home():
    fetchPosts()
    return render_template('home.html', posts=posts, columns=columns)


if __name__ == '__main__':
    app.run(debug=True)