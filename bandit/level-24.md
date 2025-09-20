# Bandit Level 24 → 25 - Brute Force Attack with Network Automation

## Challenge Description
A daemon is listening on port 30002 and will give you the password for bandit25 if given the password for bandit24 and a secret numeric 4-digit pincode. There is no way to retrieve the pincode except by going through all of the 10000 combinations, called brute-forcing. You do not need to create new connections each time.

## Solution

### Step 1: Understanding the Challenge
This level introduces **brute force attacks** - systematically trying all possible combinations until finding the correct one. Key requirements:
- Service on port 30002 expects bandit24 password + 4-digit PIN
- Must try all combinations from 0000 to 9999 (10,000 total)
- Can use a single connection for all attempts
- Need to automate the process

### Step 2: Manual Service Testing
First, I tested the service manually to understand its behavior:
```bash
nc localhost 30002
```

**Service response:**
```
I am the pincode checker for user bandit25. Please enter the password for user bandit24 and the secret pincode on a single line, separated by a space.
```

I tested with a sample PIN:
```
gb8KRRCsshuZXI0tUuR6ypOFjiZbf3G8 1111
```

**Response:**
```
Wrong! Please enter the correct current password and pincode. Try again.
```

**Key observations:**
- **Format**: `password pincode` separated by a space
- **Connection persistence**: Service keeps connection open for multiple attempts
- **Clear feedback**: Service tells you when attempts are wrong
- **Continuous operation**: Can keep trying without reconnecting

### Step 3: Understanding the Brute Force Requirements
**Scope of attack:**
- 4-digit PIN codes: 0000 through 9999
- Total combinations: 10,000
- Format requirement: Leading zeros needed (0001, not 1)

**Automation needs:**
- Generate all 10,000 combinations
- Format each as "password pincode"
- Send all through single network connection
- Monitor for success response

### Step 4: Developing the Brute Force Strategy
I needed to create a script that would:
1. Generate all PIN combinations with proper formatting
2. Combine each PIN with the known password
3. Send all combinations through one netcat connection
4. Continue until finding the correct PIN

### Step 5: Implementation
I used a bash for-loop with printf formatting to generate all combinations:

```bash
for i in {0..9999}; do printf "gb8KRRCsshuZXI0tUuR6ypOFjiZbf3G8 %04d\n" $i; done | nc localhost 30002
```

**Breaking down the command:**
- `for i in {0..9999}` - Loop through numbers 0 to 9999
- `printf "gb8KRRCsshuZXI0tUuR6ypOFjiZbf3G8 %04d\n" $i` - Format each number with leading zeros
- `%04d` - Format as 4-digit decimal with leading zeros
- `\n` - Add newline after each combination
- `| nc localhost 30002` - Pipe all output to netcat connection

### Step 6: Execution and Success
The script automatically:
1. Generated all 10,000 combinations
2. Sent each one to the service
3. Continued until finding the correct PIN
4. Received the bandit25 password when successful

**Success!** The correct PIN was discovered and the service provided the next level's password.

## Key Learning Points

### 1. Brute Force Attack Fundamentals
- **Definition**: Systematically trying all possible combinations
- **Use cases**: When no other method exists to discover the secret
- **Efficiency**: Automation is essential for large search spaces
- **Success guarantee**: Will eventually find the answer if it exists in the search space

### 2. Network Service Interaction
- **Connection management**: Understanding when to maintain vs. create new connections
- **Protocol understanding**: Learning service input/output formats through testing
- **Persistent connections**: More efficient than repeatedly connecting/disconnecting
- **Response analysis**: Distinguishing between failure and success responses

### 3. Bash Automation Techniques
- **Loop structures**: `for i in {start..end}` for generating sequences
- **Printf formatting**: `%04d` for zero-padded decimal numbers
- **Output redirection**: Using pipes (`|`) to chain commands
- **Command composition**: Combining generation and network communication

### 4. The Power of Unix Pipes
- **Data flow**: Output of one command becomes input of another
- **Single connection**: All generated data flows through one netcat session
- **Efficiency**: No need for temporary files or complex scripting
- **Modularity**: Each part of the pipeline has a single responsibility

### 5. Problem-Solving Methodology
- **Manual testing first**: Understand the system before automating
- **Format discovery**: Learn exact input requirements through experimentation
- **Incremental development**: Build and test small pieces before full automation
- **Patience in brute force**: Accept that some problems require exhaustive search

## Command Summary
```bash
# Manual testing
nc localhost 30002
# Input: gb8KRRCsshuZXI0tUuR6ypOFjiZbf3G8 1111

# Automated brute force
for i in {0..9999}; do printf "gb8KRRCsshuZXI0tUuR6ypOFjiZbf3G8 %04d\n" $i; done | nc localhost 30002
```

## Optimization Considerations

### 1. Connection Efficiency
- **Single connection**: Avoiding connection overhead for each attempt
- **Batch processing**: Sending multiple attempts without waiting for individual responses
- **Network buffering**: Understanding how data flows through network connections

### 2. Search Strategy
- **Sequential search**: Starting from 0000 and incrementing
- **Random search**: Could randomize order but no advantage here
- **Parallel attack**: Could use multiple connections (not needed for this level)

### 3. Response Handling
- **Success detection**: Monitoring output for different response patterns
- **Early termination**: Stopping when success is detected
- **Error handling**: Dealing with network issues or service problems

## Real-World Applications

### 1. Password Security Testing
- **PIN code vulnerability**: Testing numeric passcodes for weakness
- **Brute force resistance**: Evaluating how systems handle automated attacks
- **Rate limiting**: Understanding defenses against brute force attacks
- **Account lockout**: Testing security measures that prevent brute forcing

### 2. Penetration Testing
- **Service enumeration**: Testing network services for weak authentication
- **Automated exploitation**: Using scripts to exploit discovered vulnerabilities
- **Credential attacks**: Systematic testing of login credentials
- **Documentation**: Recording attack methods and success rates

### 3. Security Awareness
- **Attack demonstration**: Showing how quickly weak PINs can be broken
- **Defense evaluation**: Testing effectiveness of security controls
- **Policy development**: Informing password/PIN complexity requirements
- **Training material**: Demonstrating real attack techniques

### 4. Defensive Measures
- **Rate limiting**: Implementing delays between failed attempts
- **Account lockout**: Temporary or permanent lockout after failures
- **Strong authentication**: Requiring longer, more complex codes
- **Multi-factor authentication**: Adding additional authentication factors

This level effectively demonstrates both the power and simplicity of brute force attacks, while highlighting the importance of strong authentication mechanisms and proper defensive measures.
