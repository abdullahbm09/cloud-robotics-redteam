# Mitigations & Recommendations

Security hardening recommendations derived from both attack scenarios. Prioritised by severity and ease of implementation.

---

## Priority 1 — Critical (Implement Immediately)

### 1.1 Patch OpenSSH to ≥ 9.3p2

**Addresses:** CVE-2023-38408 (CVSS 9.8) — lateral movement between network zones

```bash
# Ubuntu
sudo apt update && sudo apt upgrade openssh-server openssh-client
ssh -V   # Verify version ≥ 9.3p2
```

**Also:** Disable SSH agent forwarding unless explicitly required per session:
```bash
# /etc/ssh/ssh_config — system-wide
ForwardAgent no

# Per-session when required:
ssh -A user@trusted-host-only
```

---

### 1.2 Restrict sudo Privileges

**Addresses:** Python/Git sudo misconfiguration enabling direct GTFOBins root escalation

The developer group must not have unrestricted sudo for Python. If Python execution under elevated privileges is genuinely required, scope it strictly:

```bash
# /etc/sudoers — WRONG (current configuration)
developer ALL=(ALL:ALL) /usr/bin/git, /usr/bin/python3

# RIGHT — restrict to specific scripts only
developer ALL=(ALL:ALL) /opt/robotics/approved_scripts/ros2_deploy.py
```

**If unrestricted Python sudo is genuinely needed:** require MFA via `pam_google_authenticator` for sudo sessions.

---

### 1.3 SROS2 Active Certificate Revocation

**Addresses:** Permission File Replacement vulnerability (CVSS 8.5)

```bash
# Implement file system protection on SROS2 keystore
# Restrict write access to SROS2 keystore to root only
chmod 700 ~/.ros/sros2_keystore
chown root:root ~/.ros/sros2_keystore

# Monitor for unexpected keystore access
auditd rule: -w ~/.ros/sros2_keystore -p rwxa -k sros2_access
```

**Longer term:** Implement a SROS2 patch or plugin that tracks and invalidates all copies of a permission file on revocation. This requires upstream ROS2 contribution.

---

### 1.4 SROS2 Forced Policy Enforcement

**Addresses:** Outdated Node Service vulnerability (CVSS 8.0)

Deploy a privileged watchdog process that enforces node policy updates:

```python
# Watchdog concept — monitors SROS2 policy changes and forces node restart
import subprocess
import time
import hashlib

def get_policy_hash(keystore_path):
    # Hash the current permission files
    ...

def force_node_restart(node_name):
    subprocess.run(['ros2', 'lifecycle', 'set', node_name, 'shutdown'])
    time.sleep(1)
    subprocess.run(['ros2', 'lifecycle', 'set', node_name, 'configure'])

# If policy hash changes, all nodes must restart within grace period
```

**Network-level fallback:** segment ROS2 traffic so that policy-non-compliant nodes can be cut off at the network layer.

---

## Priority 2 — High (Implement Within 30 Days)

### 2.1 Adversarial Training for CNN Defect Detection Model

**Addresses:** FGSM inference poisoning (V1, CVSS 9.0 in AI context)

```python
def adversarial_training_step(model, images, labels, epsilon=0.3):
    images.requires_grad = True
    outputs = model(images)
    loss = criterion(outputs, labels)
    model.zero_grad()
    loss.backward()

    # Generate FGSM perturbed samples
    perturbed = images + epsilon * images.grad.sign()
    perturbed = torch.clamp(perturbed, 0, 1)

    # Train on both clean and adversarial samples
    adv_outputs = model(perturbed.detach())
    adv_loss = criterion(adv_outputs, labels)
    return (loss + adv_loss) / 2
```

Also consider: **randomised smoothing**, **feature squeezing**, and **input preprocessing** (bit-depth reduction, spatial smoothing) as lightweight defences.

---

### 2.2 Real-Time AI Model Monitoring

**Addresses:** Absence of anomaly detection for model behaviour drift (R5 score: 2.5/10)

