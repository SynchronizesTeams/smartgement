"""
Test if collections router can be imported
"""
try:
    from app.routers import collections
    print("✅ Collections router imported successfully")
    print(f"Router object: {collections.router}")
    print(f"Routes: {[route.path for route in collections.router.routes]}")
except Exception as e:
    print(f"❌ Error importing collections router: {e}")
    import traceback
    traceback.print_exc()

# Also test main app
try:
    from app.main import app
    print("\n✅ Main app imported successfully")
    routes = [route.path for route in app.routes]
    collections_routes = [r for r in routes if 'collections' in r]
    print(f"Collections routes in app: {collections_routes}")
    if not collections_routes:
        print("⚠️ WARNING: No collections routes found in app!")
except Exception as e:
    print(f"\n❌ Error importing main app: {e}")
    import traceback
    traceback.print_exc()
