#!/usr/bin/env python3
"""
Test script to verify Flask configuration is working correctly.
"""

import os
import sys

# Test different environments
environments = ["development", "production", "testing"]

for env in environments:
    print(f"\n=== Testing {env.upper()} environment ===")
    
    # Set environment
    os.environ["FLASK_ENV"] = env
    
    # Import and create app (fresh import each time)
    if "app" in sys.modules:
        del sys.modules["app"]
    if "config" in sys.modules:
        del sys.modules["config"]
    
    try:
        from app import app
        print(f"✅ App created successfully")
        print(f"📝 DEBUG: {app.config.get('DEBUG')}")
        print(f"📝 ENV: {app.config.get('ENV')}")
        print(f"🔐 SECRET_KEY present: {'Yes' if app.config.get('SECRET_KEY') else 'No'}")
        print(f"🔐 SECRET_KEY value: {app.config.get('SECRET_KEY')[:10]}..." if app.config.get('SECRET_KEY') else "None")
        
        # Test that sessions work (this is what causes the original error)
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['test'] = 'value'
            print(f"✅ Session test passed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

print(f"\n=== Environment Variables ===")
print(f"FLASK_ENV: {os.environ.get('FLASK_ENV', 'Not set')}")
print(f"SECRET_KEY: {'Set' if os.environ.get('SECRET_KEY') else 'Not set'}")