```python
class ModelMonitor:
    def __init__(self, baseline_accuracy, drift_threshold=0.005):
        self.baseline = baseline_accuracy
        self.threshold = drift_threshold
        self.window = []

    def check(self, current_accuracy):
        self.window.append(current_accuracy)
        if len(self.window) > 100:
            self.window.pop(0)
        rolling_avg = sum(self.window) / len(self.window)
        drift = self.baseline - rolling_avg
        if drift > self.threshold:
            self.alert(f"Model drift detected: {drift:.4f} — possible poisoning attack")

    def alert(self, message):
        # Page on-call, trigger incident response
        ...
```

**Set threshold at 0.5% accuracy drop** — below normal variance but detectable before significant operational impact.

---

### 2.3 Enhanced Authentication for Cloud AI Systems

**Addresses:** Weak access control to cloud AI (R2 — partially met)

- Enforce MFA on all cloud system SSH access (not just operator dashboard)
- Implement role-based API authentication for AI model inference endpoints
- Disable password-based SSH — key pairs only
- Implement jump host / bastion architecture for cloud access

```bash
# /etc/ssh/sshd_config on Machine 2
PasswordAuthentication no
ChallengeResponseAuthentication no
AuthenticationMethods publickey,keyboard-interactive
```

---

### 2.4 Intrusion Detection & Network Monitoring

**Addresses:** Across both scenarios — no detection capability confirmed during engagement

- Deploy **Suricata** or **Zeek** for network traffic monitoring on the L3 switch
- Write custom ROS2 detection rules: unexpected node registration, high-frequency pub on joint command topics
- Implement **pspy** or auditd rules for detecting unusual process execution on both VMs

---

## Priority 3 — Medium (Implement Within 90 Days)

### 3.1 Comprehensive Logging for AI Inference

```python
import logging
import hashlib

logging.basicConfig(filename='/var/log/ai_inference.log', level=logging.INFO)

def logged_inference(model, input_data, request_id):
    input_hash = hashlib.sha256(input_data.numpy().tobytes()).hexdigest()
    output = model(input_data)
    prediction = output.argmax().item()
    confidence = output.softmax(dim=1).max().item()
    logging.info(f"req={request_id} input_hash={input_hash} prediction={prediction} confidence={confidence:.4f}")
    return output
```

All AI inference requests should be logged with input hash, prediction, and confidence. This enables forensic analysis if poisoning is discovered post-hoc.

---

### 3.2 Data Integrity Checks for Inference Pipeline

```python
import hmac, hashlib

def verify_inference_input(data, expected_hmac, secret_key):
    computed = hmac.new(secret_key, data, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(computed, expected_hmac):
        raise SecurityException("Inference input integrity check failed — possible tampering")
```

Sign inference data at the edge layer and verify at the cloud layer before feeding to the model.

---

### 3.3 Confidence Thresholding

```python
CONFIDENCE_THRESHOLD = 0.85   # Reject low-confidence classifications

def safe_predict(model, input_data):
    output = model(input_data)
    confidence = output.softmax(dim=1).max().item()
    if confidence < CONFIDENCE_THRESHOLD:
        return "MANUAL_REVIEW_REQUIRED"
    return output.argmax().item()
```

Adversarially perturbed inputs often produce lower confidence scores. Thresholding routes uncertain classifications to human review rather than automated robotic action.

---

## Summary Table

| # | Recommendation | Addresses | Priority | Effort |
|---|---------------|-----------|----------|--------|
| 1.1 | Patch OpenSSH ≥ 9.3p2 | CVE-2023-38408 | Critical | Low |
| 1.2 | Restrict sudo for developer group | Python root escalation | Critical | Low |
| 1.3 | SROS2 keystore file protection | Permission File Replacement | Critical | Medium |
| 1.4 | Watchdog for SROS2 policy enforcement | Outdated Node Service | Critical | High |
| 2.1 | Adversarial training for CNN model | FGSM inference poisoning | High | High |
| 2.2 | Real-time model accuracy monitoring | AI drift detection | High | Medium |
| 2.3 | MFA + key-only SSH to cloud systems | Access control gaps | High | Medium |
| 2.4 | IDS/network monitoring | No detection capability | High | Medium |
| 3.1 | AI inference logging | Forensic traceability | Medium | Low |
| 3.2 | Inference input integrity (HMAC) | Data pipeline tampering | Medium | Medium |
| 3.3 | Confidence thresholding | Adversarial misclassification | Medium | Low |
