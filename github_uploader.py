import os
import subprocess
from datetime import datetime
from pathlib import Path
import time

class GitHubAutoUploader:
    def __init__(self, repo_path, files_directory, github_token=None):
        """
        Initialize the GitHub Auto Uploader
        
        Args:
            repo_path: Path to your local git repository
            files_directory: Directory containing files to upload
            github_token: Optional GitHub personal access token
        """
        self.repo_path = Path(repo_path)
        self.files_dir = Path(files_directory)
        self.uploaded_log = self.repo_path / '.uploaded_files.log'
        self.github_token = github_token
        
    def get_uploaded_files(self):
        """Get list of already uploaded files"""
        if self.uploaded_log.exists():
            with open(self.uploaded_log, 'r') as f:
                return set(line.strip() for line in f)
        return set()
    
    def mark_as_uploaded(self, filename):
        """Mark a file as uploaded"""
        with open(self.uploaded_log, 'a') as f:
            f.write(f"{filename}\n")
    
    def get_next_file(self):
        """Get the next file to upload"""
        uploaded = self.get_uploaded_files()
        
        # Get all files from directory
        all_files = []
        for file_path in self.files_dir.rglob('*'):
            if file_path.is_file():
                rel_path = file_path.relative_to(self.files_dir)
                if str(rel_path) not in uploaded:
                    all_files.append(file_path)
        
        # Sort to maintain consistent order
        all_files.sort()
        return all_files[0] if all_files else None
    
    def git_command(self, *args):
        """Execute a git command"""
        cmd = ['git', '-C', str(self.repo_path)] + list(args)
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Git command failed: {result.stderr}")
        return result.stdout
    
    def upload_file(self, file_path):
        """Upload a single file to GitHub"""
        try:
            # Copy file to repo
            rel_path = file_path.relative_to(self.files_dir)
            dest_path = self.repo_path / rel_path
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy the file
            import shutil
            shutil.copy2(file_path, dest_path)
            
            # Git operations
            self.git_command('add', str(rel_path))
            
            commit_msg = f"Add {rel_path.name} - {datetime.now().strftime('%Y-%m-%d')}"
            self.git_command('commit', '-m', commit_msg)
            
            # Push to remote
            self.git_command('push', 'origin', 'main')
            
            # Mark as uploaded
            self.mark_as_uploaded(str(rel_path))
            
            print(f"✓ Successfully uploaded: {rel_path}")
            return True
            
        except Exception as e:
            print(f"✗ Error uploading {file_path}: {str(e)}")
            return False
    
    def run_daily_upload(self):
        """Run the daily upload task"""
        print(f"\n{'='*50}")
        print(f"GitHub Auto Uploader - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}\n")
        
        next_file = self.get_next_file()
        
        if next_file:
            print(f"Uploading: {next_file.name}")
            self.upload_file(next_file)
        else:
            print("No more files to upload!")
        
        print(f"\n{'='*50}\n")


# Example usage
if __name__ == "__main__":
    # Configuration
    REPO_PATH = "/path/to/your/repo"  # Your local git repo path
    FILES_DIRECTORY = "/path/to/your/old/files"  # Directory with files to upload
    GITHUB_TOKEN = None  # Optional: your GitHub token
    
    # Create uploader instance
    uploader = GitHubAutoUploader(REPO_PATH, FILES_DIRECTORY, GITHUB_TOKEN)
    
    # Run daily upload
    uploader.run_daily_upload()