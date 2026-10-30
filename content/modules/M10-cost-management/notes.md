# Cost management

## What you will learn

- Describe the factors that affect costs in Azure (M10-O1).
- Use the pricing calculator to estimate costs (M10-O2).
- Describe cost management capabilities (M10-O3).
- Describe the purpose of tags (M10-O4).
- Describe cost optimisation options: reservations, savings plans and Spot pricing (M10-O5).

## Key ideas

### What affects cost

- **Resource type and size:** a larger virtual machine or a premium storage account costs more.
- **Consumption:** you pay for how much and how long you use a resource.
- **Region:** prices differ between regions.
- **Network traffic:** data coming into Azure is generally free, while data leaving Azure to the internet or another region is generally charged.
- **Pricing model:** pay-as-you-go versus commitments such as reservations or savings plans, and offers such as **Azure Hybrid Benefit**, which lets you use existing eligible licences.
- **Subscription type and Marketplace purchases:** some services have their own charges.

Always check Microsoft Learn for current rules and amounts.

### The pricing calculator

The **Azure pricing calculator** is a web tool that estimates what planned resources will cost before you deploy them. Add products, choose size, region and options, and adjust until the estimate suits your budget. It gives an estimate, not a bill.

### Microsoft Cost Management

**Microsoft Cost Management** helps you understand and control what you actually spend:

- **Cost analysis:** see where costs come from, by resource, resource group, tag or time.
- **Budgets and alerts:** set a spending limit and get notified when it is reached or forecast. A budget alerts you; it does not stop resources by itself.
- **Recommendations and exports:** find savings and send cost data elsewhere for reporting.

### Tags

A **tag** is a name and value pair, such as Department = Finance or Environment = Production, attached to a resource, resource group or subscription. Tags help you organise resources and **group costs** by team, project or environment. Resources do not automatically inherit tags from their resource group unless you set that up, for example with Azure Policy.

### Cost optimisation options

After you estimate and monitor costs, choose the pricing option that matches each workload:

- **Reservations:** commit to a specific amount of capacity for one or three years and get a discount. Best for steady, predictable, long-running workloads.
- **Azure savings plan for compute:** commit to an hourly spend for one or three years instead of to a specific VM type. It suits steady usage that moves between compute services.
- **Spot pricing:** Spot virtual machines use Azure's unused capacity at reduced prices, but Azure can take the capacity back. Best for fault-tolerant, interruptible work such as batch jobs.

Review the choice regularly, because a workload's needs change over time.

## How it looks in real life

Before moving a website, a team builds an estimate in the pricing calculator and compares two regions. After launch, they set a monthly budget with an alert at 80%. They tag every resource with a Department tag, so finance can see each team's share in cost analysis.

## Compare and contrast

| Tool | Answers the question | Easy to confuse with |
|---|---|---|
| Pricing calculator | What will it cost? (before) | Cost analysis (what did it cost?) |
| Cost analysis | Where is the money going? | Budgets (alerts at limits) |
| Budget | Tell me when spending reaches a limit | A hard spending cap |
| Tags | Which team or project owns this? | Resource groups (containers) |

## Exam tips

- Calculator is before deployment; Cost Management is after.
- Outbound data is charged; inbound is generally free.
- A budget notifies; it does not shut anything down.
- Tags are not inherited by default.
- Predictable and long-running: reservations. Steady but flexible: savings plan. Interruptible: Spot.

## Quick recap

- Size, usage, region, traffic and pricing model drive cost.
- The pricing calculator estimates; Cost Management analyses actual spend and sets budgets.
- Tags label resources so costs can be grouped.
- Reservations and savings plans trade commitment for discounts; Spot is cheapest but can be interrupted.

## Go deeper

- [Plan and manage costs](https://learn.microsoft.com/azure/cost-management-billing/understand/plan-manage-costs)
- [Cost Management overview](https://learn.microsoft.com/azure/cost-management-billing/costs/overview-cost-management)
- [Tag resources](https://learn.microsoft.com/azure/azure-resource-manager/management/tag-resources)
- [Reservations](https://learn.microsoft.com/azure/cost-management-billing/reservations/save-compute-costs-reservations)
- [Azure savings plan for compute](https://learn.microsoft.com/azure/cost-management-billing/savings-plan/savings-plan-compute-overview)
- [Spot virtual machines](https://learn.microsoft.com/azure/virtual-machines/spot-vms)

Last reviewed: 2026-10-29
