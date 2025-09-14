# Bandit Levels 13-14 - SSH Key Authentication and Network Services

## Challenge Overview
These two levels are interconnected and introduce key concepts in SSH authentication and network service communication.

**Level 13:** Use an SSH private key to access bandit14 instead of a password.  
**Level 14:** Submit the current user's password to a network service to get the next password.

## Level 13: SSH Key Authentication

### Challenge Description
The password for the next level is stored in **/etc/bandit_pass/bandit14** and can only be read by user bandit14. For this level, you don't get the next password, but you get a private SSH key that can be used to log into the next level. **Note:** **localhost** is a hostname that refers to the machine you are working on.

### Solution - Level 13

#### Step 1: Locating the SSH Private Key
I started by examining the current directory for available files:

```bash
ls -la
```

**Output:**
```
total 24
drwxr-xr-x   2 root     root     4096 Aug 15 13:15 .
drwxr-xr-x 150 root     root     4096 Aug 15 13:18 ..
-rw-r--r--   1 root     root      220 Mar 31  2024 .bash_logout
-rw-r--r--   1 root     root     3851 Aug 15 13:09 .bashrc
-rw-r--r--   1 root     root      807 Mar 31  2024 .profile
-rw-r-----   1 bandit14 bandit13 1679 Aug 15 13:15 sshkey.private
```

The file `sshkey.private` was the SSH private key needed for authentication.

#### Step 2: Initial SSH Attempt (Wrong Approach)
My first attempt was to connect to the external server:

```bash
ssh -i sshkey.private bandit14@bandit.labs.overthewire.org
```

**Error received:**
```
!!! You are trying to log into this SSH server on port 22, which is not intended.
!!! If you are trying to log in to an OverTheWire game, use the port mentioned in
!!! the "SSH Information" on that game's webpage (in the top left corner)
```

I also tried changing file permissions but got permission denied since the file was owned by bandit14.

#### Step 3: Understanding localhost and Port Requirements
The challenge mentioned **localhost**, meaning I needed to SSH to bandit14 on the same machine. I also needed to use the correct port (2220):

```bash
ssh -i sshkey.private -p 2220 bandit14@localhost
```

**Successful connection output:**
```
The authenticity of host 'localhost (127.0.0.1)' can't be established.
ED25519 key fingerprint is SHA256:C2ihUBV7ihnV1wUXRb4RrEcLfXC5CXlhmAAM/urerLY.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
```

After typing "yes", I successfully connected as bandit14.

## Level 14: Network Service Communication

### Challenge Description
The password for the next level can be retrieved by submitting the password of the current level to **port 30000 on localhost**.

### Solution - Level 14

#### Step 1: Obtaining the Current Level Password
Now that I was logged in as bandit14, I could read the bandit14 password:

```bash
cat /etc/bandit_pass/bandit14
```

This gave me the password that I needed to submit to the service.

#### Step 2: Understanding the Network Service
The challenge required "submitting" a password to port 30000. This indicated:
- Not an SSH connection (port 30000 is not a standard SSH port)
- A custom network service that accepts data
- Need to send the password and receive a response

#### Step 3: Connecting to the Network Service
I used `netcat` (nc) to connect to the service:

```bash
nc localhost 30000
```

After connecting, I typed/pasted the bandit14 password. The service responded with the bandit15 password.

## Key Learning Points

### 1. SSH Key Authentication vs Password Authentication
- **Private keys** provide an alternative to password-based authentication
- SSH keys often have specific permission requirements (though not always modifiable)
- Key-based authentication is more secure and commonly used in production environments

### 2. SSH Connection Parameters
- **Hostname significance**: `localhost` refers to the current machine
- **Port specification**: Always use `-p` flag for non-standard ports
- **Key file specification**: Use `-i` flag to specify private key file

### 3. Understanding Different Network Services
- **SSH services**: Typically run on ports 22 or 2220, used for shell access
- **Custom services**: Can run on any port (like 30000), may have specific protocols
- **Service communication**: Different tools for different services (ssh vs nc vs curl)

### 4. Network Service Communication Tools
- **netcat (nc)**: Swiss Army knife for network connections, can connect to any port
- **telnet**: Similar to nc but with different features
- **SSH**: Specifically for encrypted shell access and file transfer

### 5. File Ownership and Permissions
- Files owned by other users may not be modifiable
- Group membership can provide read access even without ownership
- SSH key permissions are important but not always user-modifiable

### 6. Connected Challenge Design
- Some levels build directly on previous levels
- Access gained in one level enables the next level
- Information from previous level instructions remains relevant

## Command Summary

```bash
# Level 13: SSH key authentication
ls -la                                    # Find SSH private key
ssh -i sshkey.private -p 2220 bandit14@localhost  # Connect using key

# Level 14: Network service communication  
cat /etc/bandit_pass/bandit14            # Get current password
nc localhost 30000                       # Connect to network service
# (then input the password when prompted)
```

## Real-World Applications

### SSH Key Authentication
- **DevOps**: Automated deployments and server management
- **Git repositories**: Secure code repository access
- **Cloud services**: EC2, VPS, and container access
- **System administration**: Passwordless server management

### Network Service Communication
- **API testing**: Connecting to REST APIs and web services
- **Database connections**: Direct connection to database ports
- **Service debugging**: Testing custom applications and microservices
- **Network troubleshooting**: Verifying service availability

### Security Implications
- **Key management**: Proper storage and rotation of SSH keys
- **Network services**: Understanding which services are running and exposed
- **Access control**: Using appropriate authentication methods for different services

This two-level sequence demonstrates how modern systems use multiple authentication methods and network communication protocols to create layered security approaches.
