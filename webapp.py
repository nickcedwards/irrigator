import sqlite3
import config
from flask import Flask, jsonify
from functools import wraps
import jinja2

templateLoader = jinja2.FileSystemLoader( searchpath="." )
templateEnv = jinja2.Environment( loader=templateLoader )

app = Flask(__name__)

def get_cursor():
    con = sqlite3.connect(config.DB)
    con.row_factory = sqlite3.Row
    return con.cursor()

def return_json(func):
    @wraps(func)
    def wrap():
        response = jsonify(func())
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    return wrap

@app.route('/')
def main():
    cur = get_cursor()
    cur.execute("SELECT * FROM readings ORDER BY timestamp DESC LIMIT 1")
    result = cur.fetchone()
    templateVars = {"timestamp":"", "vbat": -1, "temperature": -1, "humidity": -1}
    if result is not None:
        templateVars = { k:result[k] for k in result.keys() }
    template = templateEnv.get_template( 'home.jinja' )
    return template.render( templateVars )

@app.route('/data')
@return_json
def data():
    cur = get_cursor()
    cur.execute("SELECT * FROM readings WHERE timestamp > datetime('now' , '-7 days');")
    return [{k:row[k] for k in row.keys()} for row in cur.fetchall()]

@app.route('/status')
@return_json
def status():
    cur = get_cursor()
    cur.execute("SELECT * FROM status")
    row = cur.fetchone()
    if row is None:
        return []
    return {k:row[k] for k in row.keys()}

@app.route('/settings')
@return_json
def settings():
    cur = get_cursor()
    cur.execute("SELECT * FROM settings")
    row = cur.fetchone()
    if row is None:
        return []
    return {k:row[k] for k in row.keys()}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
