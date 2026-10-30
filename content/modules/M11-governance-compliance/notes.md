# Governance and compliance

## What you will learn

- Describe the purpose of Microsoft Purview (M11-O1).
- Describe the purpose of Azure Policy (M11-O2).
- Describe the purpose of resource locks (M11-O3).
- Describe the purpose of the Service Trust Portal (M11-O4).

## Key ideas

### Microsoft Purview

**Microsoft Purview** is a set of data governance, risk and compliance solutions. It helps an organisation discover where its data is across on-premises systems, multiple clouds and software-as-a-service apps, classify sensitive information, track where data comes from and goes, and manage compliance risk from one place.

### Azure Policy

**Azure Policy** lets you create rules about the resources in your environment and check that they follow them. Examples: allow resources only in approved regions, allow only certain VM sizes, or require a tag on every resource.

- A **policy definition** describes the rule and what happens when it is broken, such as audit, deny or modify.
- An **initiative** groups related policies so you manage them together.
- You **assign** a policy at a scope: management group, subscription, resource group or resource. Assignments are inherited downward.
- Resources that already exist are evaluated and shown as **non-compliant** if they break the rule; they are not deleted automatically.

Policy controls what is **allowed** on resources. It does not decide who may sign in or who can act; that is RBAC.

### Resource locks

A **resource lock** stops accidental deletion or change. There are two types:

- **CanNotDelete:** authorised users can still read and modify the resource, but cannot delete it.
- **ReadOnly:** authorised users can read the resource but cannot modify or delete it.

A lock applies to everyone, whatever their role, so even an Owner must remove the lock before deleting. Locks set on a parent, such as a resource group, are inherited by the resources inside it.

### Service Trust Portal

The **Service Trust Portal** gives you content, tools and reports about Microsoft's security, privacy and compliance practices, including details of the controls and processes that protect its cloud services and customer data. Some resources need you to sign in with a Microsoft Entra work or school account and accept a non-disclosure agreement for compliance materials. In the portal, **My Library** lets you pin documents and get notified when they are updated, and **All Documents** is the place to browse everything. Reports and documents stay available to download for at least 12 months after publishing, or until a newer version replaces them.

## How it looks in real life

A company uses Azure Policy to allow resources only in two approved regions and to require a CostCenter tag. It puts a CanNotDelete lock on the production database's resource group. Its compliance team uses Microsoft Purview to find where customer data lives across its systems and to see which of it is sensitive.

## Compare and contrast

| Feature | Question it answers | Easy to confuse with |
|---|---|---|
| Azure RBAC | Who can do what? | Azure Policy |
| Azure Policy | What is allowed on resources? | RBAC |
| Resource lock | Can this be changed or deleted? | RBAC permissions |
| Microsoft Purview | Where is our data and is it governed? | Defender for Cloud (threat protection) |

## Exam tips

- "Only allow resources in these regions" is Azure Policy, not RBAC.
- A lock applies even to Owners.
- CanNotDelete still allows changes; ReadOnly does not.
- Existing non-compliant resources are reported, not removed.
- Auditors and compliance teams look for Microsoft's compliance reports in the Service Trust Portal.

## Quick recap

- Purview governs and classifies data across the whole data estate.
- Azure Policy enforces and audits rules on resources and can be grouped into initiatives.
- Resource locks prevent accidental deletion (CanNotDelete) or any change (ReadOnly).
- The Service Trust Portal is where you find Microsoft's security, privacy and compliance documents and reports.

## Go deeper

- [Azure Policy overview](https://learn.microsoft.com/azure/governance/policy/overview)
- [Lock your resources](https://learn.microsoft.com/azure/azure-resource-manager/management/lock-resources)
- [Microsoft Purview](https://learn.microsoft.com/purview/purview)
- [Get started with the Service Trust Portal](https://learn.microsoft.com/purview/get-started-with-service-trust-portal)

Last reviewed: 2026-10-29
