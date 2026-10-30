# Security in Azure

## What you will learn

- Describe the Zero Trust model (M09-O1).
- Describe the defense-in-depth model (M09-O2).
- Describe the purpose of Microsoft Defender for Cloud (M09-O3).
- Describe encryption and key management options in Azure (M09-O4).

## Key ideas

### Zero Trust

**Zero Trust** is a security approach summed up as "never trust, always verify". It does not assume anything is safe because of where it sits, such as inside the corporate network. Its three principles are:

- **Verify explicitly:** check every request using all available data, such as identity, location, device health and risk.
- **Use least-privilege access:** give people only the access they need, for only as long as they need it.
- **Assume breach:** design as if an attacker may already be inside. Limit the damage by segmenting networks, encrypting data and monitoring for threats.

### Defense in depth

**Defense in depth** uses several layers of protection, so if one layer fails the others still stand in the way. The layers, from outside in, are:

1. **Physical security:** controlled access to datacenters.
2. **Identity and access:** sign-in checks, MFA and least privilege.
3. **Perimeter:** protection such as DDoS defence and firewalls at the network edge.
4. **Network:** segmentation and limiting connectivity between resources.
5. **Compute:** secure and patched virtual machines.
6. **Application:** secure code and configuration.
7. **Data:** encryption and protection of stored and transmitted information.

### Microsoft Defender for Cloud

**Microsoft Defender for Cloud** helps you strengthen and protect your environment. It assesses your **security posture**, gives a **secure score** and lists recommendations, and it detects threats and raises alerts. It covers Azure, on-premises servers and other clouds, so it supports hybrid and multicloud setups.

### Encryption and key management

Encryption makes data unreadable to anyone without the right key. **Encryption at rest** protects stored data, such as databases, disks and storage accounts. **Encryption in transit** protects data moving between services, applications and users. A strong setup uses both.

**Azure Key Vault** is the main Azure service for securely storing and controlling access to **secrets** (such as connection strings and passwords), **encryption keys** and **certificates**. It helps you control who can use them, rotate keys over time and audit how they are used. Applications can fetch secrets from Key Vault when they run, often using a managed identity, instead of keeping passwords in code or configuration files.

## How it looks in real life

A company requires MFA for every sign-in, even from the office (verify explicitly), gives developers read-only access by default (least privilege), splits its network into zones and encrypts its databases (assume breach and defense in depth). The security team opens Defender for Cloud each week to review the secure score and fix the top recommendations.

## Compare and contrast

| Idea | Key point | Easy to confuse with |
|---|---|---|
| Zero Trust | Verify every request, assume breach | Trusting the internal network |
| Defense in depth | Several protective layers | One strong firewall |
| Defender for Cloud | Posture assessment and threat detection | Azure Policy (rule enforcement) |

## Exam tips

- "Never trust, always verify" is Zero Trust.
- Defense in depth means layers; one layer failing should not expose everything.
- Defender for Cloud gives a secure score and recommendations.
- Encryption belongs to the data layer; firewalls and DDoS protection to the perimeter.
- Encryption at rest protects stored data, encryption in transit protects moving data, and Key Vault stores secrets, keys and certificates.

## Quick recap

- Zero Trust: verify explicitly, least privilege, assume breach.
- Defense in depth: physical, identity, perimeter, network, compute, application, data.
- Defender for Cloud assesses posture, recommends fixes and detects threats across Azure, hybrid and other clouds.
- Encrypt data at rest and in transit, and keep secrets, keys and certificates in Azure Key Vault.

## Go deeper

- [Zero Trust overview](https://learn.microsoft.com/security/zero-trust/zero-trust-overview)
- [Microsoft Defender for Cloud introduction](https://learn.microsoft.com/azure/defender-for-cloud/defender-for-cloud-introduction)
- [Azure Key Vault overview](https://learn.microsoft.com/azure/key-vault/general/overview)
- [Azure encryption overview](https://learn.microsoft.com/azure/security/fundamentals/encryption-overview)

Last reviewed: 2026-10-29
