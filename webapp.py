import sqlite3
import config
from flask import Flask, jsonify
import jinja2

templateLoader = jinja2.FileSystemLoader( searchpath="." )
templateEnv = jinja2.Environment( loader=templateLoader )

app = Flask(__name__)

def get_latest():
    con = sqlite3.connect(config.DB)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM readings ORDER BY timestamp DESC LIMIT 1")
    result = cur.fetchone()
    templateVars = { k:result[k] for k in result.keys() }
    template = templateEnv.get_template( 'home.jinja' )
    return template.render( templateVars )


@app.route('/')
def main():
    return get_latest()

@app.route('/data')
def data():
    con = sqlite3.connect(config.DB)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM readings WHERE timestamp > datetime('now' , '-7 days');")
    result = [{k:row[k] for k in row.keys()} for row in cur.fetchall()]
    response = jsonify(result)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
