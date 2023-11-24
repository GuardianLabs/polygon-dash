from pony.orm import db_session


@db_session
def upgrade_from_v1(db):
    # Create a cursor object
    conn = db.get_connection()
    cur = db.get_connection().cursor()

    cur.execute("BEGIN;")
    cur.execute("""
        ALTER TABLE block
        ALTER COLUMN timestamp
        TYPE bigint USING timestamp::bigint;
    """)

    cur.execute("""
        ALTER TABLE blockdelta
        ALTER COLUMN block_time
        TYPE bigint USING block_time::bigint;
    """)

    cur.execute("""
        ALTER TABLE transaction
        DROP COLUMN created;
    """)

    cur.execute("""
        ALTER TABLE transaction
        ADD COLUMN first_seen_ts BIGINT;
    """)

    cur.execute("""
        ALTER TABLE transaction
        ADD COLUMN finalized_ts BIGINT;
    """)

    cur.execute("""
        CREATE TABLE auxillarydata(
        key TEXT PRIMARY KEY,
        value TEXT
        ); 
    """)

    cur.execute("""
        INSERT INTO auxillarydata(key, value) 
        VALUES ('dbVersion', '20'), ('network', 'polygon'); 
    """)

    conn.commit()

    # Close cursor and connection
    cur.close()
