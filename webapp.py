import sqlite3
import config
from flask import Flask
import jinja2

templateLoader = jinja2.FileSystemLoader( searchpath="." )
templateEnv = jinja2.Environment( loader=templateLoader )

app = Flask(__name__)

def get_latest():
    con = sqlite3.connect(config.DB)
    cur = con.cursor()
    cur.execute("SELECT * FROM readings ORDER BY timestamp DESC LIMIT 1")
    #return repr(cur.fetchone())

    templateVars = { "title" : "Test Example",
                    "description" : "A simple inquiry of function." }

    template = templateEnv.get_template( 'home.jinja' )
    return template.render( templateVars )


@app.route('/')
def hello_world():
    return get_latest()

if __name__ == '__main__':
    app.run()
