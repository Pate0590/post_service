# post_service.py

from flask import Flask, jsonify, request
import requests

app = Flask(__name__)
posts = {
        '1': {'user_id': '1', 'post': 'Hello, world!'},
        '2': {'user_id': '2', 'post': 'My first blog post'}
    }

@app.route('/')
def hello():
    return "i am live now"

@app.route('/post/<id>')
def post(id):
    
    post_info = posts.get(id, {})
    
    if post_info:
        response = requests.get(f'http://localhost:5001/user/{post_info["user_id"]}')
        if response.status_code == 200:
            post_info['user'] = response.json()

    return jsonify(post_info)
@app.route('/post', methods=['POST'])
def create_post():
    new_post = request.get_json()
    
    required_keys = ['user_id',  'post']

    if all(key in new_post for key in required_keys):
        posts[str(len(posts.keys()) + 1)] = new_post
        print(posts)
        return jsonify({"success":True})
    else:
        return jsonify({"success":False, "msg": "Please pass all the data"})
    
@app.route('/post/<id>', methods=['PUT'])
def update_post(id):
    
    if id in posts:
        updated_post = request.get_json()

        required_keys = ['user_id',  'post']
        if all(key in updated_post for key in required_keys):
            posts[id] = updated_post
            print(posts)
            return jsonify({"success": True, "msg": "post updated successfully"})
        else:
            return jsonify({"success": False, "msg": "Please pass all the required data for update"}), 400
    else:
        return jsonify({"success": False, "msg": "post not found"}), 404
    
@app.route('/post/<id>', methods=['DELETE'])
def delete_post(id):
    if id in posts:
        
        del posts[id]
        return jsonify({"success": True, "msg": "post deleted successfully"})
    else:
        return jsonify({"success": False, "msg": "post not found"}), 404



if __name__ == '__main__':
    app.run(port=5001)