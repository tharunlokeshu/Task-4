from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for users
users = {}

# Home route
@app.route('/')
def home():
    return "Welcome to the User API!"

# GET all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

# GET a specific user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

# POST a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user_id = data.get("id")
    name = data.get("name")
    email = data.get("email")

    if not all([user_id, name, email]):
        return jsonify({"error": "Missing required fields"}), 400

    if user_id in users:
        return jsonify({"error": "User already exists"}), 409

    users[user_id] = {"name": name, "email": email}
    return jsonify({"message": "User created", "user": users[user_id]}), 201

# PUT (Update) a user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    users[user_id].update(data)
    return jsonify({"message": "User updated", "user": users[user_id]})

# DELETE a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        deleted = users.pop(user_id)
        return jsonify({"message": "User deleted", "user": deleted})
    return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
