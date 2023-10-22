import pytest
from fastapi.testclient import TestClient
from main import app
import docker
import os


@pytest.fixture(scope="module", autouse=True)
def start_mongodb_container():
    client = docker.from_env()
    client.volumes.create("mongodb")
    script_path = os.path.abspath("./mongodb_init_testdata.js")
    container = client.containers.run(
        "mongo",
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
            "mongodb": {
                "bind": "/data/db",
                "mode": "rw"
            }
        }
    )

    yield

    container.stop()
    container.remove()
    client.volumes.get("mongodb").remove(force=True)

@pytest.fixture(scope="module")
def test_client():
    client = TestClient(app)
    yield client

def test_home_route(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert "<title>Monsters</title>" in response.text

def test_get_monsters(test_client):
    response = test_client.get("/api/monsters?name=scorpion")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_monster(test_client):
    response = test_client.get("/api/monster/1001")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "image_url" in data

def test_get_nonexistent_monster(test_client):
    response = test_client.get("/api/monster/9999999999")
    assert response.status_code == 404
    data = response.json()
    assert 'error' in data
