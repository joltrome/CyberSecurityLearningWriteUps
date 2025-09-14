# Bandit Level 16 - SSL Port Scanning and SSH Key Authentication

## Challenge Description
The credentials for the next level can be retrieved by submitting the password of the current level to **a port on localhost in the range 31000 to 32000**. First find out which of these ports have a server listening on them. Then find out which of those speak SSL/TLS and which don't. There is only 1 server that will give the next credentials, the others will simply send back to you whatever you send to it.

## Solution

### Step 1: Understanding the Challenge
The challenge requires us to:
- Scan ports 31000-32000 on localhost to find active services
- Identify which services speak SSL/TLS
- Find the one service that provides credentials instead of echoing input
- Submit the current level's password to get the next credentials

### Step 2: Initial Port Scanning
First, I scanned the specified port range to identify which ports have active services:
```bash
nmap -p 31000-32000 localhost
```

**Output:**
```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-09-14 04:34 UTC
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00011s latency).
Not shown: 996 closed tcp ports (conn-refused)
PORT      STATE SERVICE
31046/tcp open  unknown
31518/tcp open  unknown
31691/tcp open  unknown
31790/tcp open  unknown
31960/tcp open  unknown
```

This identified 5 active ports that need further investigation.

### Step 3: Service Version Detection
To determine which services speak SSL/TLS, I used nmap's service version detection:
```bash
nmap -p 31000-32000 -sV localhost
```

**Output:**
```
PORT      STATE SERVICE     VERSION
31046/tcp open  echo
31518/tcp open  ssl/echo
31691/tcp open  echo
31790/tcp open  ssl/unknown
31960/tcp open  echo
```

### Step 4: Analyzing the Results
From the scan results, I identified:
- **Regular echo servers**: Ports 31046, 31691, 31960 (will just echo back input)
- **SSL echo server**: Port 31518 (SSL-enabled but still just echoes)
- **SSL unknown service**: Port 31790 (SSL-enabled with unknown behavior - this is our target!)

### Step 5: Connecting to the Target Service
I connected to port 31790 using SSL and submitted the current level's password:
```bash
ncat --ssl localhost 31790
```

After entering the bandit16 password, instead of getting a simple password back, I received an RSA private key:

```
-----BEGIN RSA PRIVATE KEY-----
[RSA private key content]
-----END RSA PRIVATE KEY-----
```

### Step 6: Using the RSA Private Key
Since this was an SSH private key rather than a password, I needed to:

1. **Save the key to a file**:
   ```bash
   nano /tmp/bandit17.key
   # Pasted the entire RSA private key content
   ```

2. **Set proper file permissions** (SSH requires restrictive permissions):
   ```bash
   chmod 600 /tmp/bandit17.key
   ```

3. **Use the key to SSH into bandit17**:
   ```bash
   ssh -i /tmp/bandit17.key bandit17@bandit.labs.overthewire.org -p 2220
   ```

**Success!** This granted access to bandit17.

## Key Learning Points

### 1. Network Service Discovery
- **nmap port scanning**: Essential for discovering active network services
- **Service version detection** (`-sV`): Identifies the type and capabilities of services
- **SSL/TLS identification**: Critical for understanding how to interact with services

### 2. SSL/TLS Communication
- Services marked as `ssl/` require encrypted connections
- `openssl s_client` is the standard tool for connecting to SSL services
- Always check if a service requires SSL before attempting plain connections

### 3. SSH Key-Based Authentication
- **Private keys vs passwords**: Not all authentication uses passwords
- **File permissions matter**: SSH private keys must have restrictive permissions (600)
- **SSH key usage**: The `-i` flag specifies the private key file for authentication

### 4. CTF Problem-Solving Strategy
- **Process of elimination**: Test each discovered service systematically
- **Pattern recognition**: "Echo" services typically just return your input
- **Expect the unexpected**: Credentials aren't always passwords - they could be keys, tokens, etc.

### 5. File Management in Restricted Environments
- **Permission issues**: Always consider write permissions when saving files
- **Safe directories**: `/tmp` is usually writable when home directories aren't
- **Temporary storage**: Use `/tmp` for temporary files that don't need persistence

## Command Summary
```bash
# Port discovery
nmap -p 31000-32000 localhost

# Service identification  
nmap -p 31000-32000 -sV localhost

# SSL connection
ncat --ssl localhost 31790

# File management
nano /tmp/bandit17.key
chmod 600 /tmp/bandit17.key

# SSH with private key
ssh -i /tmp/bandit17.key bandit17@bandit.labs.overthewire.org -p 2220
```

## Real-World Applications
This level demonstrates several important cybersecurity concepts:

- **Network reconnaissance**: Port scanning is a fundamental skill in penetration testing
- **Service enumeration**: Identifying service types and versions helps determine attack vectors
- **Secure communications**: Understanding SSL/TLS is crucial for modern network security
- **Public key cryptography**: SSH key authentication is widely used in production environments
- **Privilege escalation**: Using discovered credentials to gain access to new systems

The methodology used here mirrors real-world penetration testing workflows where attackers scan for services, identify communication protocols, and exploit services to gain credentials for lateral movement.
