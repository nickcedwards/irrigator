BEGIN TRANSACTION;

Create Table config(
    id INTEGER PRIMARY KEY CHECK (id = 0),
    vbat_r1 REAL,
    vbat_r2	REAL
);

Create Table readings(
    timestamp   TEXT,
    temperature	REAL,
    humidity    REAL,
    vbat_raw	REAL,
    vbat    	REAL
);

Create Table settings(
    id INTEGER PRIMARY KEY,
    frequency		  TEXT,
    first_occurence   TEXT,
    runtime			  INTEGER
);

INSERT into settings (id, frequency, first_occurence, runtime) VALUES (0, 'Off', 'Null', 0);

Create Table status(
    id INTEGER PRIMARY KEY CHECK (id = 0),
    pump  		    INTEGER,
    valve           INTEGER,
    next_action		TEXT,
    next_action_at	TEXT
);

INSERT INTO status (id, pump, valve, next_action, next_action_at) VALUES (0, -1, -1, 'none', 'none');

COMMIT