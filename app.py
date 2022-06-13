from flask import Flask, request, jsonify, session, redirect, url_for
from helpers.db_helpers import *
import sys

app = Flask(__name__)

app.secret_key = "Super secret key"


# Basic requirements satisfied.  
@app.get('/api/posts')
def posts_get():
    # TODO: db SELECT
    posts_list = run_query("SELECT * FROM user_posts")
    resp = []
    for post in posts_list:
        an_obj = {}
        an_obj['username'] = post[1]
        an_obj['post'] = post[2]
        resp.append(an_obj)
    return jsonify(resp), 200

@app.post('/api/posts')
def create_post():
    data = request.json
    user_name = data.get('username')
    post_content = data.get('post')
    if not user_name:
        return jsonify("Missing required argument 'Username'"), 422
    if not post_content:
        return jsonify("Missing required argument 'Content'"), 422
    # TODO: Error checking the actual values for the arguments
    run_query("INSERT INTO user_posts (username, post) VALUES (?,?)", [user_name, post_content])
    return jsonify("Post added"), 201
    
@app.put('/api/posts')
def edit_post():
    params = request.args
    post_id = params.get('id')
    data = request.json
    post_content = data.get('post')
    run_query("UPDATE user_posts SET post = ? WHERE id=?", [post_content, post_id])
    return jsonify("Your post was successfully edited"), 205

@app.delete('/api/posts')
def delete_post():
    params = request.args
    user_id = params.get('id')
    run_query("DELETE FROM user_posts WHERE id=?",[user_id])
    return jsonify("Post deleted"),201


# This is the features section with an api to users, 
# where seperate tables are utilized: users, user_posts.

# @app.get('/login')
# def login():
#     data = request.json
#     username = data.get('username')
#     password = data.get('password')
#     user = run_query("SELECT id,username FROM users WHERE username=? AND password=?", [username,password])
#     if user:
#         session['loggedIn']=True
#         session['username']=user[0][1]
#         session['userId']=user[0][0]
#         return jsonify(session),201
#     else:
#         return jsonify("Missing required argument 'Username'"), 422

# @app.post('/login')
# def signup():
#     data = request.json
#     username = data.get('username')
#     password = data.get('password')
#     run_query("INSERT INTO users (username,password) VALUES (?,?)",[username,password])
#     session['loggedIn']=True
#     return jsonify(session),201
    
# @app.route('/logout')
# def logout():
#     session.pop('loggedIn', None)
#     session.pop('username', None)
#     return redirect(url_for('login'))

# @app.route('/user')
# def create_post():
#     user = session

# @app.post('/api/posts')
# def create_post():
#     data = request.json
#     post = data.get('post')
#     user_id = session['userId']
#     if not user_id:
#         return jsonify("You must be logged in to make a post.")
#     else:
#         run_query("INSERT INTO posts (post,post_user_id) VALUES (?)", [post,user_id])
#         return jsonify("Post created successfully!")
    



if (len(sys.argv) > 1):
    mode = sys.argv[1]
else:
    print("No mode argument: testing | production")
    exit()    
    
if mode == "testing":
    from flask_cors import CORS
    CORS(app)    # Only want CORS on testing servers
    app.run(debug=True)
elif mode == "production":
    import bjoern
    bjoern.run(app, "0.0.0.0", 5004)
    print('Running in development mode!')
else:
    print("Invalid mode.  Must be testing or production")