from datetime import datetime, timedelta
import gpiozero
import platform
from config import INTERVALS, Actions, get_cursor, PUMP_PIN, VALVE_PIN, Frequencies

if platform.system() == 'Windows':
    # For Windows we use a Mock pin factory that just does what we tell it
    from gpiozero.pins.mock import MockFactory
    gpiozero.Device.pin_factory = MockFactory()

pump = gpiozero.OutputDevice(PUMP_PIN)
valve = gpiozero.OutputDevice(VALVE_PIN)

def check_and_update():
    # Determine if the pump should be on or off
    cur = get_cursor()

    status_query = "SELECT * FROM status WHERE id = 0"
    cur.execute(status_query)
    row = cur.fetchone()
    action = row['next_action']
    try:
        at = datetime.fromisoformat(row['next_action_at'])
    except ValueError:
        at = datetime.now()

    settings_query = "SELECT * FROM settings WHERE id = 0"
    cur.execute(settings_query)
    row = cur.fetchone()
    frequency = row['frequency']
    runtime = row['runtime']

    run_irrigation = False
    new_action = None
    if action == Actions.TurnOff.value:
        if at > datetime.now():
            run_irrigation = True
        else:
            run_irrigation = False
            if not frequency in (Frequencies.Off.value, Frequencies.Once.value):
                new_action = Actions.TurnOn.value
                next_action_at = datetime.now() + timedelta(hours=INTERVALS[frequency])
            else:
                new_action = Actions.Nothing.value
                next_action_at = datetime.now()
    elif action == Actions.TurnOn.value and frequency != Frequencies.Off.value:
        if at <= datetime.now():
            run_irrigation = True
            new_action = Actions.TurnOff.value
            next_action_at = datetime.now() + timedelta(minutes=runtime)

    if new_action:
        print(f"{datetime.now()}: Updating action to {new_action} at {next_action_at}")
        update_query = "UPDATE status SET next_action = ?, next_action_at = ? WHERE id = 0"
        cur.execute(update_query, (new_action, next_action_at))
        cur.connection.commit()

    if run_irrigation:
        if not pump.is_active or not valve.is_active:
            irrigation_on()
    else:
        if pump.is_active or valve.is_active:
            irrigation_off()
    
def sync_from_settings():
    query = "SELECT frequency, runtime, first_occurence FROM settings ORDER BY id DESC LIMIT 1"
    cur = get_cursor()
    cur.execute(query)
    row = cur.fetchone()
    frequency = row['frequency']
    next_action_at = row['first_occurence']
    if frequency == Frequencies.Off.value:
        action = Actions.TurnOff.value
        next_action_at = datetime.now().isoformat()
    else:
        action = Actions.TurnOn.value
    update_query = "UPDATE status SET next_action = ?, next_action_at = ? WHERE id = 0"
    cur.execute(update_query, (action, next_action_at))
    cur.connection.commit()
    cur.close()

def irrigation_on():
    print(f"{datetime.now()}: Turning on irrigation")
    pump.on()
    valve.on() 

def irrigation_off():
    print(f"{datetime.now()}: Turning off irrigation")
    pump.off()
    valve.off()