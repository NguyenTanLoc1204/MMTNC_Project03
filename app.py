from flask import Flask, request

app = Flask(__name__)

DB_PASSWORD = "admin_password"

flag = "NTL{P3rs0nal_Pr0j3ct_N3tW0rK1ing__Xss_S11cc3ss}"

@app.route('/')
def hello_world():
    return "DevSecOps Demo"

@app.route('/search')
def search():
    user_input = request.args.get('query', '')

    if user_input == DB_PASSWORD:
        return flag
    else:
        return f"Sai password: {user_input}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
