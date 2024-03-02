import paramiko
import os
from dotenv import load_dotenv
from typing import Generator
from contextlib import contextmanager

class UnexpectedRemoteHostError(Exception):
    """Custom exception for representing errors generated on the remote server."""
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class UsefulStrings():
    """Grabs passwords from the env file, avoiding global variables"""    
    def __init__(self) -> None:
        load_dotenv()
        self.strongPassword1 = os.getenv('STRONG_PASSWORD_1')
        self.strongPassword2 = os.getenv('STRONG_PASSWORD_2')

@contextmanager
def ssh_connection(host_ip:str, username:str, password:str=None, path_to_priv_key:str=None) -> Generator[paramiko.SSHClient, None, None]:
    """Sets up an ssh context that will automatically close if an error occurs.

    Args:
        host_ip (str): the designated ip to connect to
        username (str): the username on the host
        password (str, optional): said user's password. Required unless path_to_priv_key is specified. Defaults to None.
        path_to_priv_key (str, optional): said user's local path to their private key. Required unless password is specified. Defaults to None.

    Raises:
        ValueError: Only specify a password or a private key, not both

    Yields:
        Generator[paramiko.SSHClient, None, None]: the ssh client session
    """    
    if (password is None and path_to_priv_key is None) or (password is not None and path_to_priv_key is not None):
        raise ValueError('Specify a private key OR a password')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host_ip, username=username, password=password)
        yield ssh
    finally:
        ssh.close()

@contextmanager
def sftp_connection(ssh:paramiko.SSHClient) -> Generator[paramiko.SFTPClient, None, None]:
    """Given that an ssh session has already been initialized, sets up a secure file
    transfer protocol session context. If an error occurs, the session will
    automatically close.

    Args:
        ssh (paramiko.SSHClient): the ssh client session

    Yields:
        Generator[paramiko.SFTPClient, None, None]: the sftp client session
    """    
    sftp = ssh.open_sftp()
    try:
        yield sftp
    finally:
        sftp.close()

def execute_command(ssh:paramiko.SSHClient, command:str, necessary_inputs:list[str]=None) -> tuple[str, str]:
    """Executes an unprivileged command on a remote host using an ssh session

    Args:
        ssh (paramiko.SSHClient): the ssh client session
        command (str): the command to be executed
        necessary_input (str, optional): any additions that need to be added after 
        the command is executed. Defaults to None.

    Returns:
        tuple[str, str]: output (empty if none) and errors (empty if none)
    """  
    stdin, stdout, stderr = ssh.exec_command(command)
    if necessary_inputs:
        for n_input in necessary_inputs:
            stdin.write(f'{n_input}\n')
            stdin.flush()
    output = stdout.read().decode()
    errors = stderr.read().decode()
    return output, errors

def execute_privileged_command(ssh:paramiko.SSHClient, command:str, sudo_password:str, necessary_inputs:list[str]=None) -> tuple[str, str]:
    """Executes an unprivileged command on a remote host using an ssh session

    Args:
        ssh (paramiko.SSHClient): the ssh client session
        command (str): the command to be executed
        sudo_password (str): the password of the sudoer on the remote host
        necessary_input (str, optional): any additions that need to be added after 
        the command is executed. Defaults to None.

    Returns:
        tuple[str, str]: output (empty if none) and errors (empty if none)
    """  
    stdin, stdout, stderr = ssh.exec_command(f"sudo -S -p '' {command}")
    stdin.write(f'{sudo_password}\n')
    stdin.flush()
    if necessary_inputs:
        for n_input in necessary_inputs:
            stdin.write(f'{n_input}\n')
            stdin.flush()
    output = stdout.read().decode()
    errors = stderr.read().decode()
    return output, errors

def add_user_if_necessary(ssh:paramiko.SSHClient, user_to_add:str, sudo_password:str) -> bool:
    """Adds a user to the remote host if they are not already added

    Args:
        ssh (paramiko.SSHClient): the ssh client session
        user_to_add (str): the name of the user in question
        sudo_password (str): the sudo password of the connected client

    Raises:
        UnexpectedRemoteHostError: Should the remote host not run as expected,
        this error with the error's message will be raised.

    Returns:
        bool: whether the user was added. If false, the remote host already had 
        the user
    """    
    # Check if the user is already added to the remote host
    id_command = f'id {user_to_add}'
    output, errors = execute_command(ssh, id_command)

    # If user already added to remote host, return false
    if not errors:
        return False
    
    # Otherwise, add the user, set password, give them a dir, and return true
    else:
        # Add the user
        command = f'useradd -m -s /bin/bash {user_to_add}'
        output, errors = execute_privileged_command(ssh, command, sudo_password)
        if errors:
            if 'already exists' not in errors:
                raise UnexpectedRemoteHostError(errors)

        # Set the user password
        reset_user_password(ssh, user_to_add, sudo_password)

        # Change the ownership of the user's home directory
        command = f'chown -R {user_to_add}:{user_to_add} /home/{user_to_add}'
        output, errors = execute_privileged_command(ssh, command, sudo_password)
        if errors:
            raise UnexpectedRemoteHostError(errors)

        # Added
        return True
    
