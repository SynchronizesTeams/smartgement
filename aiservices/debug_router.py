import sys
import os
sys.path.append(os.getcwd())

print("Importing app.routers.products...", flush=True)
try:
    from app.routers import products
    print("Import successful", flush=True)
except Exception as e:
    print(f"Import failed: {e}", flush=True)
    import traceback
    traceback.print_exc()
