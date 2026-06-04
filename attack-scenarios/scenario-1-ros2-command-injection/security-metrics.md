# Security Assurance Metrics — Scenario 1

Quantitative evaluation of the defect correction process security posture under the ROS2 command injection attack, using the Security Assurance Metrics model (Katt & Prasher, 2018) adapted for this framework.

**Formula:** `AM = RM − VM` where AM = Assurance Metric, RM = Requirement Metric, VM = Vulnerability Metric

---

## Security Requirements (R1–R6)

Six security requirements were defined for the ROS2-based defect correction process:

| ID | Requirement | Description |
|----|-------------|-------------|
| R1 | System Completeness | Every ROS2 node must have enforced access control rules |
| R2 | Topic Utilisation | All topics must have at least one authorised publisher and subscriber |
| R3 | Consistent Publishing Access | Publishing permissions must match system owner declarations |
| R4 | Consistent Subscription Access | Subscription permissions must match system owner declarations |
| R5 | Resource Management | Publish/subscribe only permitted to authorised nodes |
| R6 | Privacy & Confidentiality | Subscribers cannot infer information from unauthorised topics |

---

## Requirement Metric (RM) Calculation

Using the GQM (Goal Question Metric) approach, each requirement is evaluated with test cases. Fulfillment factors: 0 = Not Met, 0.5 = Partially Met, 1 = Met. Weight (w) = 10 for all requirements (equal criticality).

| Requirement | Test Case | Score (f) | Rationale |
|-------------|-----------|-----------|-----------|
| R1 | Does every node have an access control rule? | **0.5** | Partially met — some nodes allow access via expired certs |
| R2 | Are all topics properly utilised? | **0.5** | Partially met — outdated permissions allow unauthorised topic persistence |
| R3 | Are publishing rules enforced per security policy? | **0.0** | Not met — adversary exploits Permission File Replacement to inject commands |
| R4 | Are subscription rules enforced per security policy? | **0.0** | Not met — adversary retains subscription via outdated certificates |
| R5 | Does the system prevent unauthorised resource access? | **0.5** | Partially met — access control bypass possible via authentication flaws |
| R6 | Can adversarial nodes infer unauthorised information? | **0.0** | Not met — adversary intercepts trajectory data via compromised nodes |

**Requirement Metric (RM):**

```
RM = (10 × 0.5) + (10 × 0.5) + (10 × 0.0) + (10 × 0.0) + (10 × 0.5) + (10 × 0.0)
RM = 5 + 5 + 0 + 0 + 5 + 0 = 15
```

---

## Vulnerability Metric (VM) Calculation

Two vulnerabilities exploited in this scenario, scored with RVSS (Robot Vulnerability Scoring System):

| Vulnerability | Description | Existence (e) | Risk Score (RVSS/r) |
|--------------|-------------|---------------|---------------------|
| V1: Permission File Replacement | Expired SROS2 certificates reused after revocation | **1.0** (fully confirmed and exploited) | **8.5** (High — persistent unauthorised access) |
| V2: Outdated Node Service | Malicious node prevents policy enforcement by refusing restart | **1.0** (fully confirmed and exploited) | **8.0** (High — prolonged unauthorised access) |

**Vulnerability Metric (VM):**

```
VM = (8.5 × 1.0) + (8.0 × 1.0)
VM = 8.5 + 8.0 = 16.5
```

---

## Assurance Metric (AM) — Raw

```
AM = RM − VM = 15 − 16.5 = −1.5
```

**Interpretation:** Negative AM confirms that vulnerabilities outweigh implemented security controls. The security posture is critically exposed in the presence of this attack.

---

## Normalisation (0–10 scale)

Applying Min-Max Normalisation:

```
AM_normalised = (AM − AM_min) / (AM_max − AM_min) × 10
AM_normalised = (−1.5 + 90) / (100 + 90) × 10
AM_normalised = 88.5 / 190 × 10 = 4.66
```

Where AM_min = −90 (all requirements unmet, all vulnerabilities present at max risk) and AM_max = 100 (all requirements fully met, no vulnerabilities).

---

## Security Assurance Classification

| Score Range | Classification |
|-------------|----------------|
| 0.0 – 0.99 | No Security |
| 1.0 – 3.9 | Low Security |
| **4.0 – 6.9** | **Moderate Security** |
| 7.0 – 8.9 | High Security |
| 9.0 – 10.0 | Excellent Security |

**Score: 4.66 → Moderate Security**

This classification indicates a partially implemented security posture where certain controls exist (partial access control, some topic enforcement) but critical vulnerabilities in SROS2's certificate management and policy synchronisation create significant exploitable gaps.

---

## Summary

| Metric | Value |
|--------|-------|
| RM (Requirement Metric) | 15 / 60 (25% fulfillment) |
| VM (Vulnerability Metric) | 16.5 |
| AM (Raw Assurance Metric) | −1.5 |
| AM (Normalised) | **4.66 / 10** |
| Classification | **Moderate Security** |
| Primary gap | SROS2 certificate revocation and policy synchronisation |
