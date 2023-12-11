from pony.orm import db_session


@db_session
def upgrade_from_v2(db):
    # Create a cursor object
    conn = db.get_connection()
    cur = db.get_connection().cursor()

    cur.execute("BEGIN;")
    cur.execute("""
        CREATE TABLE peer(
            id SERIAL PRIMARY KEY,
            peer_id TEXT UNIQUE NOT NULL
        );
    """)
    
    cur.execute("""
        INSERT INTO Peer (peer_id)
        SELECT DISTINCT peer_id FROM tx_summary
        UNION
        SELECT DISTINCT peer FROM block_fetched;
    """)

    cur.execute("""
        ALTER TABLE tx_summary
        ADD COLUMN peer_id_temp INTEGER;
    """)

    cur.execute("""
        ALTER TABLE block_fetched
        ADD COLUMN peer_temp INTEGER;
    """)

   
    cur.execute("""
        UPDATE tx_summary SET peer_id_temp = (
        SELECT id FROM Peer 
        WHERE Peer.peer_id = tx_summary.peer_id);
    """)
    
    
    
    cur.execute("""
    ALTER TABLE tx_summary
    DROP COLUMN peer_id;
    """)
    cur.execute("""
    ALTER TABLE tx_summary RENAME COLUMN peer_id_temp TO peer;
    """)
    cur.execute("""
    ALTER TABLE tx_summary ADD PRIMARY KEY (tx_hash, peer, tx_first_seen);
    """)
    
    cur.execute("""
    ALTER TABLE tx_summary ADD CONSTRAINT fk_peer_id FOREIGN KEY (peer) REFERENCES Peer(id);
    """)

    

    
    cur.execute("""
        UPDATE block_fetched SET peer_temp = (
        SELECT id FROM Peer 
        WHERE Peer.peer_id = block_fetched.peer);            
    """)
    cur.execute("""
        ALTER TABLE block_fetched DROP COLUMN peer;
    """)
    cur.execute("""
        ALTER TABLE block_fetched RENAME COLUMN peer_temp TO peer;
    """)
    cur.execute("""
        ALTER TABLE block_fetched ADD CONSTRAINT fk_peer FOREIGN KEY (peer) REFERENCES Peer(id);
    """)
    
    
    conn.commit()

    # Close cursor and connection
    cur.close()
