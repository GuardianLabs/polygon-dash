from pony import orm
from pony.orm import PrimaryKey

from polydash.common.db import GetOrInsertMixin, db


class Peer(db.Entity, GetOrInsertMixin):
    id = orm.PrimaryKey(int, auto=True)
    peer_id = orm.Required(str, unique=True)
    transactions = orm.Set('TransactionP2P')
    blocks = orm.Set('BlockP2P')

class TransactionP2P(db.Entity, GetOrInsertMixin):
    _table_ = "tx_summary"
    tx_hash = orm.Required(str, index=True)
    peer = orm.Required(Peer)
    tx_first_seen = orm.Required(int, size=64)
    PrimaryKey(tx_hash, peer, tx_first_seen)
    time = orm.Optional(int, size=64)

    @classmethod
    def get_first_by_hash(cls, tx_hash):
        return cls.select().where(tx_hash=tx_hash).order_by(cls.tx_first_seen).first()


class BlockP2P(db.Entity):
    _table_ = "block_fetched"
    id = orm.PrimaryKey(int, auto=True)
    block_hash = orm.Required(str, index=True)
    block_number = orm.Optional(int, size=64)
    first_seen_ts = orm.Optional(int, size=64)
    peer = orm.Optional(Peer)
    peer_remote_addr = orm.Optional(str)
    peer_local_addr = orm.Optional(str)

    @classmethod
    def get_first_by_hash(cls, block_hash):
        return (
            cls.select()
            .where(block_hash=block_hash)
            .order_by(cls.first_seen_ts)
            .first()
        )


