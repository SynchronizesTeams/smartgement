import sys
import os

# Add current directory to sys.path
sys.path.append(os.getcwd())

modules = [
    "app.schemas.product",
    "app.routers.products",
    "app.routers.trends",
    "app.routers.risk",
    "app.routers.chatbot",
    "app.routers.embeddings",
    "app.routers.collections",
    "app.routers.ai_generate",
    "app.main"
]

for module in modules:
    print(f"Importing {module}...", flush=True)
    try:
        __import__(module)
        print(f"{module} imported successfully.", flush=True)
    except Exception as e:
        print(f"Error importing {module}: {e}", flush=True)
        # Print traceback
        import traceback
        traceback.print_exc()
        break
