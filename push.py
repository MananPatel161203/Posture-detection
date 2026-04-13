import subprocess
import sys

def run_command(command):
    """Runs a shell command and prints the output."""
    try:
        # Run the command and capture the output
        result = subprocess.run(command, check=True, text=True, shell=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running command: {command}")
        print(e.stderr)
        sys.exit(1)

def git_push():
    # Ask the user for a commit message
    commit_message = input("Enter your commit message: ")
    
    if not commit_message.strip():
        print("❌ Commit message cannot be empty. Aborting.")
        sys.exit(1)

    print("\n📦 Staging files...")
    run_command("git add .")
    
    print(f"📝 Committing with message: '{commit_message}'...")
    run_command(f'git commit -m "{commit_message}"')
    
    print("🚀 Pushing to GitHub...")
    run_command("git push -u origin main")
    
    print("✅ Successfully pushed to GitHub!")

if __name__ == "__main__":
    git_push()