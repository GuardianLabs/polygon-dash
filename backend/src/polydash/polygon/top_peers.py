from fastapi import APIRouter
from pony.orm import desc, db_session

from polydash.miners_ratings.model import MinerRisk
from polydash.polygon.deanon.model import DeanonNodeByBlock, DeanonNodeByTx, PeerToIP

top_peers_router = router = APIRouter(
    prefix="/top-peers",
    tags=["W3Router"],
    responses={404: {"description": "Not found"}},
)


@db_session
def get_one_deanoned_peer(node, memorized_peer_ids: set[str]):
    # try to get possible peer IDs of the node using two tables
    deanoned_nodes = []
    for table in (DeanonNodeByBlock, DeanonNodeByTx):
        deanoned_nodes.extend(
            table.select(signer_key=node.pubkey)
            .order_by(desc(table.confidence)))
    if not deanoned_nodes:
        # we don't know peer ID of this node, moving on
        return None

    # try to get the peer ID of this node which we don't know yet
    final_deanoned_node = None
    for deanoned_node in deanoned_nodes:
        if deanoned_node.peer_id not in memorized_peer_ids:
            final_deanoned_node = deanoned_node
            memorized_peer_ids.add(final_deanoned_node.peer_id)
            break
    if final_deanoned_node is None:
        return None

    # now, try to get IP address of that node
    if not (node_ip := PeerToIP.select(peer_id=final_deanoned_node.peer_id)
            .order_by(desc(PeerToIP.id))
            .first()):
        # we don't know IP of this node, moving on
        return None
    return node_ip


@router.get("/")
async def get_top_peers(count: int = 10) -> list[str]:
    # Iterating over a list is fine every time, since it typically is very small...
    new_top_nodes = []
    memorized_peer_ids = set()
    with db_session:
        # build a new list, including the IP addresses
        for node in MinerRisk.select().order_by(desc(MinerRisk.risk)):
            node_ip = get_one_deanoned_peer(node, memorized_peer_ids)
            # we have found IP of that node, memorize it if it wasn't in the list before
            if not node_ip or node_ip.ip in new_top_nodes:
                continue

            new_top_nodes.append(node_ip.ip)
            # if we have gathered enough nodes information, finish
            if len(new_top_nodes) >= count:
                break
    return new_top_nodes
