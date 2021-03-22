from flask import Flask, render_template, jsonify, request, abort
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'flask-backend'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
con = mysql.connect()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users')
def users():
    cur = con.cursor()
    cur.execute("select * from users order by id")
    con.commit()
    users = []
    for id, name, address, role in cur.fetchall():
        user = dict()
        user['id'] = id
        user['name'] = name
        user['address'] = address
        user['role'] = role
        users.append(user)
    return jsonify(users)

@app.route('/users/delete/<user_id>', methods=['POST'])
def delete(user_id):
    cur = con.cursor()
    cur.execute('delete from users where id=' + user_id)
    con.commit()
    return jsonify({'result': True})

@app.route('/users/add', methods=['POST'])
def add():
    cur = con.cursor()
    name = request.form.get('name')
    address = request.form.get('address')
    role = request.form.get('role')
    if not name or not address:
        abort(500)
    cur.execute('insert into users values("%s", "%s", "%s")' % (name, address, role))
    con.commit()
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)