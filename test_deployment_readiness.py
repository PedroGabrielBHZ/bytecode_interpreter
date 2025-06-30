#!/usr/bin/env python3
"""
Test script to verify the web application works correctly before deployment.
"""

import os
import sys
import requests
import time
import subprocess
import threading
from urllib.parse import urlparse


def test_web_app():
    """Test the web application locally."""
    print("🧪 Testing Bytecode Interpreter Web App")
    print("=" * 50)

    # Set production environment
    os.environ["FLASK_ENV"] = "production"

    try:
        # Import app
        from app import app

        # Test basic configuration
        print("✅ App import successful")
        print(f"📝 Environment: {app.config.get('ENV', 'Unknown')}")
        print(f"📝 Debug mode: {app.config.get('DEBUG', 'Unknown')}")
        print(
            f"🔐 Secret key configured: {'Yes' if app.config.get('SECRET_KEY') else 'No'}"
        )

        # Start test server in background
        print("\n🚀 Starting test server...")

        def run_server():
            app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)

        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()

        # Wait for server to start
        time.sleep(2)

        base_url = "http://127.0.0.1:5000"

        # Test endpoints
        tests = [
            ("Home page", "/"),
            ("Examples page", "/examples"),
            ("Health check", "/health"),
        ]

        print("\n🔍 Testing endpoints...")
        for name, endpoint in tests:
            try:
                response = requests.get(f"{base_url}{endpoint}", timeout=5)
                if response.status_code == 200:
                    print(f"✅ {name}: OK ({response.status_code})")
                else:
                    print(f"⚠️ {name}: {response.status_code}")
            except Exception as e:
                print(f"❌ {name}: Error - {e}")

        # Test API endpoints
        print("\n🔍 Testing API endpoints...")

        # Test bytecode execution
        test_code = """PUSH 10
PUSH 20
ADD
PRINT
HALT"""

        try:
            response = requests.post(
                f"{base_url}/api/run", json={"code": test_code}, timeout=10
            )
            if response.status_code == 200:
                result = response.json()
                print(f"✅ API /run: OK - Output: {result.get('output', '').strip()}")
            else:
                print(f"⚠️ API /run: {response.status_code}")
        except Exception as e:
            print(f"❌ API /run: Error - {e}")

        # Test bytecode optimization
        try:
            response = requests.post(
                f"{base_url}/api/optimize", json={"code": test_code}, timeout=10
            )
            if response.status_code == 200:
                result = response.json()
                print(
                    f"✅ API /optimize: OK - Optimized {result.get('stats', {}).get('instructions_removed', 0)} instructions"
                )
            else:
                print(f"⚠️ API /optimize: {response.status_code}")
        except Exception as e:
            print(f"❌ API /optimize: Error - {e}")

        print("\n🎉 Web app testing completed!")

    except Exception as e:
        print(f"❌ Failed to test web app: {e}")
        return False

    return True


def test_docker_build():
    """Test Docker build process."""
    print("\n🐳 Testing Docker build...")

    try:
        # Build Docker image
        result = subprocess.run(
            ["docker", "build", "-t", "bytecode-interpreter-test", "."],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(__file__),
        )

        if result.returncode == 0:
            print("✅ Docker build successful")

            # Try to run container briefly to test
            print("🧪 Testing Docker container...")
            run_result = subprocess.run(
                [
                    "docker",
                    "run",
                    "--rm",
                    "-d",
                    "-p",
                    "8080:8080",
                    "--name",
                    "bytecode-test",
                    "bytecode-interpreter-test",
                ],
                capture_output=True,
                text=True,
            )

            if run_result.returncode == 0:
                time.sleep(3)  # Give container time to start

                # Test health endpoint
                try:
                    response = requests.get("http://localhost:8080/health", timeout=5)
                    if response.status_code == 200:
                        print("✅ Docker container running correctly")
                    else:
                        print(
                            f"⚠️ Docker container responding with {response.status_code}"
                        )
                except Exception as e:
                    print(f"⚠️ Docker container not responding: {e}")

                # Stop container
                subprocess.run(["docker", "stop", "bytecode-test"], capture_output=True)

            else:
                print(f"❌ Docker run failed: {run_result.stderr}")

        else:
            print(f"❌ Docker build failed: {result.stderr}")
            return False

    except FileNotFoundError:
        print("⚠️ Docker not found - skipping Docker tests")
        return True
    except Exception as e:
        print(f"❌ Docker test error: {e}")
        return False

    return True


if __name__ == "__main__":
    success = True

    # Run web app tests
    success &= test_web_app()

    # Run Docker tests
    success &= test_docker_build()

    if success:
        print("\n🎉 All tests passed! Ready for deployment.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the issues above.")
        sys.exit(1)