def reset_user_password(ssh:paramiko.SSHClient, user:str, sudo_password:str):
    command = f'passwd {user}'
    new_password = UsefulStrings().strongPassword1
    output, errors = execute_privileged_command(ssh, command, sudo_password, [new_password, new_password])
    if 'updated successfully' not in errors:
        raise UnexpectedRemoteHostError(errors)
    
def recursively_create_dir(ssh:paramiko.SSHClient, dir_path:str, sudo_password:str):
    command = f'mkdir -p {dir_path}'
    output, errors = execute_privileged_command(ssh, command, sudo_password)
    if errors:
        raise UnexpectedRemoteHostError(errors)
    
def recursively_change_owner(ssh:paramiko.SSHClient, dir_path:str, new_owner, sudo_password:str):
    command = f'chown -R {new_owner}:{new_owner} {dir_path}'
    output, errors = execute_privileged_command(ssh, command, sudo_password)
    if errors:
        raise UnexpectedRemoteHostError(errors)
    
def create_blank_file_with_path(ssh:paramiko.SSHClient, path:str, sudo_password:str):
    # Delete the file (if it exists)
    command = f'rm {path}'
    output, errors = execute_privileged_command(ssh, command, sudo_password)
    if (errors) and ('No such file' not in errors):
        raise UnexpectedRemoteHostError(errors)
    # Recreate it
    command = f'touch {path}'
    output, errors = execute_privileged_command(ssh, command, sudo_password)
    if errors:
        raise UnexpectedRemoteHostError(errors)
    
def change_permissions(ssh:paramiko.SSHClient, path:str, permission_nums:int, sudo_password:str):
    command = f'chmod {permission_nums} {path}'
    output, errors = execute_privileged_command(ssh, command, sudo_password)
    if errors:
        raise UnexpectedRemoteHostError(errors)
    
def copy_file_to_other_file(ssh:paramiko.SSHClient, source_file_path:str, destination_file_path:str, sudo_password:str):
    command = f'cp -p  {source_file_path} {destination_file_path}'
    output, errors = execute_privileged_command(ssh, command, sudo_password)
    if errors:
        raise UnexpectedRemoteHostError(errors)

def copy_file_to_remote_host(ssh:paramiko.SSHClient, path_to_local_file:str) -> str:
    """Copies a file from the client's computer to the temp folder of the remote host.

    Args:
        ssh (paramiko.SSHClient): the ssh client session
        path_to_local_file (str): the path on the client's computer

    Returns:
        str: the remote host file path of the copied file
    """    
    with sftp_connection(ssh) as sftp:
        file_name = os.path.basename(path_to_local_file)
        temp_remote_file_path = f"/tmp/{file_name}"
        sftp.put(path_to_local_file, temp_remote_file_path)
        return temp_remote_file_path

def set_up_ssh_for_user(ssh:paramiko.SSHClient, designated_user:str, local_path_of_pub_ssh_key:str, sudo_password:str):
    # Add the user, if needed, to the remote host
    add_user_if_necessary(ssh, designated_user, sudo_password)

    # Add the necessary dirs if not already created
    dir_path = f'/home/{designated_user}/.ssh/'
    recursively_create_dir(ssh, dir_path, sudo_password)

    # Recreates the known_hosts files from scratch
    file_path = f'/home/{designated_user}/.ssh/known_hosts'
    create_blank_file_with_path(ssh, file_path, sudo_password)

    # Send the pub file from client to /home/username/.ssh/authorized_keys
    tmp_path_on_remote = copy_file_to_remote_host(ssh, local_path_of_pub_ssh_key)
    file_path = f'/home/{designated_user}/.ssh/authorized_keys'
    copy_file_to_other_file(ssh, tmp_path_on_remote, file_path, sudo_password)

    # Change the files' and dirs' owner
    dir_path = f'/home/{designated_user}/'
    recursively_change_owner(ssh, dir_path, designated_user, sudo_password)

    # Change the files' and dirs' permissions
    dir_path = f'/home/{designated_user}/'
    change_permissions(ssh, dir_path, 755, sudo_password)
    dir_path = f'/home/{designated_user}/.ssh'
    change_permissions(ssh, dir_path, 700, sudo_password)
    file_path = f'/home/{designated_user}/.ssh/authorized_keys'
    change_permissions(ssh, file_path, 600, sudo_password)
    file_path = f'/home/{designated_user}/.ssh/known_hosts'
    change_permissions(ssh, file_path, 644, sudo_password)

def main():
    remote_host_ip = ''
    sudo_password = ''
    defender = 'blueteam'
    with ssh_connection(remote_host_ip, defender, sudo_password) as ssh:
        user_to_ssh_pub_key = {
            'samanthaallen': '/path/to/key.pub',
        }
        for user, path_ssh_pub_key in user_to_ssh_pub_key.items():
            set_up_ssh_for_user(ssh, user, path_ssh_pub_key, sudo_password)

    
if __name__ == '__main__':
    main()




