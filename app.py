from flask import Flask,g,request,jsonify
from db import get_db
from functools import wraps

app = Flask(__name__)

api_username = 'simeone'
api_password = 'Jamesrodriguez10'

def protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == api_username and auth.password == api_password:
            return f(*args,**kwargs)
        else:
            return jsonify({'message' : 'Authentication failed'}), 403
    return decorated



@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()




@app.route('/user',methods=['GET'])
@protected
def get_users():
    data = get_db()
    users_cur = data.execute('select id, name, email, level from users')
    users = users_cur.fetchall()

    return_values = []
    for user in users:
        user_dict = {}
        user_dict['id'] = user['id']
        user_dict['name'] = user['name']
        user_dict['email'] = user['email']
        user_dict['level'] = user['level']

        return_values.append(user_dict)
   
    return jsonify ({'users': return_values, 'username' : username, 'password' : password })


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    
    data = get_db()
    user_cur = data.execute('select id, name, email, level from users where id = ?',[user_id])    
    user = user_cur.fetchone()


    return jsonify({ 'user' : {'id': user['id'], 'name': user['name'], 'email': user['email'], 'level': user['level']}})
    

@app.route('/user',methods=['POST'])
def add_user():
    new_user_data = request.get_json()

    name = new_user_data['name']
    email = new_user_data['email']
    level = new_user_data['level']

    data = get_db()
    data.execute('insert into users (name, email, level) values (?, ?, ?)',[name,email,level])
    data.commit()

    user_cur = data.execute('select id, name, email, level from users where name = ?',[name])    
    new_user = user_cur.fetchone()


    return jsonify({ 'user' : {'id': new_user['id'], 'name': new_user['name'], 'email': new_user['email'], 'level': new_user['level']}})

@app.route('/user/<int:user_id>',methods=['PUT','PATCH'])
def edit_user(user_id):
    new_user_data = request.get_json()

    name = new_user_data['name']
    email = new_user_data['email']
    level = new_user_data['level']
    
    data = get_db()
    data.execute('update users set name = ?, email = ?, level = ? where id = ?',[name,email,level,user_id])
    data.commit()
    
    user_cur = data.execute('select id, name, email, level from users where id = ?',[user_id])
    user = user_cur.fetchone()

    return jsonify({ 'user' : {'id': user['id'], 'name': user['name'], 'email': user['email'], 'level': user['level']}})

@app.route('/user/<int:user_id>',methods=['DELETE'])
def delete_user(user_id):
    data = get_db()
    data.execute('delete from users where id = ?',[user_id])
    data.commit()

    return jsonify({'message' : 'The user has been deleted!'})





if __name__=='__main__':
    app.run(debug=True)
