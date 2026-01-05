from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "NTL{H3llo_Pr0j3ct_CI/CD w1th j3nk1ns, D0ck3er!!}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')