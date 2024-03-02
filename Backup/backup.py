import os
import shutil
from datetime import datetime

def create_backup_folder():
    # Create /backups directory if it doesn't exist
    backup_dir = '/backups'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    return backup_dir

def copy_to_backup(files):
    backup_dir = create_backup_folder()
    # Create a folder with current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_folder = os.path.join(backup_dir, timestamp)
    os.makedirs(backup_folder)

    # Copy files or directories into the backup folder
    for file_path in files:
        if os.path.exists(file_path):
            if os.path.isdir(file_path):
                shutil.copytree(file_path, os.path.join(backup_folder, os.path.basename(file_path)))
            else:
                shutil.copy(file_path, backup_folder)
        else:
            print(f"File {file_path} does not exist.")

if __name__ == "__main__":
    files_and_dirs_to_backup = [
        "/etc/passwd",
        "/etc/shadow",
        "/etc/group",
        "/etc/sudoers",
        "/etc/hosts.allow",
        "/etc/hosts.deny",
        "/etc/fstab",
        "/etc/ssh/sshd_config",
        "/etc/sysctl.conf",
        "/etc/security",
        # Add any additional file paths here
    ]
    
    copy_to_backup(files_and_dirs_to_backup)