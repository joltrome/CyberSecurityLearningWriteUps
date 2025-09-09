# Bandit Level 0 - SSH Connection Basics

## Challenge Description
The goal of this level is for you to log into the game using SSH. The host to which you need to connect is **bandit.labs.overthewire.org**, on port 2220. The username is **bandit0** and the password is **bandit0**. Once logged in, go to the Level 1 page to find out how to beat Level 1.

## Solution

### Understanding SSH Connection Syntax
SSH (Secure Shell) is used to securely connect to remote servers. The basic syntax is:
```bash
ssh [options] username@hostname
```

### Step 1: Identifying the Connection Parameters
From the challenge description, I extracted:
- **Host**: bandit.labs.overthewire.org
- **Port**: 2220 (non-standard port, default SSH port is 22)
- **Username**: bandit0
- **Password**: bandit0

### Step 2: Connecting via SSH
I used the following command to connect:

```bash
ssh -p 2220 bandit0@bandit.labs.overthewire.org
```

**Command Breakdown:**
- `ssh` - The SSH client command
- `-p 2220` - Specifies the port number (2220 instead of default port 22)
- `bandit0` - The username for authentication
- `@` - Separator between username and hostname
- `bandit.labs.overthewire.org` - The server hostname/address

### Step 3: Authentication
After running the command, I was prompted for a password:
```
bandit0@bandit.labs.overthewire.org's password:
```

I entered the password: `bandit0`

### Step 4: Successful Connection
Upon successful authentication, I was logged into the Bandit server and saw the welcome message and command prompt:
```
bandit0@bandit:~$
```

This indicates I'm now logged in as user `bandit0` on the `bandit` server.

## Key Learning Points

### SSH Syntax Components
1. **Username placement**: Always comes before the `@` symbol
2. **Hostname**: Always comes after the `@` symbol
3. **Port specification**: Use `-p` flag followed by port number
4. **Password authentication**: Entered interactively when prompted (not in command for security)

### Important SSH Concepts
- **Default port**: SSH typically uses port 22, but this challenge uses 2220
- **Security**: Passwords are not visible when typing (this is normal)
- **Connection format**: `username@hostname` is the standard format for remote connections

### Command Structure
```bash
ssh [flags] username@hostname
```
Common flags:
- `-p [port]` - Specify custom port
- `-v` - Verbose output (useful for debugging)
- `-l [username]` - Alternative way to specify username

## Alternative Connection Methods
You could also connect using:
```bash
ssh -l bandit0 -p 2220 bandit.labs.overthewire.org
```
This uses the `-l` flag to specify the username instead of the `username@hostname` format.

## Next Steps
After successfully logging in, the challenge directs to check Level 1 instructions to continue the Bandit series. The connection established here will be the foundation for all subsequent Bandit levels.

## Troubleshooting Tips
- **Connection refused**: Check if the port number is correct
- **Host unreachable**: Verify the hostname spelling
- **Authentication failed**: Double-check username and password
- **Permission denied**: Ensure you're using the correct credentials
