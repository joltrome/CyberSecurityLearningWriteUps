# Bandit Level 12 - Hexdump of Repeatedly Compressed File

## Challenge Description
The password for the next level is stored in the file **data.txt**, which is a hexdump of a file that has been repeatedly compressed. For this level it may be useful to create a directory under /tmp in which you can work. Use mkdir with a hard to guess directory name. Or better, use the command "mktemp -d". Then copy the datafile using cp, and rename it using mv (read the manpages!)

## Solution

This challenge involved multiple layers of compression that needed to be peeled back one by one, like an onion.

### Step 1: Setting Up Workspace
Following the challenge instructions, I created a temporary directory:

```bash
mktemp -d
cd /tmp/tmp.cFMSvX2oAb  # (random directory name generated)
cp ~/data.txt .
```

### Step 2: Understanding the Initial Data
I first examined the data to understand its format:

```bash
head -5 data.txt
```

**Output:**
```
00000000: 1f8b 0808 0933 9f68 0203 6461 7461 322e  .....3.h..data2.
00000010: 6269 6e00 0148 02b7 fd42 5a68 3931 4159  bin..H...BZh91AY
00000020: 2653 59be 9d9d 9600 001f ffff fe7f fbcf  &SY.............
00000030: af7f 9eff f7ee ffdf bff7 fef7 ddbe 9db7  ................
00000040: bf9f 9f5f ca6f fffe d6fb feff b001 3ab3  ..._.o........:.
```

This confirmed it was a hexdump format with addresses on the left, hex values in the middle, and ASCII representation on the right.

### Step 3: Converting Hexdump to Binary
I converted the hexdump back to binary data:

```bash
mv data.txt testdata2.txt
xxd -r testdata2.txt binary
```

**Initial confusion:** When I first tried `file binary`, I was still getting "ASCII text" which seemed wrong. After some troubleshooting, the conversion worked correctly.

### Step 4: Beginning the Decompression Journey
Once I had the binary file, I checked its type:

```bash
file binary
```

**Output:** `binary: gzip compressed data, was "data2.bin"`

This began the iterative process of decompression:

### Layer 1: Gzip Decompression
```bash
mv binary binary.gz
gzip -d binary.gz
file binary
```

**Result:** `binary: bzip2 compressed data, block size = 900k`

### Layer 2: Bzip2 Decompression
```bash
mv binary binary.bz2
bzip2 -d binary.bz2
file binary
```

**Result:** `binary: gzip compressed data, was "data4.bin"`

### Layer 3: Gzip Again
```bash
mv binary binary.gz
gzip -d binary.gz
file binary
```

**Result:** `binary: POSIX tar archive (GNU)`

### Layer 4: Tar Archive Extraction
```bash
mv binary binary.tar
tar -xf binary.tar
ls
```

**Result:** New file appeared: `data5.bin`

**Initial confusion with tar:** I expected the extracted file to be named "binary" but it was actually "data5.bin". This is because tar preserves the original filenames from when the archive was created.

### Layer 5: Another Tar Archive
```bash
file data5.bin
```

**Output:** `data5.bin: POSIX tar archive (GNU)`

```bash
mv data5.bin data5.tar
tar -xf data5.tar
ls
```

**Result:** New file appeared: `data6.bin`

### Layer 6: Bzip2 Again
```bash
file data6.bin
mv data6.bin data6.bz2
bzip2 -d data6.bz2
file data6
```

**Result:** `data6: POSIX tar archive (GNU)`

### Layer 7: Final Tar Archive
```bash
mv data6 data6.tar
tar -xf data6.tar
ls
```

**Result:** New file appeared: `data8.bin`

### Layer 8: Final Gzip Layer
```bash
file data8.bin
mv data8.bin data8.gz
gzip -d data8.gz
file data8
```

**Result:** `data8: ASCII text`

### Step 5: Finding the Password
Finally reaching the end:

```bash
cat data8
```

**Output:** `The password is FO5dwFsc0cbaIiH0h8J2eUks2vdTDwAn`

## Complete Decompression Sequence

The file went through this compression journey (in reverse):

1. **Original text file** → gzip → bzip2 → gzip → tar → tar → bzip2 → tar → gzip → **hexdump**
2. **My decompression process:** hexdump → gzip → bzip2 → gzip → tar → tar → bzip2 → tar → gzip → **text file**

## Key Learning Points

### 1. Working with Hexdumps
- **`xxd -r`** converts hexdump format back to binary data
- Always verify the conversion worked by checking file types
- Hexdumps represent binary data as readable hex characters

### 2. File Type Identification
- **Always use `file` command** before attempting decompression
- File extensions matter for decompression tools
- The `file` command identifies the actual format regardless of filename

### 3. Compression Tools Understanding
- **gzip/gunzip**: Fast, general-purpose compression (.gz files)
- **bzip2/bunzip2**: Higher compression ratio (.bz2 files)  
- **tar**: Archive tool that bundles files (not compression by itself)

### 4. Iterative Problem Solving
- Complex problems often require repeating the same process multiple times
- Each layer reveals the next step
- Patient, systematic approach is key

### 5. Tar Archive Behavior
- Tar preserves original filenames when extracting
- `tar -tf [file]` lists contents without extracting
- `tar -xf [file]` extracts using original filenames

### 6. File Naming Strategy
- Proper extensions help tools recognize file types
- Rename files before using format-specific tools
- Keep track of which files are originals vs. intermediate results

## Command Reference

```bash
# Hexdump conversion
xxd -r hexfile.txt binary_output

# File type checking
file filename

# Compression/Decompression
gzip -d file.gz          # or gunzip file.gz
bzip2 -d file.bz2        # or bunzip2 file.bz2
tar -xf archive.tar      # extract tar archive
tar -tf archive.tar      # list tar contents

# File management
mv oldname newname       # rename files
mktemp -d               # create temporary directory
```

## Real-World Applications

This type of challenge simulates:
- **Malware analysis**: Unpacking nested compressed/encoded malware
- **Data recovery**: Reconstructing files from damaged archives
- **Forensics**: Analyzing layered file obfuscation
- **System administration**: Handling complex backup archives

The systematic approach of identify → rename → decompress → repeat is a fundamental skill in cybersecurity and system administration.
