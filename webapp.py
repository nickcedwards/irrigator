import sqlite3
import config
from flask import Flask

app = Flask(__name__)

def get_latest():
    con = sqlite3.connect(config.DB)
    cur = con.cursor()
    cur.execute("SELECT * FROM readings ORDER BY timestamp DESC LIMIT 1")
    return repr(cur.fetchone())


@app.route('/')
def hello_world():
    return get_latest()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
