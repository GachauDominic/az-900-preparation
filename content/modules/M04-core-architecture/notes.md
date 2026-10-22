# Core architecture of Azure

## What you will learn

- Explain what regions, region pairs and sovereign regions are (M04-O1).
- Describe availability zones and how they relate to datacenters (M04-O2).
- Explain resources and resource groups (M04-O3).
- Describe subscriptions, management groups and how they stack (M04-O4).
- Explain what Azure Resource Manager does (M04-O5).

## Key ideas

### Regions

An **Azure region** is a set of datacenters placed close together and joined by a fast, dedicated network. When you create most resources you pick a region, usually the one closest to your users or the one that meets your data rules. Not every service is offered in every region, so check availability before you plan.

Many regions are **paired** with another region in the same geography. Pairs are usually hundreds of miles apart. If a very large outage hits, Azure prioritises restoring one region from each pair first. Some services, such as geo-redundant storage, use the pair as the place for a backup copy. Pairing does not copy everything automatically; each service decides what it replicates.

**Sovereign regions** are separate Azure instances built for strict legal or compliance needs, for example Azure Government for US government bodies. They are isolated from the public Azure cloud.

### Availability zones and datacenters

A **datacenter** is the physical building full of servers, storage and networking. An **availability zone** is a physically separate location inside a region made of one or more datacenters, with its own power, cooling and networking. Regions that support zones have at least three. If one zone fails, the others keep running.

You choose zones when you create a resource, for example a virtual machine in zone 1 and another in zone 2. That protects you from a datacenter problem without leaving the region. Not every region has availability zones.

### Resources and resource groups

A **resource** is anything you create and manage in Azure: a virtual machine, a storage account, a virtual network, a database. A **resource group** is a logical container for related resources. Rules to remember:

- Every resource lives in exactly one resource group.
- Resource groups cannot be nested inside each other.
- Deleting a resource group deletes everything inside it.
- The resources in a group can be in different regions. The group's own location only says where its metadata is stored.

Groups usually follow a lifecycle: things that are deployed, updated and deleted together belong together.

### Subscriptions and management groups

A **subscription** is the unit where you get billed and where access is controlled. Organisations use several subscriptions to separate teams, projects or environments such as testing and production.

**Management groups** sit above subscriptions. They let you apply policies and access rules once and have them inherited by every subscription underneath, which saves a lot of repeated work in large organisations.

The full hierarchy, from broadest to narrowest, is: management group, subscription, resource group, resource.

### Azure Resource Manager

**Azure Resource Manager (ARM)** is the service that receives every request to create, update or delete resources. The Azure portal, Azure CLI, Azure PowerShell, REST APIs and SDKs all talk to ARM, so you get the same result whichever tool you use. ARM also applies access control, tags and locks, and it can deploy from declarative templates that describe the end state you want.

## How it looks in real life

A retail company runs an online shop. It keeps two subscriptions, one for testing and one for production, both under a management group that enforces company policy. The production web servers sit in two availability zones in one region, so a datacenter power failure does not take the shop offline. Everything for the shop lives in one resource group, so the team can remove a test copy by deleting a single group. Creating that group from the command line looks like this:

```bash
az group create --name rg-shop-test --location westeurope
```

## Compare and contrast

| Concept | What it is | Easy to confuse with |
|---|---|---|
| Region | Set of datacenters in one area | Datacenter (a single facility) |
| Region pair | Two regions in one geography | Availability zones (inside one region) |
| Availability zone | Separate location inside a region | Region pair |
| Resource group | Logical container for resources | Subscription (billing and access boundary) |
| Management group | Container for subscriptions | Resource group (holds resources, not subscriptions) |

## Exam tips

- Zones protect you **inside** a region. Region pairs protect you **across** regions.
- A resource is in one group only, but that group can hold resources from many regions.
- Management groups contain subscriptions, never the other way round.
- Read scenario questions for the clue words: "compliance and isolated" points to sovereign regions; "datacenter failure, same region" points to availability zones; "apply policy to many subscriptions" points to management groups.

## Quick recap

- Regions are groups of datacenters; many are paired for large-outage recovery.
- Sovereign regions are isolated Azure instances for strict compliance needs.
- Availability zones are separate locations in a region with their own power, cooling and networking.
- Resource groups hold related resources; subscriptions bill and control access; management groups organise subscriptions.
- Azure Resource Manager processes every management request, whatever tool you use.

## Go deeper

- [Azure region pairs](https://learn.microsoft.com/azure/reliability/regions-paired)
- [Availability zones overview](https://learn.microsoft.com/azure/reliability/availability-zones-overview)
- [Management groups overview](https://learn.microsoft.com/azure/governance/management-groups/overview)
- [Azure Resource Manager overview](https://learn.microsoft.com/azure/azure-resource-manager/management/overview)

Last reviewed: 2026-10-22
