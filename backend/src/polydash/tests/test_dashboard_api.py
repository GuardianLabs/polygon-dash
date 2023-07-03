import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pony.orm import db_session

from polydash.db import db
from polydash.model.risk import MinerRisk
from polydash.routers.dashboard import router


@pytest.fixture()
def mock_db(tmp_path):
    # ACTHUNG! We must use real file (no :memory:) here,
    # because FastAPI testing does not work otherwise (threads-related stuff)
    db.bind(provider='sqlite', filename=str(tmp_path / "test.db"), create_db=True)
    db.generate_mapping(create_tables=True)


@pytest.fixture()
def client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app=app)


def test_complete_init_with_default_values(mock_db, client):
    MinerRisk.add_datapoint("abc", 20)
    MinerRisk.add_datapoint("ebf", 30)
    MinerRisk.add_datapoint("ebf", 15)
    MinerRisk.add_datapoint("abc", 20)
    MinerRisk.add_datapoint("abc", 20)
    MinerRisk.add_datapoint("foo", 20)
    response = client.get("/dash/miners")
    assert response.status_code == 200
    assert response.json()['total'] == 3
    # assert response.json() == result

    response = client.get("/dash/miners?order_by=rank&sort_order=asc")
    assert [x['rank'] for x in response.json()['data']] == list(range(3))

    response = client.get("/dash/miners?order_by=rank&sort_order=desc")
    assert [x['rank'] for x in response.json()['data']] == list(reversed(range(3)))

    # Risk score increasing -> rank (standing) increasing
    response = client.get("/dash/miners?order_by=score&sort_order=asc")
    print(response.json())
    assert [x['rank'] for x in response.json()['data']] == list(range(3))

    response = client.get("/dash/miners?order_by=score&sort_order=desc")
    assert [x['rank'] for x in response.json()['data']] == list(reversed(range(3)))
