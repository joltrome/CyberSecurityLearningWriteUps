# Bandit Level 22 → 23 - Dynamic Filename Generation with MD5 Hashing

## Challenge Description
A program is running automatically at regular intervals from **cron**, the time-based job scheduler. Look in **/etc/cron.d/** for the configuration and see what command is being executed.

**NOTE: Looking at shell scripts written by other people is a very useful skill. The script for this level is intentionally made easy to read. If you are having problems understanding what it does, try executing it to see the debug information it prints.**

## Solution

### Step 1: Exploring System Cron Jobs
Building on the previous level's knowledge, I examined the cron directory:
```bash
ls -la /etc/cron.d/
```

**Output:**
```
-rw-r--r--   1 root root   122 Aug 15 13:16 cronjob_bandit23
```

Found the relevant cron job for this level.

### Step 2: Examining the Cron Configuration
```bash
cat /etc/cron.d/cronjob_bandit23
```

**Output:**
```
@reboot bandit23 /usr/bin/cronjob_bandit23.sh  &> /dev/null
* * * * * bandit23 /usr/bin/cronjob_bandit23.sh  &> /dev/null
```

This shows that `/usr/bin/cronjob_bandit23.sh` runs every minute as the bandit23 user.

### Step 3: Analyzing the Script
```bash
cat /usr/bin/cronjob_bandit23.sh
```

**Script contents:**
```bash
#!/bin/bash
myname=$(whoami)
mytarget=$(echo I am user $myname | md5sum | cut -d ' ' -f 1)
echo "Copying passwordfile /etc/bandit_pass/$myname to /tmp/$mytarget"
cat /etc/bandit_pass/$myname > /tmp/$mytarget
```

**Script breakdown:**
1. `myname=$(whoami)` - Gets the current username (will be "bandit23" when run by cron)
2. `mytarget=$(echo I am user $myname | md5sum | cut -d ' ' -f 1)` - Generates MD5 hash of "I am user bandit23"
3. Copies bandit23's password to `/tmp/[hash]`

### Step 4: Understanding the Key Difference
Unlike the previous level where the filename was hardcoded, this script **dynamically generates** the filename based on the username. This makes it more flexible but requires us to calculate the correct hash.

### Step 5: Initial Exploration and Common Mistakes
I started by testing the variables and understanding how the script works:

```bash
whoami
# Output: bandit22

echo i am user $myname
# Output: i am user
# (Note: $myname is not set in my shell)
```

**First mistake:** I tried using my current username instead of the target username.

### Step 6: Testing Different Username Scenarios
I tested generating hashes for different users to understand the pattern:

```bash
# Hash for bandit22 (current user)
echo I am user bandit22 | md5sum | cut -d ' ' -f 1
# Output: 8169b67bd894ddbb4412f91573b38db3

# Hash for bandit23 (target user - what the cron job uses)
echo I am user bandit23 | md5sum | cut -d ' ' -f 1
# Output: 8ca319486bfbbc3663ea0fbe81326349

# Hash using current shell variable (empty myname)
echo I am user $myname | md5sum | cut -d ' ' -f 1
# Output: 7db97df393f40ad1691b6e1fb03d53eb
```

### Step 7: Key Insight - Context Matters
The crucial realization: When the cron job runs, it executes as **bandit23**, so `whoami` returns "bandit23", not "bandit22".

Therefore, the script generates the filename using:
```bash
echo I am user bandit23 | md5sum | cut -d ' ' -f 1
# Result: 8ca319486bfbbc3663ea0fbe81326349
```

### Step 8: Retrieving the Password
Using the correct hash generated for bandit23:
```bash
cat /tmp/8ca319486bfbbc3663ea0fbe81326349
```

**Success!** Retrieved the bandit23 password: `0Zf11ioIjMVN551jX3CmStKLYqjk54Ga`

### Step 9: Verification of Wrong Approaches
I also tested what would happen if I used the wrong hash:
```bash
cat /tmp/8169b67bd894ddbb4412f91573b38db3
# Error: No such file or directory
```

This confirmed that only the hash generated with "bandit23" as the username works.

## Key Learning Points

### 1. Dynamic vs Static Filename Generation
- **Previous level**: Used hardcoded filename `t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv`
- **This level**: Generates filename dynamically using `echo I am user $username | md5sum`
- **Advantage**: Same script can work for different users
- **Challenge**: Must understand the context in which the script runs

### 2. Context Awareness in Script Analysis
- **Critical insight**: Scripts run in different contexts than when you analyze them
- **Variable values**: `whoami` returns different values depending on who runs the script
- **Execution context**: Cron jobs run as specified users, not the analyzing user

### 3. MD5 Hashing for Filename Generation
- **Purpose**: Creates consistent, unique filenames based on input
- **Predictability**: Same input always produces same hash
- **Security consideration**: MD5 is cryptographically weak but sufficient for filename generation

### 4. Methodical Problem-Solving Approach
- **Test hypotheses**: Try different username combinations
- **Understand the system**: Consider who actually runs the script
- **Verify assumptions**: Test wrong approaches to confirm understanding

### 5. Common Pitfalls and Mistakes
- **Wrong context**: Assuming script runs as current user instead of cron user
- **Variable confusion**: Not understanding when variables are set vs unset
- **Case sensitivity**: "I am user" vs "i am user" (capitalization matters)

## Command Summary
```bash
# Reconnaissance
ls -la /etc/cron.d/
cat /etc/cron.d/cronjob_bandit23
cat /usr/bin/cronjob_bandit23.sh

# Understanding the hash generation
echo I am user bandit23 | md5sum | cut -d ' ' -f 1
# Result: 8ca319486bfbbc3663ea0fbe81326349

# Getting the password
cat /tmp/8ca319486bfbbc3663ea0fbe81326349
```

## Script Analysis Techniques

### 1. Variable Tracing
```bash
# Understand what each variable contains in different contexts
whoami                    # Current user context
echo I am user $(whoami)  # Dynamic string generation
```

### 2. Command Pipeline Breakdown
```bash
# Break down complex pipelines step by step
echo I am user bandit23           # Step 1: Generate string
echo I am user bandit23 | md5sum  # Step 2: Hash the string
echo I am user bandit23 | md5sum | cut -d ' ' -f 1  # Step 3: Extract hash only
```

### 3. Context Simulation
```bash
# Simulate how the script runs in different contexts
myname="bandit23"
mytarget=$(echo I am user $myname | md5sum | cut -d ' ' -f 1)
echo $mytarget
```

## Real-World Applications

### 1. Automated System Management
- **Log file rotation**: Generate unique filenames based on dates/users
- **Backup systems**: Create consistent naming schemes for backup files
- **User session management**: Generate session identifiers

### 2. Security Analysis
- **Script behavior prediction**: Understanding how automated scripts behave in different contexts
- **Privilege escalation**: Finding files created by higher-privilege processes
- **Forensic analysis**: Predicting where automated processes store data

### 3. System Administration
- **Troubleshooting**: Understanding why automated processes behave differently than expected
- **Monitoring**: Predicting where to find files created by scheduled tasks
- **Configuration management**: Understanding how dynamic configurations are generated

### 4. Software Development
- **Testing**: Understanding how code behaves in different execution contexts
- **Debugging**: Tracing variable values through complex pipelines
- **Security**: Ensuring scripts behave correctly regardless of execution context

## Security Implications

### 1. Predictable File Generation
- **Vulnerability**: Predictable filenames allow unauthorized access
- **Mitigation**: Use cryptographically secure random generation for sensitive files
- **Best practice**: Implement proper access controls regardless of filename predictability

### 2. Information Disclosure
- **Risk**: Sensitive data stored in predictable locations
- **Impact**: Unauthorized users can access higher-privilege data
- **Prevention**: Use appropriate file permissions and secure temporary directories

This level demonstrates the importance of understanding execution context when analyzing scripts and shows how dynamic filename generation can be both a feature and a potential security concern.
