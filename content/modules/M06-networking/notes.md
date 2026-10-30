# Networking services

## What you will learn

- Explain virtual networks and subnets (M06-O1).
- Describe virtual network peering (M06-O2).
- Compare VPN Gateway and ExpressRoute (M06-O3).
- Describe Azure DNS (M06-O4).
- Compare public and private endpoints (M06-O5).
- Describe how traffic is routed and filtered, including network security groups (M06-O6).

## Key ideas

### Virtual networks and subnets

An **Azure virtual network (VNet)** is your private network in Azure. Resources in it can talk to each other, to the internet and to your on-premises network, and the network is isolated from other customers. By default, resources in the same VNet can communicate.

A **subnet** is a range of IP addresses inside a VNet. You split a VNet into subnets to organise and secure resources, for example one for web servers and one for databases.

### Peering

**Virtual network peering** connects two VNets so their resources communicate privately using private IP addresses. Traffic travels over Microsoft's backbone network, not the public internet, with low latency. VNets in different regions can be peered. Their address ranges must not overlap.

### Connecting on-premises networks

- **VPN Gateway** sends encrypted traffic between Azure and another network **over the public internet**. It is quick to set up and relatively low cost.
- **ExpressRoute** is a **private connection** through a connectivity provider that does not travel over the public internet. It offers more reliability, consistent latency and higher speeds, and usually costs more.

### Azure DNS

**Azure DNS** hosts your DNS domains on Azure infrastructure. It translates names such as www.contoso.com into IP addresses, and you manage DNS records with the same tools and billing as other Azure resources.

### Public and private endpoints

A **public endpoint** is reachable over the internet through a public IP address. A **private endpoint** is a network interface with a private IP address from your VNet that connects you privately to an Azure service, so the traffic stays off the public internet.

### VPN connection types

A **point-to-site** VPN lets a single computer outside your network start an encrypted connection to an Azure virtual network. A **site-to-site** VPN links an on-premises VPN device to an Azure VPN gateway, so Azure resources can appear to be on your local network; the connection is encrypted and runs over the internet.

### Service endpoints

**Service endpoints** connect a virtual network to Azure services such as storage accounts and Azure SQL Database over Azure's network, improving security and giving optimal routing between those resources.

### Routing and filtering traffic

By default Azure routes traffic between subnets, connected virtual networks, on-premises networks and the internet. You can take control with **route tables** and **user-defined routes (UDR)**, and **Border Gateway Protocol (BGP)** can bring on-premises routes into Azure through VPN gateways, Azure Route Server or ExpressRoute.

To **filter** traffic you can use **network security groups (NSGs)**, which hold inbound and outbound rules that allow or block traffic by source and destination address, port and protocol. **Network virtual appliances** are specialised virtual machines that perform a network function, such as acting as a firewall. To accept connections from the internet, give a resource a public IP address or place it behind a public load balancer.

## How it looks in real life

A company places its web servers in one subnet and its database in another. Its head office connects to Azure through a VPN Gateway at first, then moves to ExpressRoute when it needs steadier performance. It uses a private endpoint so the storage account holding invoices is reachable only from inside the VNet.

## Compare and contrast

| Option | Path | Key point |
|---|---|---|
| VNet peering | Microsoft backbone | Connects two VNets |
| VPN Gateway | Public internet, encrypted | Fast to set up, lower cost |
| ExpressRoute | Private connection | Consistent latency, higher cost |
| Public endpoint | Internet | Reachable by anyone allowed |
| Private endpoint | Your VNet | Private IP address |

## Exam tips

- ExpressRoute does not use the public internet; VPN Gateway does (encrypted).
- Peering connects VNets with each other; gateways connect to on-premises.
- Private endpoint means a private IP address in your VNet.
- Peered networks must not have overlapping address ranges.
- An NSG filters traffic with allow and deny rules; route tables and UDRs decide where traffic goes.

## Quick recap

- A VNet is a private network; subnets divide it.
- Peering joins VNets over the Microsoft backbone.
- VPN Gateway is encrypted over the internet; ExpressRoute is private.
- Azure DNS hosts domains; private endpoints keep service traffic private.
- NSGs filter traffic; route tables and UDRs control routing; service endpoints link a VNet to Azure services; point-to-site and site-to-site are the VPN types.

## Go deeper

- [Virtual network overview](https://learn.microsoft.com/azure/virtual-network/virtual-networks-overview)
- [ExpressRoute introduction](https://learn.microsoft.com/azure/expressroute/expressroute-introduction)
- [Private endpoint overview](https://learn.microsoft.com/azure/private-link/private-endpoint-overview)
- [Network security groups](https://learn.microsoft.com/azure/virtual-network/network-security-groups-overview)
- [Virtual network traffic routing](https://learn.microsoft.com/azure/virtual-network/virtual-networks-udr-overview)
- [Virtual network service endpoints](https://learn.microsoft.com/azure/virtual-network/virtual-network-service-endpoints-overview)

Last reviewed: 2026-10-29
