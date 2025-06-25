#!/usr/bin/env python3
"""
Git Workflow Setup Script for Dev and Prod Branches
"""

import subprocess
import sys
import os

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

def check_git_status():
    """Check if we're in a git repository"""
    result = run_command("git status", "Checking git status")
    return result is not None

def get_current_branch():
    """Get current branch name"""
    result = run_command("git branch --show-current", "Getting current branch")
    return result

def setup_dev_prod_workflow():
    """Set up dev and prod branches"""
    print("🚀 Setting up Dev and Prod Git Workflow")
    print("=" * 50)
    
    # Check if we're in a git repo
    if not check_git_status():
        print("❌ Not in a git repository. Please run this from your project root.")
        return False
    
    current_branch = get_current_branch()
    print(f"📍 Current branch: {current_branch}")
    
    # Check if branches already exist
    branches = run_command("git branch -a", "Checking existing branches")
    has_dev = branches and "dev" in branches
    has_prod = branches and "prod" in branches
    
    print(f"📋 Existing branches - dev: {has_dev}, prod: {has_prod}")
    
    # Create dev branch if it doesn't exist
    if not has_dev:
        print("\n🌿 Creating dev branch...")
        run_command("git checkout -b dev", "Creating dev branch")
        run_command("git push -u origin dev", "Pushing dev branch to remote")
    else:
        print("✅ dev branch already exists")
    
    # Create prod branch if it doesn't exist
    if not has_prod:
        print("\n🚀 Creating prod branch...")
        run_command("git checkout -b prod", "Creating prod branch")
        run_command("git push -u origin prod", "Pushing prod branch to remote")
    else:
        print("✅ prod branch already exists")
    
    # Switch back to dev for development
    run_command("git checkout dev", "Switching to dev branch")
    
    print("\n🎉 Git workflow setup complete!")
    print("\n📋 Next steps:")
    print("1. Set 'prod' as default branch on GitHub/GitLab (optional)")
    print("2. Set up branch protection for 'prod' (recommended)")
    print("3. Configure Railway to deploy from 'prod' branch")
    print("4. Start developing on 'dev' branch")
    
    return True

def show_workflow_commands():
    """Show common workflow commands"""
    print("\n📚 Common Workflow Commands:")
    print("=" * 40)
    
    commands = [
        ("Development", [
            "git checkout dev",
            "git pull origin dev",
            "# ... make changes ...",
            "git add .",
            "git commit -m 'feat: add new feature'",
            "git push origin dev"
        ]),
        ("Production Deployment", [
            "git checkout prod",
            "git pull origin prod",
            "git merge dev",
            "git push origin prod"
        ]),
        ("Feature Branch (Optional)", [
            "git checkout dev",
            "git checkout -b feature/new-feature",
            "# ... make changes ...",
            "git push origin feature/new-feature",
            "# Create PR: feature/new-feature → dev"
        ])
    ]
    
    for title, cmds in commands:
        print(f"\n🔧 {title}:")
        for cmd in cmds:
            print(f"   {cmd}")

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--commands":
        show_workflow_commands()
        return
    
    success = setup_dev_prod_workflow()
    if success:
        show_workflow_commands()

if __name__ == "__main__":
    main() 