BEGIN TRANSACTION;

Create Table config(
    vbat_r1     REAL,
	vbat_r2	    REAL
);


Create Table readings(
    timestamp   TEXT,
	temperature	REAL,
	humidity    REAL,
	vbat_raw	REAL,
	vbat    	REAL
);

COMMIT