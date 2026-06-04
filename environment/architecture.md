# Target Environment Architecture

## Three-Layer Cloud-Robotics Architecture

```
┌────────────────────────────────────────────────────────────┐
│  CLOUD LAYER — Machine 2 (192.168.100.6)                   │
│  Ubuntu 22.04 LTS (Jellyfish)                             │
│                                                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  AI-Driven Defect Detection                         │   │
│  │  CNN Model (PyTorch) — MNIST/defect classification  │   │
│  │  Defect decisions → dispatched to Edge Layer        │   │
│  │  Users: Sys_admin, Operator (no prod ops), Developer│   │
│  └─────────────────────────────────────────────────────┘   │
│                              ↕ SSH / Data Pipeline         │
├────────────────────────────────────────────────────────────┤
│  EDGE LAYER — Machine 1 (192.168.100.5)                    │
│  Ubuntu 22.04 LTS (Jammy), ROS2 Galactic Distribution      │
│                                                            │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ Noise        │  │ Image        │  │ Anomaly         │  │
│  │ Reduction    │  │ Enhancement  │  │ Detection       │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
│                      Local PC/Server                        │
│  Users: Sys_admin, Operator (plant mgr, QA, prod ops),     │
│         Developer (robotics eng — sudo python3, git)        │
├────────────────────────────────────────────────────────────┤
│  PHYSICAL RESOURCES LAYER                                  │
│                                                            │
│  ┌──────────────────────┐    ┌──────────────────────────┐  │
│  │  Product Inspection  │    │  Real-Time Correction    │  │
│  │  High-res vision     │    │  PX-150 Robotic Arms (2) │  │
│  │  systems             │    │  ROS2 + SROS2            │  │
│  │  Camera, Sensors     │    │  Defect Correction Node  │  │
│  └──────────────────────┘    └──────────────────────────┘  │
│              Production Line                               │
└────────────────────────────────────────────────────────────┘
        ↕ Internet / Machine 3 (Kali — Attacker, 192.168.100.x)
```

## User Groups and Privileges

| Group | Members | Machine 1 | Machine 2 | Sudo |
|-------|---------|-----------|-----------|------|
| sys_admin | IT/OT Administrators | ✓ | ✓ | ALL |
| operator | Plant Manager, QA Team, Prod Operators | ✓ | ✓ (no prod ops on M2) | None |
| developer | Robotics Engineers/Operators | ✓ | Data Scientists/AI Specialists | `/usr/bin/git, /usr/bin/python3` |

**Critical finding:** Developer group granted sudo for `python3` and `git` — direct GTFOBins root escalation path with no additional exploitation required.

## Network Architecture

- Machine 1 (`192.168.100.5`) — **Internal network** zone
- Machine 2 (`192.168.100.6`) — **Cloud network** zone
- L3 Switch (`192.168.100.1`) — default gateway
- Machine 3 (Kali) — **Internet/attacker** zone, no direct internal access
- Both VMs run VirtualBox Host-Only networking for simulation isolation

## Robotic Hardware

**PincherX-150 Robot Arm (×2)**
- Manufacturer: Interbotix X-Series
- Motors: DYNAMIXEL X-Series Smart Servo
- Communication: ROS2 over DDS (Data Distribution Service)
- Security: SROS2 (Secure ROS2) with DDS security profiles
- Documentation: https://docs.trossenrobotics.com/interbotix_xsarms_docs/specifications/px150.html

## Security Measures Deployed

| Layer | Security Controls |
|-------|------------------|
| IT | AES-256, TLS 1.3, VPNs, MFA, RBAC, anomaly detection, firewall |
| OT | OPC UA secure comms, device authentication, firmware integrity, patch management |
| Cloud | AI model protection, encrypted storage, access control, incident response |
| Robotics | SROS2, security hardening, secure component configuration |

Despite these controls, two critical architectural vulnerabilities in SROS2 and an unpatched CVE in OpenSSH created full attack paths through all three layers.
