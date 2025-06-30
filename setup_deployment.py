#!/usr/bin/env python3
"""
Setup script for automatic deployment to Fly.io.
This script helps configure your project for automatic deployment.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} successful!")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} failed!")
            print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} failed with exception: {e}")
        return False

def check_flyctl():
    """Check if flyctl is installed."""
    return run_command("flyctl version", "Checking flyctl installation")

def login_flyctl():
    """Login to Fly.io."""
    return run_command("flyctl auth login", "Logging into Fly.io")

def get_auth_token():
    """Get Fly.io auth token."""
    print("🔄 Getting Fly.io auth token...")
    try:
        result = subprocess.run("flyctl auth token", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            token = result.stdout.strip()
            print("✅ Auth token retrieved!")
            print(f"\n🔑 Your Fly.io API Token:")
            print(f"   {token}")
            print(f"\n📋 IMPORTANT - Add this to GitHub:")
            print(f"   1. Go to: https://github.com/YOUR_USERNAME/YOUR_REPO/settings/secrets/actions")
            print(f"   2. Click 'New repository secret'")
            print(f"   3. Name: FLY_API_TOKEN")
            print(f"   4. Value: {token}")
            print(f"   5. Click 'Add secret'")
            print(f"\n⚠️  Keep this token secure and don't share it publicly!")
            
            # Copy to clipboard if possible
            try:
                import pyperclip
                pyperclip.copy(token)
                print(f"📋 Token copied to clipboard!")
            except ImportError:
                print(f"💡 Tip: Install 'pyperclip' to auto-copy tokens to clipboard")
            
            return True
        else:
            print(f"❌ Failed to get auth token: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ Failed to get auth token: {e}")
        return False

def launch_app():
    """Launch the app on Fly.io."""
    if os.path.exists("fly.toml"):
        print("📋 fly.toml already exists. Skipping launch.")
        return True
    
    print("🔄 Launching app on Fly.io...")
    print("   Please follow the prompts to configure your app.")
    try:
        result = subprocess.run("flyctl launch", shell=True)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Failed to launch app: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 Bytecode Interpreter - Automatic Deployment Setup")
    print("=" * 55)
    
    # Check if flyctl is installed
    if not check_flyctl():
        print("\n❌ flyctl is not installed or not in PATH.")
        print("   Please install it from: https://fly.io/docs/hands-on/install-flyctl/")
        sys.exit(1)
    
    # Login to Fly.io
    if not login_flyctl():
        print("\n❌ Failed to login to Fly.io.")
        print("   Please try running 'flyctl auth login' manually.")
        sys.exit(1)
    
    # Launch app (if not already launched)
    if not launch_app():
        print("\n❌ Failed to launch app on Fly.io.")
        print("   Please try running 'flyctl launch' manually.")
        sys.exit(1)
    
    # Get auth token
    if not get_auth_token():
        print("\n❌ Failed to get auth token.")
        print("   Please try running 'flyctl auth token' manually.")
        sys.exit(1)
    
    print("\n🎉 Setup complete!")
    print("\n📋 Summary:")
    print("   ✅ flyctl is installed and working")
    print("   ✅ Logged into Fly.io")
    print("   ✅ App launched on Fly.io")
    print("   ✅ Auth token retrieved")
    print("\n🔧 Next steps:")
    print("   1. Add FLY_API_TOKEN to your GitHub repository secrets")
    print("   2. Commit your changes to the main branch")
    print("   3. Watch GitHub Actions automatically deploy your app!")
    print("\n📖 For detailed instructions, see DEPLOYMENT_AUTOMATION.md")

if __name__ == "__main__":
    main()
