# Command & Control (50)

## Challenge Description

Our SOC detected suspicious activity from a suspected APT group. We were provided a network capture (`CyberWar.pcap`). The task is to analyze the traffic and uncover the **C2 Server Address**.

## Analysis

We began by inspecting the PCAP with simple string extraction to quickly identify artifacts:

```bash
strings CyberWar.pcap | less
```

Among the output, several random-looking subdomains and registry-related strings appeared (common when DNS queries are logged). However, two key indicators stood out:

```
Q0JDVEZ7Y1liM1J3QHJ9
gh0stwar
```

The string `gh0stwar` appeared repeatedly, suggesting it was the suspicious hostname or identifier used by the malware for its Command & Control.

The other string `Q0JDVEZ7Y1liM1J3QHJ9` is base64-encoded.

Decoding it:

```bash
echo Q0JDVEZ7Y1liM1J3QHJ9 | base64 -d
```

Yields:

```
CBCTF{cYb3Rw@r}
```

This confirms both the C2 beacon and the hidden flag.

## Solution Steps

1. Ran `strings` on the PCAP to extract readable artifacts.

2. Identified suspicious hostname: **`gh0stwar`**.

3. Found encoded payload: `Q0JDVEZ7Y1liM1J3QHJ9`.

4. Base64 decoded it to reveal the flag.

## C2 Server Address

```
gh0stwar
```

## Flag

```
CBCTF{cYb3Rw@r}
```

## Identified Vulnerability

The traffic reveals unencrypted DNS-based beaconing to the C2 (`gh0stwar`). Attackers often use custom or random-looking domains for C2 communications.

## Remediation

* Implement DNS monitoring and filtering to detect suspicious or algorithmically generated domains.

* Deploy threat intelligence feeds to block known C2 domains.

* Use network intrusion detection systems (IDS) to catch base64 exfiltration patterns.
