import sqlite3
import config
from flask import Flask
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
def hello_world():
    return get_latest()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
