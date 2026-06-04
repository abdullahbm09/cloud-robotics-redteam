# Security Assurance Framework for Business Processes

**Developed by:** Abdullah Bin Masood, Victor Cionca, Donna O'Shea — MTU Cork  
**Funded by:** Dell Technologies  
**Status:** Paper in submission, IEEE Access (April 2025)

---

## Overview

Existing Security Assurance Evaluation (SAE) methodologies focus on system-level security and fail to comprehensively evaluate business process security — particularly in dynamic Industry 4.0 environments where IT, OT, cloud, and robotics are deeply integrated.

This framework addresses that gap by combining:

1. **Structured business process mapping** (Process of Interest definition)
2. **Stakeholder-driven assurance context**
3. **MITRE ATT&CK–based threat modelling**
4. **Quantitative security assurance metrics** (not just qualitative checklists)
5. **Penetration testing–based evaluation**

---

## Framework Components

### Component 1: Security Assurance Context

The assurance context establishes the evaluation boundary — what is being evaluated, under what conditions, and with what assumptions. This is the most commonly missing element in existing SAE methodologies.

**4 elements of the assurance context:**

**1. Stakeholder Context** — identifies internal (process owners, IT/OT admins, engineers), external (regulatory bodies, customers), and third-party (security auditors, vendors) stakeholders. Each stakeholder group shapes the security requirements and evaluation scope.

**2. Business Process Context** — defines the Process of Interest (PoI): its assets, boundaries, environment, and dependencies. The PoI is the specific business process subjected to SAE evaluation (e.g., "automated quality control cloud-robotic process").

```
Operational Environment
└── Process Environment
    └── Process Assets (IT, OT, Cloud, Robotics)
        └── Process of Interest (PoI)
```

**3. Assurance Assumption Context** — explicitly documents conditions assumed to hold during evaluation (e.g., "SROS2 is properly deployed," "physical security measures are in place"). Invalid assumptions lead to flawed conclusions. Must be published alongside results.

**4. Security Concern Context** — maps the threat landscape (using MITRE ATT&CK) and compliance requirements (ISO 27001, NIST CSF, GDPR, sector-specific standards). Drives the development of realistic attack scenarios.

---

### Component 2: Cyber-Attack Scenario Development

Using the assurance context, realistic attack scenarios are constructed using MITRE ATT&CK:

1. Define the PoI and its critical assets
2. Analyse threats using historical attack intelligence
3. Map adversary TTPs using MITRE ATT&CK (Enterprise, ICS, or Mobile matrices)
4. Construct step-by-step attack sequences
5. Score scenarios using CVSS and RVSS (Robot Vulnerability Scoring System)
6. Prioritise by potential impact and likelihood

---

### Component 3: Security Assurance Evaluation Process

Security assurance is measured quantitatively rather than qualitatively:

**Assurance Metric (AM):**
```
AM = RM − VM
```

**Requirement Metric (RM):** measures how well security requirements are fulfilled
```
RM = Σ (w_i × (Σ f_ij / k))
```
Where w_i = importance weight, f_ij = GQM test case fulfillment score (0/0.5/1), k = number of test cases

**Vulnerability Metric (VM):** measures risk exposure from identified vulnerabilities
```
VM = Σ (r_i × Σ e_ij)
```
Where r_i = CVSS/RVSS risk score, e_ij = vulnerability existence factor (0/0.5/1)

**Normalisation to 0–10 scale:**
```
AM_normalised = ((AM − AM_min) / (AM_max − AM_min)) × 10
```

**Security Classification:**

| Score | Level |
|-------|-------|
| 0.0 – 0.99 | No Security |
| 1.0 – 3.9 | Low Security |
| 4.0 – 6.9 | Moderate Security |
| 7.0 – 8.9 | High Security |
| 9.0 – 10.0 | Excellent Security |

---

## How This Differs from Existing SAE Approaches

| Aspect | OpenSAMM / BSIMM / Common Criteria | This Framework |
|--------|-------------------------------------|----------------|
| Scope | System-level | Business process–level |
| Metrics | Qualitative | **Quantitative (AM = RM − VM)** |
| Threat modelling | Generic | **MITRE ATT&CK TTP-driven** |
| Assurance context | Implicit | **Explicitly defined and documented** |
| Validation | Checklist | **Penetration testing simulation** |
| Vulnerability scoring | — | **CVSS + RVSS integration** |

---

## Application to Cloud-Robotics Case Study

The framework was applied to an automated quality control cloud-robotics business process. Two attack scenarios were developed and executed:

| Scenario | Attack | AM Score | Classification |
|----------|--------|----------|----------------|
| 1 | SROS2 bypass + ROS2 command injection | 4.66/10 | Moderate Security |
| 2 | CVE-2023-38408 lateral movement + FGSM AI poisoning | 4.79/10 | Moderate Security |

Both scenarios demonstrated **Moderate Security** — a security posture that exists in name but can be defeated by a technically competent attacker exploiting architectural flaws rather than requiring zero-days or sophisticated tooling.

---

## Implementation Guidelines (UML Activity Flow)

```
Identify stakeholders
    ↓
Map business processes → select PoI
    ↓
Define PoI boundaries, assets, environment
    ↓
Formulate assurance assumptions
    ↓
Build threat landscape (MITRE ATT&CK)
    ↓
Develop cyber-attack scenarios (score with CVSS/RVSS)
    ↓
Define security requirements (GQM approach)
    ↓
Simulate selected scenarios
    ↓
Score: compute RM, VM, AM
    ↓
Generate evaluation report with mitigation recommendations
    ↓
Share with stakeholders
```

---

## References

- Katt, B. & Prasher, N. (2018). "Quantitative security assurance metrics: REST API case studies." ECSA 2018
- Wen, S-F. & Katt, B. (2024). "Exploring the role of assurance context in system security assurance evaluation." Information & Computer Security, 32(2), 159–178
- MITRE ATT&CK. https://attack.mitre.org/ (v14, 2024)
- Vilches et al. (2018). "Towards an open standard for assessing the severity of robot security vulnerabilities, the RVSS." arXiv:1807.10357
