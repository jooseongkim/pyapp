from flask import Flask, render_template, request, redirect
import pymysql

conn = pymysql.connect(host = '127.0.0.1',
                          port = 3306,
                          db = 'pyapp',
                          user = 'root',
                          passwd= 'java1004')

# print(conn)
app = Flask(__name__)
# 21

        

# 1. msg 목록
@app.route('/', methods=['GET'])
def msg_list():
    cursor = conn.cursor()
    cursor.execute("SELECT msg_id, msg_text FROM msg")
    msglist = cursor.fetchall()
    return render_template('msglist.html',msglist = msglist)

 # 3. 삭제
@app.route('/del_msg', methods=['GET'])
def del_msg():
    msg_id = request.args.get('msg_id')
    # db 입력
    cursor = conn.cursor()
    cursor.execute('delete from msg where msg_id = (%s)', [msg_id])
    conn.commit()
    return redirect('/')

@app.route('/mod_msg',methods=['GET','POST'])
def mod_msg():
    if request.method == 'GET':
        msg_id = request.args.get('msg_id')
        cursor = conn.cursor()
        cursor.execute('select msg_id, msg_text from msg where msg_id=(%s)',[msg_id])
        modify = cursor.fetchone()
        return render_template('/modify.html',modify = modify)

    elif request.method == 'POST':
        msg_id = request.form['msg_id']
        msg_text = request.form['msg_text']
        cursor = conn.cursor()
        cursor.execute('update msg set msg_text=(%s) where msg_id=(%s)', [msg_text, msg_id])
        conn.commit()
        return redirect('/')

@app.route("/add_msg", methods=['GET', 'POST'])
def add_msg():
    if request.method =='GET':
        return render_template('add.html')
    elif request.method =='POST':
        msg_text = request.form['msg_text']
        cursor = conn.cursor()
        cursor.execute('INSERT INTO msg(msg_text) VALUES(%s)',[msg_text])
        conn.commit()
        return redirect('/')

app.run(host='127.0.0.1', port='80')