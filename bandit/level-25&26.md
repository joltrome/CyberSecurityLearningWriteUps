# Bandit Levels 25 → 27 - Shell Escape and Vi Editor Exploitation

## Bandit Level 25 → 26

### Challenge Description
Logging in to bandit26 from bandit25 should be fairly easy… The shell for user bandit26 is not **/bin/bash**, but something else. Find out what it is, how it works and how to break out of it.

### Solution

#### Step 1: Reconnaissance
First, I explored the bandit25 home directory to identify available resources:
```bash
ls -la
```

**Key findings:**
```
-r--------   1 bandit25 bandit25 1679 Aug 15 13:16 bandit26.sshkey
```

Found an SSH private key for bandit26.

#### Step 2: Investigating bandit26's Shell
I checked what shell bandit26 uses instead of the standard bash:
```bash
cat /etc/passwd | grep bandit26
```

**Output:**
```
bandit26:x:11026:11026:bandit level 26:/home/bandit26:/usr/bin/showtext
```

**Critical discovery:** bandit26's shell is `/usr/bin/showtext`, not `/bin/bash`.

#### Step 3: Analyzing the Custom Shell
I examined what this custom "shell" actually does:
```bash
cat /usr/bin/showtext
```

**Script contents:**
```bash
#!/bin/sh
export TERM=linux
exec more ~/text.txt
exit 0
```

**Understanding the behavior:**
- Sets terminal type to linux
- Executes `more ~/text.txt` (displays a text file)
- Exits immediately after `more` finishes

This means when logging into bandit26, instead of getting an interactive shell, the system just shows a text file and then disconnects.

#### Step 4: Initial SSH Connection Attempts
I attempted to connect using the SSH key:
```bash
ssh -i bandit26.sshkey bandit26@localhost -p 2220
```

**What I observed:** 
- Connection established successfully
- Saw the OverTheWire banner and bandit26 ASCII art
- Connection immediately closed without giving me a shell prompt

**Why this happened:** 
- The `/usr/bin/showtext` "shell" executed `more ~/text.txt`
- My terminal was large enough to display the entire text file at once
- When `more` finished displaying the file, it exited immediately
- This caused the "shell" to exit, closing the SSH connection
- I never got an interactive prompt because the custom shell doesn't provide one

**Key realization:** I needed to make `more` enter interactive mode instead of just displaying and exiting.

#### Step 5: The Key Insight - Terminal Size Manipulation
**Critical realization:** The `more` command only becomes interactive when the content doesn't fit entirely on the screen.

**Strategy:** Make the terminal window very small so that `more` cannot display the entire file at once.

#### Step 6: Exploiting the `more` Command
**Preparation:**
1. **Manually resized my terminal window** to be extremely small - approximately 5-6 lines tall
   - This was crucial: `more` only becomes interactive when it can't fit all content on screen
   - If the terminal is too large, `more` displays everything and exits immediately

2. **Connected via SSH again:**
   ```bash
   ssh -i bandit26.sshkey bandit26@localhost -p 2220
   ```

**What happened this time:**
- Connection established
- OverTheWire banner started displaying
- **Critical moment:** Because my terminal was too small to show all the text, `more` couldn't display everything at once
- Instead of exiting, `more` displayed the first part of the text and stopped
- At the bottom of the screen, I saw the `more` interactive prompt

**Success indicators:**
- The screen showed partial content with `~` symbols indicating empty lines
- Most importantly: I saw a `:` prompt at the bottom
- The connection stayed open instead of closing immediately
- I was now **inside the interactive `more` program**

#### Step 7: Escaping to Vi Editor
**From within the `more` program:**
At the `:` prompt, I typed the `v` command:
```
v
```

**What the `v` command does:**
- `v` is a built-in `more` command that opens the current file in vi editor
- This transfers control from `more` to vi, but maintains the same user context (bandit26)
- Vi opens with the same text file that `more` was displaying

**Result:**
- The screen changed to vi editor interface
- I could see the text file content in vi
- Vi was now running with bandit26 privileges
- Most importantly: Vi has much more powerful escape capabilities than `more`


- I could now run normal shell commands
- I had successfully bypassed the restrictive custom shell
- The escape chain was complete: SSH → `more` → vi → bash shell

#### Step 9: Retrieving the Password
With shell access as bandit26, I could read the password:
```bash
cat /etc/bandit_pass/bandit26
```

**Password obtained:** `s0773xxkk0MXfdqOfPRVr9L3jJBUOgCZ`

## Bandit Level 26 → 27

### Challenge Discovery
After gaining shell access to bandit26, I explored the home directory:
```bash
ls -la
```

**Key finding:**
```
-rwsr-x---   1 bandit27 bandit26 14884 Aug 15 13:16 bandit27-do
```

Found a **setuid binary** owned by bandit27, similar to previous levels.

### Solution

#### Step 2: Testing the Setuid Binary
I examined the binary to understand its capabilities:
```bash
./bandit27-do
```

**Output:**
```
Run a command as another user.
  Example: ./bandit27-do id
```

