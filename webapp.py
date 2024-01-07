from flask import Flask, jsonify, request
from flask_apscheduler import APScheduler
from functools import wraps
from datetime import datetime, timedelta
import jinja2

from config import get_cursor
import irrigation_control

templateLoader = jinja2.FileSystemLoader( searchpath="." )
template_env = jinja2.Environment( loader=templateLoader )

app = Flask(__name__)

INTERVAL_TASK_ID = 'interval-task-id'
 
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

scheduler.add_job(id=INTERVAL_TASK_ID, func=irrigation_control.check_and_update, trigger='interval', seconds=20)
 

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


def next_occurrence(input_time):
    input_time = input_time[:5]
    t = datetime.strptime(input_time, "%H:%M").time()
    now = datetime.now()
    next_time = datetime.combine(now.date(), t)
    if next_time <= now:
        next_time += timedelta(days=1)
    return next_time.isoformat()

def handle_settings_post(request):
    fields = ['frequency', 'runtime', 'time']
    for f in fields:
        if not f in request.form:
            return False, f"Missing field {f}"
    first_occurence = next_occurrence(request.form['time'])
    cur = get_cursor()
    cur.execute("UPDATE settings SET frequency = ?, runtime = ?, first_occurence = ? WHERE id = 0", 
                (request.form['frequency'], request.form['runtime'], first_occurence))
    cur.connection.commit()
    cur.close()
    irrigation_control.sync_from_settings()
    return True, "Settings updated"

@app.route('/', methods=['GET', 'POST'])
def main():
    template_vars = {
        'vbat': -1,
        'temperature': -1,
        'humidity': -1,
        'post': False,
    }
    if request.method == 'POST':
        template_vars['post'] = True
        template_vars['post_valid'], template_vars['post_result'] = handle_settings_post(request)
    cur = get_cursor()
    add_single_row(cur, "SELECT * FROM readings ORDER BY timestamp DESC LIMIT 1", template_vars)
    add_single_row(cur, "SELECT * FROM status LIMIT 1", template_vars)
    add_single_row(cur, "SELECT frequency, runtime, TIME(first_occurence) as time FROM settings ORDER BY id DESC LIMIT 1", template_vars)
    template_vars['pump'] = irrigation_control.pump.is_active
    template_vars['valve'] = irrigation_control.valve.is_active
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
