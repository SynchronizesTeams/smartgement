import os
import sys
from fastapi.testclient import TestClient

# Add current directory to sys.path
sys.path.append(os.getcwd())

print("Attempting to import app.main...")
try:
    from app.main import app
    print("app.main imported successfully.")
    
    client = TestClient(app)
    print("Attempting to fetch /docs...")
    response = client.get("/docs")
    print(f"Response status code: {response.status_code}")
    if response.status_code == 200:
        print("/docs is accessible.")
    else:
        print(f"/docs returned {response.status_code}")
        print(response.text[:500])

except Exception as e:
    print(f"Error during import or execution: {e}")
    import traceback
    traceback.print_exc()
