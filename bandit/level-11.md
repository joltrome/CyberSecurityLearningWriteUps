# Bandit Level 11 Writeup - ROT13 Decryption

## Challenge Description
The password for the next level is stored in the file **data.txt**, where all lowercase (a-z) and uppercase (A-Z) letters have been rotated by 13 positions.

## Initial Investigation
First, I examined the contents of the data.txt file to see what we're working with:

```bash
cat data.txt
```

**Output:**
```
Gur cnffjbeq vf 7k16JArUVv5LxVuJfsSVdbbtaHGlw9D4
```

The text is clearly encoded - "Gur cnffjbeq vf" doesn't look like normal English, which confirms that ROT13 encryption has been applied.

## Understanding ROT13
ROT13 is a simple letter substitution cipher that replaces each letter with the letter 13 positions after it in the alphabet. Since there are 26 letters in the alphabet, applying ROT13 twice returns the original text (13 + 13 = 26, which wraps around).

## Solution
To decode the ROT13-encrypted text, I used the `tr` (translate) command:

```bash
cat data.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m'
```

**Output:**
```
The password is 7x16WNeHIi5YkIhWsfFIqoognUTyj9Q4
```

## How the `tr` Command Works
The `tr 'A-Za-z' 'N-ZA-Mn-za-m'` transformation breaks down as follows:

### Input Character Set: `'A-Za-z'`
- `A-Z`: All uppercase letters (A, B, C, ..., Z)
- `a-z`: All lowercase letters (a, b, c, ..., z)

### Output Character Set: `'N-ZA-Mn-za-m'`
- `N-ZA-M`: Maps uppercase letters
  - A→N, B→O, C→P, ..., M→Z, N→A, O→B, ..., Z→M
- `n-za-m`: Maps lowercase letters  
  - a→n, b→o, c→p, ..., m→z, n→a, o→b, ..., z→m

### Translation Example:
- **G** (7th letter) → **T** (20th letter) - shifted by 13 positions
- **u** (21st letter) → **h** (8th letter) - shifted by 13 positions (wraps around)
- **r** (18th letter) → **e** (5th letter) - shifted by 13 positions (wraps around)

So "Gur" becomes "The"

## Key Takeaway
The `tr` command performs character-by-character translation. Each character from the first set is replaced by the corresponding character in the same position from the second set. The ROT13 transformation is achieved because the second set is the first set shifted by 13 positions.

## Solution
**Password:** `7x16WNeHIi5YkIhWsfFIqoognUTyj9Q4`
