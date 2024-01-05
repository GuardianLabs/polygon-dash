import queue
import threading
import traceback
import time

from pony import orm
from pony.orm import select

from polydash.common.log import LOGGER
from polydash.common.model import Block
from polydash.polygon.p2p_data.model import (
    TransactionPending,
    TRANSACTION_CONFIRMED,
    TRANSACTION_PENDING,
    TRANSACTION_TO_DELETE
)

FIFTEEN_MINUTES_IN_MS = 900000
FIVE_MINUTES_IN_MS = 300000
PendingTransactionQueue = queue.Queue()

class PolygonPendingTransactionsProcessor(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = LOGGER.getChild(self.__class__.__name__)
        
        
    def process_block(self, block: Block):
        with orm.db_session:
            tx_hashes = []
            for tx in block.transactions:
                tx_hashes.append(tx.hash)
            pending_txs = TransactionPending.select()
            time_now_in_ms = int(time.time() * 1000)
            for pending_tx in pending_txs:
                if pending_tx.tx_hash in tx_hashes:
                    pending_tx.status = TRANSACTION_CONFIRMED
                else:
                    if pending_tx.status == TRANSACTION_TO_DELETE:
                        pending_tx.delete()
                    elif pending_tx.status == TRANSACTION_PENDING and time_now_in_ms - pending_tx.tx_first_seen > FIVE_MINUTES_IN_MS:
                        pending_tx.status = TRANSACTION_TO_DELETE
                        


    def run(self):
        LOGGER.info("Starting Polygon pending txs thread...")
        while True:
            try:
                # get the block from some other thread
                block_number = PendingTransactionQueue.get()

                with orm.db_session:
                    block = Block.get(number=block_number)
                    self.process_block(block)

            except Exception as e:
                traceback.print_exc()
                self.logger.error(
                    "exception when deal with a pending transactions: {}".format(
                        str(e)
                    )
                )
