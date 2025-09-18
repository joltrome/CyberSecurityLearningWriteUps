# Bandit Levels 19-21 - Setuid Binaries and Network Communication

## Bandit Level 19 → 20

### Challenge Description
To gain access to the next level, you should use the setuid binary in the homedirectory. Execute it without arguments to find out how to use it. The password for this level can be found in the usual place (/etc/bandit_pass), after you have used the setuid binary.

### Solution

#### Step 1: Understanding Setuid Binaries
First, I examined the home directory to identify the setuid binary:
```bash
ls -la
```

**Output:**
```
-rwsr-x--- 1 bandit20 bandit19 14876 Sep 19 07:08 bandit20-do
```

Key observations:
- The `s` in the permissions (`-rwsr-x---`) indicates this is a **setuid binary**
- It's owned by `bandit20` but executable by `bandit19`
- When executed, it will run with `bandit20` privileges

#### Step 2: Exploring the Binary Usage
I ran the binary without arguments to understand its functionality:
```bash
./bandit20-do
```

**Output:**
```
Run a command as another user.
  Example: ./bandit20-do id
```

This confirmed that the binary allows executing commands as `bandit20`.

#### Step 3: Reading the Password File
Since I needed the password for bandit20, and it would be stored in `/etc/bandit_pass/bandit20`, I used the setuid binary to read it:
```bash
./bandit20-do cat /etc/bandit_pass/bandit20
```

**Password obtained:** `0qXahG8ZjOVMN9Ghs7iOWsCfZyXOUbYO`

## Bandit Level 20 → 21

### Challenge Description
There is a setuid binary in the homedirectory that does the following: it makes a connection to localhost on the port you specify as a commandline argument. It then reads a line of text from the connection and compares it to the password in the previous level (bandit20). If the password is correct, it will transmit the password for the next level (bandit21).

### Solution

#### Step 1: Understanding the Challenge
This level requires:
- Setting up a server that sends the bandit20 password
- Using the setuid binary to connect to that server
- The binary will verify the password and respond with bandit21's password

#### Step 2: Examining the Binary
First, I identified the setuid binary:
```bash
ls -la
```

Found the binary: `suconnect`

#### Step 3: Setting Up the Server and Client
I needed to create a network connection where:
1. A server sends the bandit20 password
2. The `suconnect` binary connects to verify it
3. If correct, it returns the bandit21 password

I used a combination of `echo`, `nc` (netcat), and the `suconnect` binary:

```bash
echo "0qXahG8ZjOVMN9Ghs7iOWsCfZyXOUbYO" | nc -l -p 1234 -q 10 & ./suconnect 1234
```

**Breaking down this command:**
- `echo "0qXahG8ZjOVMN9Ghs7iOWsCfZyXOUbYO"` - sends the bandit20 password
- `|` - pipes the output to netcat
- `nc -l -p 1234 -q 10` - creates a listening server on port 1234 that quits after 10 seconds
- `&` - runs the server in the background
- `./suconnect 1234` - connects the binary to port 1234

#### Step 4: Success
The `suconnect` binary:
1. Connected to the netcat server on port 1234
2. Read the bandit20 password from the connection
3. Verified it was correct
4. Transmitted the bandit21 password

**Password obtained:** `[bandit21 password]`

## Key Learning Points

### 1. Setuid Binary Fundamentals
- **Purpose**: Allow users to execute programs with elevated privileges
- **Security implications**: Can be used for legitimate privilege escalation
- **Identification**: Look for the `s` bit in file permissions (`-rwsr-xr-x`)
- **Real-world usage**: Common in system utilities like `passwd`, `sudo`

### 2. Network Communication Concepts
- **Client-server model**: One program listens, another connects
- **Port-based communication**: Programs communicate through specific network ports
- **Synchronization**: Server must be running when client attempts to connect

### 3. Command Composition and Backgrounding
- **Pipes (`|`)**: Chain commands together, passing output as input
- **Background processes (`&`)**: Allow commands to run simultaneously
- **Netcat versatility**: Can act as both client and server for network testing

### 4. Problem-Solving Strategy
- **Level 19**: Direct privilege escalation using setuid binary
- **Level 20**: Complex interaction requiring coordination between multiple processes
- **Progression**: Each level builds on previous networking and privilege concepts

## Command Summary

### Level 19:
```bash
# Examine permissions
ls -la

# Test binary usage
./bandit20-do

# Read password file
./bandit20-do cat /etc/bandit_pass/bandit20
```

### Level 20:
```bash
# Create server and connect client simultaneously
echo "0qXahG8ZjOVMN9Ghs7iOWsCfZyXOUbYO" | nc -l -p 1234 -q 10 & ./suconnect 1234
```

## Alternative Solutions

### Level 20 Alternative Approaches:
```bash
# Method 1: Using two terminals
# Terminal 1:
echo "0qXahG8ZjOVMN9Ghs7iOWsCfZyXOUbYO" | nc -l -p 1234

# Terminal 2:
./suconnect 1234

# Method 2: Using tmux/screen for session management
# Method 3: Different port numbers to avoid conflicts
```

## Real-World Applications

### 1. Privilege Escalation
- **Legitimate uses**: System administration tools requiring elevated privileges
- **Security testing**: Identifying misconfigurated setuid binaries
- **Incident response**: Understanding how attackers might abuse setuid binaries

### 2. Network Service Testing
- **Service verification**: Testing if network services respond correctly
- **Authentication testing**: Verifying credential validation mechanisms
- **Protocol testing**: Understanding client-server communication patterns

### 3. Process Coordination
- **Background services**: Managing long-running processes
- **Inter-process communication**: Coordinating between multiple programs
- **Automation**: Creating scripts that manage multiple simultaneous tasks

### 4. Security Concepts
- **Defense in depth**: Understanding multiple layers of system security
- **Attack vectors**: Recognizing how network services can be exploited
- **System hardening**: Learning to secure setuid binaries and network services

These levels effectively demonstrate the intersection of privilege management and network communication, core concepts in both system administration and cybersecurity.
