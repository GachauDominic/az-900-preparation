# Cloud computing basics

## What you will learn

- Define cloud computing (M01-O1).
- Explain the shared responsibility model (M01-O2).
- Compare public, private and hybrid cloud and when to use each (M01-O3).
- Describe the consumption-based model and compare cloud pricing models (M01-O4).
- Describe serverless computing (M01-O5).
- Describe multicloud and where Azure Arc and Azure VMware Solution fit (M01-O6).

## Key ideas

### What is cloud computing?

**Cloud computing** means renting computing services (servers, storage, databases, networking, software) over the internet instead of buying and running your own hardware. The provider owns and maintains the datacenters. You create what you need in minutes and usually pay only for what you use.

### Shared responsibility

Security and operations are split between the provider and you. Some things never change:

- The provider is **always** responsible for the physical datacenter, the physical network and the physical hosts.
- You are **always** responsible for your data, your accounts and identities, and the devices people use to connect.

Everything in between, such as the operating system, network controls and applications, depends on the service type. If you run a virtual machine, you patch its operating system. If you use a software-as-a-service product, the provider does far more.

### Cloud models

- **Public cloud:** owned and run by a provider, shared by many customers, reached over the internet. No hardware to buy. Good for changing workloads, testing and fast starts.
- **Private cloud:** used by one organisation, in its own datacenter or hosted for it. You get more control and carry more cost and effort. Good when rules demand tight control of data.
- **Hybrid cloud:** public cloud combined with private or on-premises resources. Good for keeping sensitive data in-house while using the cloud for other work, or for moving to the cloud step by step.

### Consumption-based model and pricing

In the **consumption-based model** (pay-as-you-go) you pay for the resources you actually use, with no upfront hardware purchase. This turns **capital expenditure (CapEx)**, large upfront spending on equipment, into **operational expenditure (OpEx)**, spending as you go. Other pricing options trade flexibility for savings: committing to a one- or three-year reservation or savings plan lowers the price, and spare-capacity options can be cheaper but may be interrupted. Check Microsoft Learn for the current options and terms.

### Serverless

In **serverless** computing you write code or configure a service, and the provider runs it on demand, scales it automatically and bills per execution. Servers still exist; you simply do not manage them. Azure Functions is a common example.

### Multicloud, Azure Arc and Azure VMware Solution

A **multicloud** setup uses more than one public cloud provider, for example to get different features from each, or while moving from one provider to another. You then manage resources and security in each provider's environment. **Azure Arc** helps manage environments that span Azure, private datacenters, hybrid setups and other clouds. **Azure VMware Solution** lets an organisation that already runs VMware in a private environment run those VMware workloads in Azure.

## How it looks in real life

A start-up launches a web shop on public cloud and pays only for the capacity it uses. A bank keeps customer records in its own datacenter and runs its public website in the cloud, which is a hybrid design. A small team uses a serverless function to resize images whenever a customer uploads one, and it pays nothing while no images arrive.

## Compare and contrast

| Idea | Key point | Easy to confuse with |
|---|---|---|
| Public cloud | Shared provider infrastructure | Private cloud (one organisation) |
| Hybrid cloud | Public plus private or on-premises | Using two public providers |
| CapEx | Upfront equipment spending | OpEx (pay as you go) |
| Pay-as-you-go | No commitment, pay for use | Reservation (commitment for a discount) |
| Serverless | You do not manage servers | "No servers exist" |

## Exam tips

- Data, accounts and devices are always yours; the physical datacenter is always the provider's.
- "Keep some data on-premises" or "move gradually" points to hybrid.
- Moving to the cloud usually shifts spending from CapEx to OpEx.
- Serverless does not mean there are no servers.
- Multicloud means two or more public cloud providers; hybrid means public plus private or on-premises.

## Quick recap

- Cloud computing is renting services over the internet, usually pay-as-you-go.
- Responsibility is shared; the split depends on the service type.
- Public, private and hybrid models fit different control and cost needs.
- Consumption-based pricing replaces upfront CapEx with OpEx; commitments can lower the price.
- Serverless means the provider runs and scales the servers for you.
- Multicloud uses several public providers; Azure Arc and Azure VMware Solution help with hybrid and multicloud estates.

## Go deeper

- [Shared responsibility in the cloud](https://learn.microsoft.com/azure/security/fundamentals/shared-responsibility)
- [Azure Functions overview](https://learn.microsoft.com/azure/azure-functions/functions-overview)
- [Cloud Adoption Framework for Azure](https://learn.microsoft.com/azure/cloud-adoption-framework/)
- [Azure Arc overview](https://learn.microsoft.com/azure/azure-arc/overview)

Last reviewed: 2026-10-29
