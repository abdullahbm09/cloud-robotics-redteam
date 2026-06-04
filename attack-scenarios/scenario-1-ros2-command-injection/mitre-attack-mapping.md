# MITRE ATT&CK Mapping — Scenario 1: ROS2 Command Injection

**Target:** Cloud-robotic defect correction process (Edge/Physical layer)  
**Framework version:** MITRE ATT&CK Enterprise v14

---

## Full TTP Table

| # | Tactic | Tactic ID | Technique | Sub-technique | ID | Description |
|---|--------|-----------|-----------|---------------|-----|-------------|
| 1 | Reconnaissance | TA0043 | Active Scanning | Scanning IP Blocks | T1595.001 | Nmap scan of target IP range to identify open SSH port 22 |
| 2 | Reconnaissance | TA0043 | Gather Victim Identity Information | Email Addresses | T1589.002 | LinkedIn/company OSINT to identify developer group members with SSH access |
| 3 | Reconnaissance | TA0043 | Phishing for Information | Spearphishing Attachment | T1598.002 | Malicious attachment sent to robotics engineer |
| 4 | Reconnaissance | TA0043 | Phishing for Information | Spearphishing Service | T1598.003 | Spoofed login page to capture SSH credentials |
| 5 | Initial Access | TA0001 | Valid Accounts | — | T1078 | SSH login using credentials obtained via phishing |
| 6 | Initial Access | TA0001 | Phishing | Spearphishing Attachment | T1566.001 | Credential delivery via malicious email attachment |
| 7 | Initial Access | TA0001 | Phishing | Spearphishing Link | T1566.002 | Spoofed SSH login portal |
| 8 | Privilege Escalation | TA0004 | Abuse Elevation Control Mechanism | Sudo and Sudo Caching | T1548.003 | `sudo python3 -c 'import os; os.system("/bin/sh")'` → root |
| 9 | Discovery | TA0007 | Account Discovery | Local Account | T1087.001 | `cat /etc/passwd` — enumerate local user accounts |
| 10 | Discovery | TA0007 | Account Discovery | Domain Account | T1087.002 | Enumerate group memberships (sys_admin, operator, developer) |
| 11 | Discovery | TA0007 | File and Directory Discovery | — | T1083 | Locate SROS2 keystore, permission files, configuration |
| 12 | Discovery | TA0007 | Network Service Discovery | — | T1046 | `netstat -tulnp` — identify running services |
| 13 | Discovery | TA0007 | Process Discovery | — | T1057 | Enumerate running ROS2 nodes and processes |
| 14 | Discovery | TA0007 | Remote System Discovery | — | T1018 | Identify Machine 2 (cloud VM) at 192.168.100.6 |
| 15 | Discovery | TA0007 | Software Discovery | Security Software Discovery | T1518.001 | Identify SROS2 deployment and DDS middleware |
| 16 | Discovery | TA0007 | Password Policy Discovery | — | T1201 | Assess password complexity policies |
| 17 | Persistence | TA0003 | External Remote Services | — | T1133 | Retain SSH access via valid accounts |
| 18 | Persistence | TA0003 | Valid Accounts | Local Accounts | T1078.003 | Reuse developer group account for persistent access |
| 19 | Credential Access | TA0006 | Credentials from Password Stores | — | T1555 | Search for stored private keys in filesystem |
| 20 | Credential Access | TA0006 | Exploitation for Credential Access | — | T1212 | Exploit SROS2 permission handling to access credentials |
| 21 | Credential Access | TA0006 | Unsecured Credentials | Private Keys | T1552.004 | Locate SROS2 DDS private keys on disk |
| 22 | Credential Access | TA0006 | Unsecured Credentials | Credentials In Files | T1552.001 | Locate SROS2 permission XML files |
| 23 | Credential Access | TA0006 | Steal or Forge Authentication Certificates | — | T1649 | Back up expired SROS2 certificates for reuse after revocation |
| 24 | Defense Evasion | TA0005 | Impersonation | — | T1656 | Adversarial node impersonates legitimate ROS2 node |
| 25 | Defense Evasion | TA0005 | Subvert Trust Controls | Code Signing | T1553.002 | Bypass SROS2 certificate verification using expired certs |
| 26 | Defense Evasion | TA0005 | Hijack Execution Flow | — | T1574 | Prevent legitimate node restart to block policy enforcement |
| 27 | Defense Evasion | TA0005 | Impair Defenses | — | T1562 | Suppress SROS2 policy update enforcement |
| 28 | Execution | TA0002 | Command and Scripting Interpreter | Python | T1059.006 | Deploy adversarial_node.py via compromised Python interpreter |
| 29 | Impact | TA0040 | Data Manipulation | Stored Data Manipulation | T1565.001 | Overwrite cached SROS2 permission files |
| 30 | Impact | TA0040 | Data Manipulation | Transmitted Data Manipulation | T1565.002 | Inject malicious joint commands into `/px150/commands/joint_single` |
| 31 | Impact | TA0040 | Data Manipulation | Runtime Data Manipulation | T1565.003 | Override real-time robotic arm trajectory at 20Hz command rate |
| 32 | Impact | TA0040 | Endpoint Denial of Service | Application Exhaustion Flood | T1499.002 | Lock robotic arm in holding position, blocking defect correction |
| 33 | Impact | TA0040 | Endpoint Denial of Service | Application or System Exploitation | T1499.003 | DoS via continuous adversarial publish overriding legitimate commands |

---

## Kill Chain Mapping (Lockheed Martin CKC)

```
Reconnaissance → Weaponisation → Delivery → Exploitation → Installation → C2 → Actions on Objectives
     ↓                ↓              ↓             ↓               ↓           ↓           ↓
  OSINT +        Spearphishing    Malicious     SSH creds      Root via    Adversarial  Robotic arm
  Nmap scan      campaign         email/link    obtained       Python sudo    node        manipulation
                                                               GTFOBins     deployed     + DoS
```

---

## MITRE ATT&CK Navigator Layer

Tactics covered in this scenario:

- **TA0043** Reconnaissance (4 techniques)
- **TA0001** Initial Access (2 techniques)
- **TA0004** Privilege Escalation (1 technique)
- **TA0007** Discovery (8 techniques)
- **TA0003** Persistence (2 techniques)
- **TA0006** Credential Access (4 techniques)
- **TA0005** Defense Evasion (4 techniques)
- **TA0002** Execution (1 technique)
- **TA0040** Impact (5 techniques)

**Total: 9 tactics, 33 techniques/sub-techniques**
