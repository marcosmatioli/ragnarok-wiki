import pytest
from fastapi.testclient import TestClient
from main import app
import docker
import os


@pytest.fixture(scope="module", autouse=True)
def start_mongodb_container():
    client = docker.from_env()
    script_path = os.path.abspath("./mongodb_init_testdata.js")
    container = client.containers.run(
        "mongo:latest",
        name="mongo",
        detach=True,
        ports={"27017": ('0.0.0.0', 27017)},
        environment={
            "MONGO_INITDB_ROOT_USERNAME": "root",
            "MONGO_INITDB_ROOT_PASSWORD": "changeme"
        },
        volumes={
            script_path: {
                "bind": "/docker-entrypoint-initdb.d/mongo-init.js",
                "mode": "ro"
            },
            "mongodb_data": {
                "bind": "/data/db",
                "mode": "rw"
            },
            "mongodb_config": {
                "bind": "/data/configdb",
                "mode": "rw"
            }
        }
    )

    yield

    container.stop()
    container.remove()
    client.volumes.get("mongodb_data").remove(force=True)
    client.volumes.get("mongodb_config").remove(force=True)

@pytest.fixture(scope="module")
def test_client():
    client = TestClient(app)
    yield client

def test_get_monsters(test_client):
    response = test_client.get("/api/monsters?name=esco")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2

    response = test_client.get("/api/monsters?name=rei")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1

def test_get_monster(test_client):
    response = test_client.get("/api/monster/1001")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "image_url" in data
    assert data["id"] == 1001

def test_get_nonexistent_monster(test_client):
    response = test_client.get("/api/monster/9999999999")
    assert response.status_code == 404
    data = response.json()
    assert 'error' in data

def test_get_monsters_per_page(test_client):
    for per_page in range(2):
        response = test_client.get(f"/api/monsters?per_page={per_page}")
        if per_page <= 0:
            # A 422 status code indicates that the server was unable to process
            # the request because it contains invalid data
            assert response.status_code == 422
        else:
            assert response.status_code == 200
            data = response.json()
            assert len(data) == per_page

def test_get_monsters_page(test_client):
    response = test_client.get("/api/monsters?per_page=1&page=1")
    assert response.status_code == 200
    data = response.json()
    assert data[0]['id'] == 1001

    response = test_client.get("/api/monsters?per_page=1&page=2")
    assert response.status_code == 200
    data = response.json()
    assert data[0]['id'] == 1168

    response = test_client.get("/api/monsters?per_page=1&page=0")
    assert response.status_code == 422

    response = test_client.get("/api/monsters?per_page=1&page=-1")
    assert response.status_code == 422

    response = test_client.get("/api/monsters?per_page=1&page=string")
    assert response.status_code == 422

def test_get_healthy(test_client):
    response = test_client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["healthy"] == "true"

def test_get_monsters_race(test_client):
    response = test_client.get("/api/monsters?race=human")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["stats"]["race"] == 7

    response = test_client.get("/api/monsters?race=human,insect")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[1]["stats"]["race"] == 7
    assert data[0]["stats"]["race"] == 4

    response = test_client.get("/api/monsters?race=inexistent")
    assert response.status_code == 422
    data = response.json()
    assert data["detail"] == "race not exist: inexistent"
