# Coverage of the three Microsoft Learn learning paths

Checked on 2026-10-29 against the live Microsoft Learn pages for:

1. Introduction to Cloud Infrastructure: Describe cloud concepts (3 modules)
2. Introduction to Cloud Infrastructure: Describe Azure architecture and services (5 modules)
3. Introduction to Cloud Infrastructure: Describe Azure management and governance (4 modules)

Each Learn module is matched to one or two modules in this project (the project splits identity and security into two). "Introduction", "Module assessment" and "Summary" units have no teaching content of their own; the module quizzes here play the part of the assessments. The hands-on sandbox exercises and videos in Learn are not reproduced.

How this was checked: every module's learning objectives and unit list were read on Microsoft Learn. The units that were missing from the first version (sustainability, AI/ML/IoT, accounts, cost optimisation, encryption and key management, Service Trust Portal, multicloud, networking filters and routing) were read in full before the notes were written. The other units were matched by title and learning objective only. Compare against Learn again whenever Microsoft updates the paths, and run `python scripts/validate_content.py`, which fails if an objective has no questions.

## Path 1: Describe cloud concepts

| Learn module | Learn units (teaching content) | Project module and objectives |
|---|---|---|
| Describe cloud computing | What is cloud computing; shared responsibility; define cloud models (public, private, hybrid, multicloud, Azure Arc, Azure VMware Solution); consumption-based model | **M01**: O1 cloud computing, O2 shared responsibility, O3 cloud models, O4 consumption-based and pricing models, O5 serverless, O6 multicloud, Azure Arc, Azure VMware Solution |
| Describe the benefits of using cloud services | High availability and scalability; reliability and predictability; security and governance; manageability; sustainability | **M02**: O1 to O4 as named, O5 sustainability |
| Describe cloud service types | IaaS; PaaS; SaaS (with use cases) | **M03**: O1 IaaS, O2 PaaS, O3 SaaS, O4 choosing a service type |

## Path 2: Describe Azure architecture and services

| Learn module | Learn units (teaching content) | Project module and objectives |
|---|---|---|
| Describe the core architectural components of Azure | What is Microsoft Azure; Azure accounts; physical infrastructure (regions, region pairs, sovereign regions, availability zones, datacenters); management infrastructure (resources, resource groups, subscriptions, management groups, hierarchy) | **M04**: O1 regions, O2 availability zones and datacenters, O3 resources and resource groups, O4 subscriptions, management groups and hierarchy, O5 what Azure is and accounts |
| Describe Azure compute services | Virtual machines (scale sets, availability sets); Azure Virtual Desktop; containers; Azure Functions; AI, machine learning and IoT/Edge; application hosting options | **M05**: O1 compute types, O2 VM options, O3 VM resources, O4 application hosting, O5 AI, machine learning and IoT/Edge |
| Describe Azure networking services | Virtual networking (subnets, endpoints, routing, filtering, peering); VPN Gateway; ExpressRoute; Azure DNS | **M06**: O1 virtual networks and subnets, O2 peering, O3 VPN Gateway and ExpressRoute, O4 Azure DNS, O5 public, private and service endpoints, O6 routing and filtering |
| Describe Azure storage services | Storage accounts; redundancy; storage services and tiers; data migration (Azure Migrate, Data Box); file movement (AzCopy, Storage Explorer, File Sync) | **M07**: O1 to O6 as named |
| Describe Azure identity, access, and security | Directory services; authentication methods; external identities; Conditional Access; RBAC; Zero Trust; defense in depth; encryption and key management; Microsoft Defender for Cloud | **M08**: O1 to O5 (directory services to RBAC). **M09**: O1 Zero Trust, O2 defense in depth, O3 Defender for Cloud, O4 encryption and key management |

## Path 3: Describe Azure management and governance

| Learn module | Learn units (teaching content) | Project module and objectives |
|---|---|---|
| Describe cost management in Azure | Factors affecting cost; pricing calculator; Microsoft Cost Management; tags; cost optimisation (reservations, savings plans, Spot) | **M10**: O1 to O4 as named, O5 cost optimisation options |
| Describe features and tools in Azure for governance and compliance | Microsoft Purview; Azure Policy; resource locks; Service Trust Portal | **M11**: O1 Purview, O2 Azure Policy, O3 resource locks, O4 Service Trust Portal |
| Describe features and tools for managing and deploying Azure resources | Tools for interacting with Azure (portal, Cloud Shell, CLI, PowerShell); Azure Arc; Azure Resource Manager and ARM templates | **M12**: O1 portal, O2 Cloud Shell, CLI and PowerShell, O3 Azure Arc, O4 infrastructure as code, O5 ARM and ARM templates |
| Describe monitoring tools in Azure | Azure Advisor; Azure Service Health; Azure Monitor (Log Analytics, alerts, Application Insights) | **M13**: O1 Advisor, O2 Service Health, O3 Azure Monitor, O4 Log Analytics, alerts and Application Insights |

## Not part of these three paths

Part 4 of the series ("Apply Azure skills in guided projects") is a separate learning path and is not included.
