import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from py_api_framework.database import Base, get_db
from py_api_framework.main import app

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    """Setup test database before each test."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def auth_headers():
    """Create authenticated user and return headers."""
    # Register user
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    client.post("/api/v1/auth/register", json=user_data)
    
    # Login
    login_data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    login_response = client.post("/api/v1/auth/token", data=login_data)
    token = login_response.json()["access_token"]
    
    return {"Authorization": f"Bearer {token}"}

def test_create_item(auth_headers):
    """Test creating a new item."""
    item_data = {
        "title": "Test Item",
        "description": "This is a test item"
    }
    response = client.post("/api/v1/items/", json=item_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == item_data["title"]
    assert data["description"] == item_data["description"]
    assert "id" in data
    assert "owner_id" in data

def test_create_item_unauthorized():
    """Test creating item without authentication."""
    item_data = {
        "title": "Test Item",
        "description": "This is a test item"
    }
    response = client.post("/api/v1/items/", json=item_data)
    assert response.status_code == 401

def test_get_items(auth_headers):
    """Test getting list of items."""
    # Create some items first
    item_data = {
        "title": "Test Item 1",
        "description": "This is test item 1"
    }
    client.post("/api/v1/items/", json=item_data, headers=auth_headers)
    
    item_data2 = {
        "title": "Test Item 2",
        "description": "This is test item 2"
    }
    client.post("/api/v1/items/", json=item_data2, headers=auth_headers)
    
    # Get items
    response = client.get("/api/v1/items/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Test Item 1"
    assert data[1]["title"] == "Test Item 2"

def test_get_my_items(auth_headers):
    """Test getting current user's items."""
    # Create items
    item_data = {
        "title": "My Item",
        "description": "This is my item"
    }
    client.post("/api/v1/items/", json=item_data, headers=auth_headers)
    
    # Get my items
    response = client.get("/api/v1/items/my-items", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "My Item"

def test_get_item(auth_headers):
    """Test getting a specific item."""
    # Create item
    item_data = {
        "title": "Test Item",
        "description": "This is a test item"
    }
    create_response = client.post("/api/v1/items/", json=item_data, headers=auth_headers)
    item_id = create_response.json()["id"]
    
    # Get item
    response = client.get(f"/api/v1/items/{item_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["title"] == item_data["title"]

def test_get_item_not_found(auth_headers):
    """Test getting non-existent item."""
    response = client.get("/api/v1/items/999", headers=auth_headers)
    assert response.status_code == 404
    assert "Item not found" in response.json()["detail"]

def test_update_item(auth_headers):
    """Test updating an item."""
    # Create item
    item_data = {
        "title": "Original Title",
        "description": "Original description"
    }
    create_response = client.post("/api/v1/items/", json=item_data, headers=auth_headers)
    item_id = create_response.json()["id"]
    
    # Update item
    update_data = {
        "title": "Updated Title",
        "description": "Updated description"
    }
    response = client.put(f"/api/v1/items/{item_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]

def test_update_item_not_found(auth_headers):
    """Test updating non-existent item."""
    update_data = {
        "title": "Updated Title"
    }
    response = client.put("/api/v1/items/999", json=update_data, headers=auth_headers)
    assert response.status_code == 404
    assert "Item not found" in response.json()["detail"]

def test_delete_item(auth_headers):
    """Test deleting an item."""
    # Create item
    item_data = {
        "title": "Test Item",
        "description": "This is a test item"
    }
    create_response = client.post("/api/v1/items/", json=item_data, headers=auth_headers)
    item_id = create_response.json()["id"]
    
    # Delete item
    response = client.delete(f"/api/v1/items/{item_id}", headers=auth_headers)
    assert response.status_code == 200
    assert "Item deleted successfully" in response.json()["message"]
    
    # Verify item is deleted
    get_response = client.get(f"/api/v1/items/{item_id}", headers=auth_headers)
    assert get_response.status_code == 404

def test_delete_item_not_found(auth_headers):
    """Test deleting non-existent item."""
    response = client.delete("/api/v1/items/999", headers=auth_headers)
    assert response.status_code == 404
    assert "Item not found" in response.json()["detail"]

def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data
    assert data["version"] == "0.1.0"

def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "docs" in data 