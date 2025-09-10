# Bandit Level 6 - System-wide File Search

## Challenge Description
The password for the next level is stored **somewhere on the server** and has all of the following properties:
- owned by user bandit7
- owned by group bandit6
- 33 bytes in size

## Solution

### Step 1: Initial Directory Search
I first tried the usual approach of checking the current directory:

```bash
ls
ls -a
```

These commands showed the files in the current directory (`/home/bandit6/`) but didn't reveal any files matching the criteria. I then realized the challenge mentioned tha the file is stored "somewhere on the server," meaning I have to search beyond just the current directory.

### Step 2: First Attempt with find
I attempted to use the `find` command for a system-wide search:

```bash
find/ -user bandit7 -group bandit6 -size 33c
```

**Error encountered:**
```
bash: find/: No such file or directory
```

I realized my mistake - there needs to be a space between `find` and `/`.

### Step 3: Corrected find Command
I fixed the syntax error:

```bash
find / -user bandit7 -group bandit6 -size 33c
```

**Command breakdown:**
- `find /` - Search starting from root directory (entire system)
- `-user bandit7` - Files owned by user bandit7
- `-group bandit6` - Files owned by group bandit6
- `-size 33c` - Files exactly 33 bytes in size (c = bytes)

**Problem encountered:**
The command worked but produced many "Permission denied" error messages mixed with the results, making it difficult to identify the actual file:

```
find: ‘/etc/polkit-1/rules.d’: Permission denied
find: ‘/etc/multipath’: Permission denied
find: ‘/home/bandit31-git’: Permission denied
find: ‘/home/bandit5/inhere’: Permission denied
find: ‘/home/leviathan4/.trash’: Permission denied
find: ‘/home/bandit30-git’: Permission denied
... (many more permission denied messages)
```

### Step 4: Filtering Out Error Messages
To get clean output, I redirected the error messages:

```bash
find / -user bandit7 -group bandit6 -size 33c 2>/dev/null
```

**Clean output:**
```
/var/lib/dpkg/info/bandit7.password
```

**Error redirection explanation:**
- `2>/dev/null` redirects error messages (stderr) to `/dev/null`
- `/dev/null` discards any data sent to it
- This filters out "Permission denied" messages while keeping the actual results

### Step 5: Accessing the Password File
Now that I found the file location, I navigated to it and read the contents:

```bash
cd /var/lib/dpkg/info
cat bandit7.password
```

This revealed the password for the next level.

## Key Learning Points

### 1. System-wide vs Local Search
- `ls` and `ls -a` only search the current directory
- When a challenge says "somewhere on the server," use system-wide search with `find /`

### 2. find Command Syntax
- Correct: `find /` (with space)
- Incorrect: `find/` (no space causes "command not found" error)

### 3. Multiple Search Criteria
The `find` command can combine multiple criteria:
- `-user [username]` - Filter by file owner
- `-group [groupname]` - Filter by group owner  
- `-size [size]c` - Filter by file size in bytes

### 4. Error Message Management
- Without `2>/dev/null`: Results mixed with permission errors
- With `2>/dev/null`: Clean output showing only accessible results
- `2>` redirects stderr (error messages)
- `>/dev/null` discards the redirected content

### 5. File Permissions in Linux
Many directories require elevated privileges to access, causing "Permission denied" errors during system-wide searches. This is normal behavior and why error filtering is useful.

## Alternative Approaches
- Could use `find / -user bandit7 -group bandit6 -size 33c 2>&1 | grep -v "Permission denied"` to filter errors differently
- Could search specific directories if you had hints about the location
- Could use `locate` command if the file database was updated (less reliable)

## Command Summary
```bash
# Final working command
find / -user bandit7 -group bandit6 -size 33c 2>/dev/null

# Read the found file
cat /var/lib/dpkg/info/bandit7.password
```
