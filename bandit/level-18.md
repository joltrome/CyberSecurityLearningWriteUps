# Bandit Level 18 - Bypassing Malicious .bashrc

## Challenge Description
The password for the next level is stored in a file **readme** in the homedirectory. Unfortunately, someone has modified **.bashrc** to log you out when you log in with SSH.

## Solution

### Step 1: Understanding the Problem
The challenge presents a common scenario where:
- A malicious `.bashrc` file automatically logs us out upon SSH login
- We need to read a file (`readme`) without triggering the problematic `.bashrc`
- This simulates real-world situations where login scripts have been compromised

### Step 2: Method 1 - Direct Command Execution (Known Target)
Since the challenge specifically mentions a `readme` file, I first tried executing the command directly through SSH without establishing an interactive session:

```bash
ssh bandit18@bandit.labs.overthewire.org -p 2220 "cat readme"
```

**Result:** This successfully retrieved the password without triggering `.bashrc` because:
- No interactive shell was started
- The command executed directly and returned the output
- `.bashrc` only runs when starting an interactive bash session

### Step 3: Method 2 - Interactive Shell Bypass (Real-World Approach)
In real-world scenarios, we wouldn't know the specific filename. To simulate a more realistic approach, I used an alternative shell to explore the directory:

```bash
ssh bandit18@bandit.labs.overthewire.org -p 2220 -t "/bin/sh"
```

This approach:
1. **Bypassed bash entirely** by using `/bin/sh` instead of the default bash shell
2. **Allocated a pseudo-terminal** with the `-t` flag for interactive exploration
3. **Avoided `.bashrc execution** since we're not using bash

### Step 4: Directory Exploration
Once in the alternative shell, I explored the directory structure:
```bash
ls
```

**Output:**
```
readme
```

### Step 5: Reading the Target File
```bash
cat readme
```

This revealed the password for bandit19.

### Step 6: Exiting the Session
```bash
exit
```

## Key Learning Points

### 1. SSH Command Execution vs Interactive Sessions
- **Direct execution**: `ssh user@host "command"` runs commands without starting an interactive shell
- **Interactive session**: `ssh user@host` starts a full shell session (triggering `.bashrc`)
- **Use case**: Direct execution is perfect when you know exactly what you want to do

### 2. Shell Alternatives and Bypasses
- **Different shells**: `/bin/sh`, `/bin/dash`, `/bin/zsh` can bypass bash-specific configurations
- **Shell flags**: `bash --norc` disables `.bashrc` execution
- **Pseudo-terminal allocation**: `-t` flag creates interactive environment when needed

### 3. Real-World Relevance
- **Incident response**: When login scripts are compromised, alternative access methods are crucial
- **System recovery**: Bypassing problematic configurations to regain system access
- **Security testing**: Understanding how attackers might bypass security measures

### 4. Reconnaissance vs Direct Attack
- **Known targets**: Use direct methods when you have specific information
- **Unknown environments**: Explore systematically using safe alternative methods
- **Defense in depth**: Always have multiple approaches available

## Command Summary
```bash
# Method 1: Direct command execution (when target is known)
ssh bandit18@bandit.labs.overthewire.org -p 2220 "cat readme"

# Method 2: Alternative shell exploration (real-world approach)
ssh bandit18@bandit.labs.overthewire.org -p 2220 -t "/bin/sh"
ls
cat readme
exit
```

## Alternative Solutions
```bash
# Using bash without rc files
ssh bandit18@bandit.labs.overthewire.org -p 2220 -t "bash --norc"

# Direct listing and reading
ssh bandit18@bandit.labs.overthewire.org -p 2220 "ls -la"
ssh bandit18@bandit.labs.overthewire.org -p 2220 "cat readme"

# Using different shells
ssh bandit18@bandit.labs.overthewire.org -p 2220 -t "/bin/dash"
```

## Real-World Applications

### 1. Incident Response
When responding to compromised systems where login scripts have been modified:
- Use alternative shells to avoid triggering malicious code
- Execute commands directly to minimize system interaction
- Maintain forensic integrity by avoiding unnecessary file modifications

### 2. System Administration
- **Recovery scenarios**: When `.bashrc` or `.profile` files are corrupted
- **Automation**: Running commands on remote systems without interactive sessions
- **Monitoring**: Executing health checks without full login procedures

### 3. Security Testing
- **Privilege escalation**: Bypassing restrictions in login scripts
- **Persistence mechanisms**: Understanding how attackers maintain access
- **Defense evaluation**: Testing how well security measures handle alternative access methods

### 4. SSH Best Practices
- **Command execution**: More secure and efficient for automated tasks
- **Shell selection**: Understanding when different shells are appropriate
- **Session management**: Minimizing attack surface through targeted access

This level effectively demonstrates that there are always multiple ways to accomplish a task, and understanding various access methods is crucial for both offensive and defensive security operations.