**What this tells me:**
- This is the same type of setuid binary from previous levels
- It allows running commands as bandit27 (the owner of the file)
- The syntax is: `./bandit27-do [command]`
- Since it's owned by bandit27 with setuid bit, any command I run through it will execute with bandit27 privileges

#### Step 2: Retrieving bandit27's Password
Using the setuid binary to read bandit27's password:
```bash
./bandit27-do cat /etc/bandit_pass/bandit27
```

**Password obtained:** `upsNCc7vzaRDx6oZC6GiR6ERwe1MowGB`

## Key Learning Points

### 1. Shell Escape Techniques
- **Custom shells**: Understanding that not all "shells" are interactive
- **Program limitations**: Exploiting the behavior of programs like `more`
- **Editor escapes**: Using vi's shell escape functionality (`:shell`)
- **Terminal manipulation**: Controlling program behavior through terminal size

### 2. The `more` Command Exploitation
- **Interactive mode**: `more` becomes interactive only when content exceeds screen size
- **Command availability**: `more` supports various commands including `v` (vi editor)
- **Chaining escapes**: Using `more` → `vi` → `shell` escape chain
- **Environmental control**: Manipulating terminal size to trigger desired behavior

### 3. Vi Editor Security Implications
- **Shell access**: Vi can spawn shells via `:shell` command
- **File system access**: Vi can read/write files with user privileges
- **Command execution**: Vi supports executing external commands
- **Privilege context**: Vi runs with the same privileges as the user who launched it

### 4. Progressive Privilege Escalation
- **Level 25→26**: Custom shell escape through program manipulation
- **Level 26→27**: Traditional setuid binary exploitation
- **Chaining techniques**: Combining multiple exploitation methods

### 5. Problem-Solving Methodology
- **System investigation**: Checking `/etc/passwd` for unusual configurations
- **Behavioral analysis**: Understanding how custom programs work
- **Creative thinking**: Manipulating environment to change program behavior
- **Tool knowledge**: Knowing escape techniques for common programs

## Command Summary

### Level 25→26:
```bash
# Investigation
ls -la
cat /etc/passwd | grep bandit26
cat /usr/bin/showtext

# Exploitation (with small terminal)
ssh -i bandit26.sshkey bandit26@localhost -p 2220
# In more: v (to enter vi)
# In vi: :shell (to get shell)

# Password retrieval
cat /etc/bandit_pass/bandit26
```

### Level 26→27:
```bash
# Discovery
ls -la

# Exploitation
./bandit27-do cat /etc/bandit_pass/bandit27
```

## Alternative Escape Methods

### Other `more` Commands:
- `!command` - Execute shell commands directly from more
- `q` - Quit more (would return to showtext and exit)
- `/pattern` - Search within the file
- `h` - Help (shows available commands)

### Other Vi Escape Techniques:
```bash
# In vi:
:!command              # Execute shell command
:set shell=/bin/bash   # Set shell type
:shell                 # Open interactive shell
:w !command            # Write to command stdin
```

### Terminal Size Manipulation Methods:
```bash
# Resize terminal programmatically
printf '\e[8;5;20t'    # Resize to 5 rows, 20 columns

# Using stty to control terminal
stty rows 5 cols 20
```

## Real-World Applications

### 1. Penetration Testing
- **Restricted shell bypass**: Escaping from limited shell environments
- **Application security**: Testing applications that use pagers or editors
- **Privilege escalation**: Finding ways to break out of restricted environments
- **Social engineering**: Understanding how users might accidentally grant shell access

### 2. System Administration
- **Security hardening**: Understanding risks of allowing interactive programs
- **User environment control**: Properly configuring restricted user environments
- **Audit considerations**: Monitoring for unusual shell escape attempts
- **Policy enforcement**: Preventing unauthorized shell access

### 3. Incident Response
- **Attack analysis**: Understanding how attackers escape restricted environments
- **Forensic investigation**: Identifying signs of shell escape techniques
- **Containment strategies**: Preventing further privilege escalation
- **Recovery procedures**: Securing systems after shell escape incidents

### 4. Security Best Practices
- **Principle of least privilege**: Limiting access to interactive programs
- **Environment validation**: Ensuring custom shells don't provide unintended access
- **Program selection**: Choosing appropriate tools for restricted environments
- **Monitoring implementation**: Logging and alerting on unusual program behavior

## Security Implications

### 1. Custom Shell Risks
- **Inadequate restrictions**: Custom shells may provide unintended escape routes
- **Program complexity**: More complex programs have more potential vulnerabilities
- **User education**: Users may not understand the security implications of their actions

### 2. Interactive Program Security
- **Pager programs**: `more`, `less` can provide shell access
- **Editors**: `vi`, `nano`, `emacs` typically support shell commands
- **Help systems**: Many programs' help functions can be exploited
- **Terminal emulators**: Even basic terminal features can sometimes be exploited

This was the hardest level so far as it demonstrates sophisticated shell escape techniques and highlights the importance of understanding the security implications of interactive programs in restricted environments.
