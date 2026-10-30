# Cloud service types

## What you will learn

- Describe infrastructure as a service (M03-O1).
- Describe platform as a service (M03-O2).
- Describe software as a service (M03-O3).
- Choose the right service type for a scenario (M03-O4).

## Key ideas

### Three service types

The service types differ in how much you manage and how much the provider manages.

**Infrastructure as a service (IaaS)** gives you basic building blocks: virtual machines, storage and networks. The provider runs the hardware and virtualization; you manage the operating system, runtime, applications and data. You get the most control and the most work.

**Platform as a service (PaaS)** gives you a ready-made environment for building and running applications. The provider manages the servers, operating system and runtime; you manage your application and data. You focus on code.

**Software as a service (SaaS)** is finished software you use over the internet. The provider manages almost everything; you manage your data, your users and how you configure and use it.

### Who manages what

| Layer | IaaS | PaaS | SaaS |
|---|---|---|---|
| Applications and data | You | You (application and data) | Provider runs the app; you manage your data and settings |
| Runtime and operating system | You | Provider | Provider |
| Servers, storage, network, datacenter | Provider | Provider | Provider |

### Choosing a service type

- **IaaS** fits moving an existing application unchanged ("lift and shift"), needing full control of the operating system, or building test environments quickly.
- **PaaS** fits building and hosting web apps, APIs and databases without managing servers.
- **SaaS** fits using ready-made tools for email, collaboration or business management.

### Azure examples

- IaaS: Azure Virtual Machines.
- PaaS: Azure App Service and Azure SQL Database.
- SaaS: Microsoft 365 and Dynamics 365.

## How it looks in real life

A company moves an old accounting program to Azure virtual machines because it needs a specific operating system setup (IaaS). Its developers publish a new customer portal on Azure App Service without ever touching a server (PaaS). Everyone in the company uses Microsoft 365 for email and documents, and nobody installs or patches it (SaaS).

## Compare and contrast

| Type | You manage | Typical use |
|---|---|---|
| IaaS | OS, runtime, apps, data | Lift and shift, full control |
| PaaS | Apps and data | Building and hosting apps |
| SaaS | Your data, users and settings | Ready-made business tools |

## Exam tips

- More control means IaaS; less management means SaaS; PaaS sits in the middle.
- "Without managing servers or the operating system" points to PaaS (or serverless).
- "Move an existing app with minimal change" points to IaaS.
- Azure Virtual Machines are IaaS, not PaaS.

## Quick recap

- IaaS rents infrastructure; you manage everything above it.
- PaaS provides a platform; you manage the app and data.
- SaaS delivers finished software; you manage your data and settings.
- Match the service type to the amount of control and effort the scenario needs.

## Go deeper

- [Azure training on Microsoft Learn](https://learn.microsoft.com/training/azure/)
- [Cloud Adoption Framework for Azure](https://learn.microsoft.com/azure/cloud-adoption-framework/)

Last reviewed: 2026-10-29
