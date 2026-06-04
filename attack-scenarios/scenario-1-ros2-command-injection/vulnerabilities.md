# SROS2 Vulnerability Analysis — Scenario 1

Two zero-day-class vulnerabilities in SROS2's access control architecture were identified and exploited in this engagement. Both were previously identified in academic research (Deng et al., CCS 2022) but had not been evaluated in the context of a full attack chain against a manufacturing business process.

---

## Vulnerability 1: Permission File Replacement

**Severity:** High | **CVSS Base Score:** 8.5  
**Affected component:** SROS2 access control — permission file revocation mechanism  
**Type:** Design flaw (insufficient revocation)

### Root Cause

When an administrator updates SROS2 access control policies, SROS2 replaces the existing permission files but does not actively revoke or invalidate them. Because ROS2 nodes have read/write access to their local file system, an adversary can:

1. Back up the original permission files before revocation
2. Continue using the backed-up (expired) permission files after revocation
3. Restore them at any time to regain access to topics that were explicitly revoked

This is not a misconfiguration — it is a fundamental design limitation of how SROS2 handles certificate lifecycle management.

### Exploitation

```bash
# During initial access phase — before administrator revokes permissions
cp -r ~/.ros/sros2_keystore /tmp/.sros2_backup   # back up permission files

# After administrator updates policies and revokes access:
# Restore expired permission files
cp -r /tmp/.sros2_backup/* ~/.ros/sros2_keystore/

# Result: node retains publish/subscribe access despite revocation
ros2 topic pub /px150/commands/joint_single ...   # succeeds with expired certs
```

### Impact

Persistent unauthorised publish/subscribe access to any ROS2 topic the adversary had access to before revocation. In the defect correction context, this allows permanent injection of movement commands into the robotic arm.

### Mitigation

- Implement **active certificate revocation** — SROS2 must track and invalidate all copies of a permission file, not just replace the active one
- Use **cryptographic timestamping** on permission files — nodes should reject certificates older than a configurable threshold
- **Immutable keystore** — restrict write access to the SROS2 keystore directory to privileged system processes only

---

## Vulnerability 2: Outdated Node Service

**Severity:** High | **CVSS Base Score:** 8.0  
**Affected component:** SROS2 / DDS QoS policy synchronisation  
**Type:** Design limitation (DDS architectural constraint)

### Root Cause

DDS (Data Distribution Service) QoS policies, which underpin ROS2 communication, can only be updated during participant initialisation. This means:

- When an administrator updates SROS2 access control policies, a node must **restart** for the new policies to take effect
- A malicious node can simply **refuse to restart**, causing it to continue operating under old (permissive) policies indefinitely
- There is no mechanism to force an external restart of a non-cooperative node

### Exploitation

```python
# A malicious node that ignores SIGTERM and SIGINT, preventing administrator restart:
import signal

def ignore_signal(signum, frame):
    pass   # Do nothing — refuse to shut down

signal.signal(signal.SIGTERM, ignore_signal)
signal.signal(signal.SIGINT, ignore_signal)

# Node continues running with old DDS QoS policies
# New SROS2 policies are never applied
```

### Impact

Even after an administrator correctly updates security policies to revoke the adversary's access, the malicious node continues to publish/subscribe under the old permissions. The security policy update is completely ineffective until the node is forcibly killed (which requires root access and creates operational disruption).

### Mitigation

- **Real-time policy enforcement:** Implement a DDS security plugin that enforces policy updates at the middleware level without requiring node restart
- **Watchdog process:** Deploy a privileged watchdog that can force-restart any node that does not acknowledge policy updates within a configurable timeout
- **Network-level enforcement:** Use network segmentation to cut off a node's communication channel as a fallback when software-level policy enforcement fails

---

## Combined Exploitation Impact

When both vulnerabilities are exploited together, the attacker achieves:

1. **Persistent access** — Permission File Replacement ensures certificates survive revocation
2. **Policy bypass** — Outdated Node Service prevents new restrictions from applying
3. **Stealthy persistence** — The adversarial node appears to be a legitimate ROS2 participant in `ros2 node list`

The combination creates a window of potentially **indefinite unauthorised access** that cannot be closed through normal SROS2 policy management.

---

## Additional SROS2 Communication Vulnerabilities

Beyond the two exploited vulnerabilities, the following communication-level weaknesses were identified in the SROS2 architecture (Yang et al., IEEE Access 2024):

| Vulnerability Type | Confidentiality | Integrity | Availability |
|-------------------|----------------|-----------|--------------|
| Stealing topic data | Compromised | Maintained | Maintained |
| Unauthorised subscription | Compromised | Maintained | Compromised |
| Unauthorised publication | Compromised | Compromised | Compromised |
| Stealing service data | Compromised | Maintained | Maintained |
| Unauthorised service call | Compromised | Compromised | Compromised |
| Stealing action data | Compromised | Maintained | Maintained |
| Unauthorised action service | Compromised | Compromised | Compromised |

These weaknesses confirm that SROS2, while an improvement over unsecured ROS2, does not provide strong security guarantees in the presence of a compromised insider node.

---

## References

- Deng, G. et al. "On the (in)security of secure ROS2." ACM CCS 2022, pp. 739–753
- Yang, J. et al. "Formal-guided fuzz testing: Targeting security assurance from specification to implementation for 5G and beyond." IEEE Access, 2024
- Open Robotics. "ROS 2 Robotic Systems Threat Model." design.ros2.org, 2019
