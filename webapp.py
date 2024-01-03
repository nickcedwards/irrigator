import sqlite3
import config
from flask import Flask, jsonify
from functools import wraps
import jinja2

templateLoader = jinja2.FileSystemLoader( searchpath="." )
template_env = jinja2.Environment( loader=templateLoader )

app = Flask(__name__)

def get_cursor():
    con = sqlite3.connect(config.DB)
    con.row_factory = sqlite3.Row
    return con.cursor()

def return_json(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        response = jsonify(f())
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    return wrap

def add_single_row(cur, query, template_vars):
    cur.execute(query)
    row = cur.fetchone()
    if not row:
        return
    for k in row.keys():
        if k != 'id':
            template_vars[k] = row[k]

@app.route('/')
def main():
    cur = get_cursor()
    template_vars = {
        'vbat': -1,
        'temperature': -1,
        'humidity': -1,
    }
    add_single_row(cur, "SELECT * FROM readings ORDER BY timestamp DESC LIMIT 1", template_vars)
    add_single_row(cur, "SELECT * FROM status LIMIT 1", template_vars)
    add_single_row(cur, "SELECT * FROM settings ORDER BY id DESC LIMIT 1", template_vars)
    template = template_env.get_template( 'home.jinja' )
    return template.render( template_vars )

@app.route('/data')
@return_json
def data():
    cur = get_cursor()
    cur.execute("SELECT * FROM readings WHERE timestamp > datetime('now' , '-7 days');")
    return [{k:row[k] for k in row.keys()} for row in cur.fetchall()]

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
