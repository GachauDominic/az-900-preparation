# Benefits of cloud services

## What you will learn

- Describe high availability and scalability (M02-O1).
- Describe reliability and predictability (M02-O2).
- Describe security and governance benefits (M02-O3).
- Describe manageability in the cloud (M02-O4).
- Describe sustainability considerations in the cloud (M02-O5).

## Key ideas

### High availability and scalability

**High availability** means a service is designed to stay running with very little downtime. Providers describe this in a **service level agreement (SLA)**, a promised uptime percentage. A higher percentage allows less downtime: 99.99% allows far less than 99.9%.

**Scalability** is the ability to change the amount of resources to match demand.

- **Scale up or down (vertical):** make one machine bigger or smaller.
- **Scale out or in (horizontal):** add or remove machines or instances.
- **Elasticity** means scaling happens automatically as demand rises and falls, so you do not pay for idle capacity.

### Reliability and predictability

**Reliability** is the ability of a system to recover from failures and keep working. The cloud supports it with redundancy, such as spreading resources across availability zones and regions.

**Predictability** means you can count on consistent outcomes, in two ways:

- **Performance:** autoscaling and load balancing keep response times steady as demand changes.
- **Cost:** tools for monitoring, forecasting and setting budgets help you estimate what you will spend.

### Security and governance

Cloud providers invest heavily in physical security, threat detection and compliance certifications, and they offer tools to protect identities, data and networks. **Governance** means setting standards and enforcing them: rules about what can be created, where, and how it must be configured. The cloud can apply and audit those rules across an entire environment. Security is still shared, because you must configure and use the tools correctly.

### Manageability

There are two sides:

- **Management of the cloud:** automatic scaling, deployment from templates, and monitoring with alerts.
- **Management in the cloud:** using the portal, command-line tools, scripts or APIs to create and manage resources.

### Sustainability

Cloud providers run at large scale, which can use resources more efficiently than many separate on-premises setups. You still play a part by matching what you run to what you need. Good habits are to **scale down** when demand falls, **turn off or deallocate** resources that are not in use, **choose efficient sizes** instead of overprovisioning, and **monitor** usage so you can keep optimising. A development environment that only runs in business hours, shut down automatically overnight and at weekends, is a simple example. The cycle is: right-size, automate, monitor, optimise.

## How it looks in real life

An online retailer expects a sale. Autoscaling adds web servers as visitors arrive and removes them afterwards, so pages stay fast and the bill matches the traffic. The shop runs across two availability zones, so one datacenter problem does not take it offline. A monthly cost report and a budget alert tell the team what to expect.

## Compare and contrast

| Benefit | What it gives you | Easy to confuse with |
|---|---|---|
| High availability | Minimal downtime, backed by an SLA | Reliability (recovering from failure) |
| Scalability | Ability to resize | Elasticity (automatic resizing) |
| Scale up | Bigger machine | Scale out (more machines) |
| Predictability | Steady performance and forecastable cost | Reliability |
| Governance | Rules enforced and audited | Security (protection) |

## Exam tips

- "Automatically adds and removes capacity" points to elasticity.
- "Add more instances" is scaling out; "make the machine bigger" is scaling up.
- A higher SLA percentage means less allowed downtime.
- Predictability covers both performance and cost.
- Sustainability in the cloud comes from right-sizing, switching off what is idle, and monitoring usage.

## Quick recap

- High availability keeps services running; SLAs state the promised uptime.
- Scalability resizes resources; elasticity does it automatically.
- Reliability is recovering from failure; predictability is steady performance and cost.
- The cloud offers security tools and governance, but security is still shared.
- Manageability covers automation of the cloud and tools to manage resources in it.
- Matching resources to demand, and shutting down what is idle, supports both sustainability and lower cost.

## Go deeper

- [Azure Well-Architected Framework](https://learn.microsoft.com/azure/well-architected/)
- [Cloud Adoption Framework for Azure](https://learn.microsoft.com/azure/cloud-adoption-framework/)
- [Azure sustainability and the Well-Architected Framework](https://learn.microsoft.com/azure/well-architected/)

Last reviewed: 2026-10-29
