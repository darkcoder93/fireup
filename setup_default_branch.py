#!/usr/bin/env python3
"""
Script to set up prod branch as default branch
"""

import subprocess
import sys

def run_command(command, description):
    """Run a git command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Success")
            return result.stdout.strip()
        else:
            print(f"❌ {description} - Failed")
            print(f"Error: {result.stderr}")
            return None
    except Exception as e:
        print(f"❌ {description} - Exception: {e}")
        return None

def setup_prod_as_default():
    """Set up prod branch as default"""
    print("🚀 Setting up prod branch as default")
    print("=" * 50)
    
    # Check current branch
    current_branch = run_command("git branch --show-current", "Getting current branch")
    print(f"📍 Current branch: {current_branch}")
    
    # Check if prod branch exists
    branches = run_command("git branch -a", "Checking branches")
    has_prod = branches and "prod" in branches
    has_master = branches and "master" in branches
    has_main = branches and "main" in branches
    
    print(f"📋 Branches - prod: {has_prod}, master: {has_master}, main: {has_main}")
    
    if not has_prod:
        print("❌ prod branch doesn't exist. Create it first:")
        print("   git checkout -b prod")
        print("   git push -u origin prod")
        return False
    
    # Switch to prod branch
    run_command("git checkout prod", "Switching to prod branch")
    
    # Push prod branch if not already pushed
    run_command("git push -u origin prod", "Pushing prod branch")
    
    print("\n📋 Next steps to complete setup:")
    print("1. Go to your GitHub/GitLab repository")
    print("2. Navigate to Settings → Repository")
    print("3. Set 'prod' as the default branch")
    print("4. Delete 'master' or 'main' branch if desired")
    
    print("\n🔧 Manual commands if needed:")
    print("   # Delete master branch locally (if exists)")
    print("   git branch -d master")
    print("   git push origin --delete master")
    print("")
    print("   # Delete main branch locally (if exists)")
    print("   git branch -d main")
    print("   git push origin --delete main")
    
    return True

def main():
    """Main function"""
    setup_prod_as_default()

if __name__ == "__main__":
    main() 