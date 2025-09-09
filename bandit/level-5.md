# Bandit Challenge - Finding File with Specific Properties

## Challenge Description
The password for the next level is stored in a file somewhere under the **inhere** directory and has all of the following properties:
- human-readable
- 1033 bytes in size
- not executable

## Solution

### Step 1: Initial Exploration
After logging into SSH, I navigated to the `inhere` directory and explored its structure:

```bash
cd inhere
file ./*
```

**Output:**
```
./maybehere00: directory
./maybehere01: directory
./maybehere02: directory
./maybehere03: directory
./maybehere04: directory
./maybehere05: directory
./maybehere06: directory
./maybehere07: directory
./maybehere08: directory
./maybehere09: directory
./maybehere10: directory
./maybehere11: directory
./maybehere12: directory
./maybehere13: directory
./maybehere14: directory
./maybehere15: directory
./maybehere16: directory
./maybehere17: directory
./maybehere18: directory
```

This showed multiple subdirectories that needs to be combed through.

### Step 2: Using find with Multiple Criteria
Instead of manually checking each directory, I used the `find` command with specific criteria to locate the target file:

```bash
find . -type f -size 1033c ! -executable -exec file {} \; 2>/dev/null | grep -E "(text|ASCII)"
```

**Command Breakdown:**
- `find .` - Search in current directory and subdirectories
- `-type f` - Only search for files (not directories)
- `-size 1033c` - Files exactly 1033 bytes in size (c = bytes)
- `! -executable` - Exclude executable files
- `-exec file {} \;` - Execute `file` command to check if human-readable
- `2>/dev/null` - Suppress permission denied errors
- `grep -E "(text|ASCII)"` - Filter for human-readable files

**Output:**
```
./maybehere07/.file2: ASCII text, with very long lines
```

### Step 3: Reading the Password
The file was found at `./maybehere07/.file2`. Since it's a hidden file (starts with dot), I accessed it directly:

```bash
cd maybehere07
cat .file2
```

This revealed the password for the next level.

## Key Learning Points
1. **Multiple criteria search**: The `find` command can combine multiple conditions to narrow down search results efficiently
2. **Hidden files**: Files starting with `.` are hidden and require explicit naming or `ls -a` to view
3. **File type detection**: The `file` command helps identify whether a file is human-readable
4. **Efficient searching**: Using `find` with specific criteria is much faster than manually checking each directory

## Alternative Approaches
- Could have used `find . -name ".*" -size 1033c ! -executable` to specifically look for hidden files
- `ls -la` in each directory to manually inspect file properties
- Using `stat` command to check file sizes and permissions
