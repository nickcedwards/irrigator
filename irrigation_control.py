from datetime import datetime
import gpiozero
import platform
from config import Actions, get_cursor, PUMP_PIN, VALVE_PIN, Frequencies

if platform.system() == 'Windows':
    # For Windows we use a Mock pin factory that just does what we tell it
    from gpiozero.pins.mock import MockFactory
    gpiozero.Device.pin_factory = MockFactory()

pump = gpiozero.OutputDevice(PUMP_PIN)
valve = gpiozero.OutputDevice(VALVE_PIN)

def check_and_update():
    # Determine if the pump should be on or off
    run_irrigation = False
    if run_irrigation:
        irrigation_on()
    else:
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
    pump.on()
    valve.on() 

def irrigation_off():
    pump.off()
    valve.off()