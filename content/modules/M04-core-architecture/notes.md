# Core architecture of Azure

## What you will learn

- Explain what regions, region pairs and sovereign regions are (M04-O1).
- Describe availability zones and how they relate to datacenters (M04-O2).
- Explain resources and resource groups (M04-O3).
- Describe subscriptions, management groups and how they stack (M04-O4).
- Explain what Azure is and how accounts, subscriptions and the free account work (M04-O5).

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

### What is Azure, and how do you get started?

**Microsoft Azure** is Microsoft's cloud platform. It offers a wide range of services, such as compute, networking, storage, identity, analytics and AI, which you use and pay for as you need them.

To create resources you need an **Azure subscription**. When you create an **Azure account**, a subscription is created for you, and you can add more later, for example separate subscriptions for development, testing and production. Resources are then created inside a subscription.

New users can try Azure with a **free account**. It includes free access to popular products for 12 months, a credit for the first 30 days and a set of services that stay free. Signing up needs a phone number, a payment card and a Microsoft or GitHub account; the card is used to verify identity, and you are not charged until you upgrade to a paid subscription. Students can use a **free student account**, which offers a credit and free developer tools without needing a payment card. Offers change, so check Microsoft's site for current terms. If you practise by creating resources, watch your usage and delete what you no longer need to avoid surprise costs.

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
- An Azure account gives you a subscription, and resources live inside subscriptions.

## Quick recap

- Regions are groups of datacenters; many are paired for large-outage recovery.
- Sovereign regions are isolated Azure instances for strict compliance needs.
- Availability zones are separate locations in a region with their own power, cooling and networking.
- Resource groups hold related resources; subscriptions bill and control access; management groups organise subscriptions.
- Azure is Microsoft's cloud platform; an account comes with a subscription, and free and student accounts let you practise.

## Go deeper

- [Azure region pairs](https://learn.microsoft.com/azure/reliability/regions-paired)
- [Availability zones overview](https://learn.microsoft.com/azure/reliability/availability-zones-overview)
- [Management groups overview](https://learn.microsoft.com/azure/governance/management-groups/overview)
- [Create an additional Azure subscription](https://learn.microsoft.com/azure/cost-management-billing/manage/create-subscription)

Last reviewed: 2026-10-29
