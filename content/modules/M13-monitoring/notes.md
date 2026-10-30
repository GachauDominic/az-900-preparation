# Monitoring tools

## What you will learn

- Describe the purpose of Azure Advisor (M13-O1).
- Describe Azure Service Health (M13-O2).
- Describe Azure Monitor (M13-O3).
- Describe Log Analytics, Azure Monitor alerts and Application Insights (M13-O4).

## Key ideas

### Azure Advisor

**Azure Advisor** is a personalised consultant. It analyses your resources and how you use them, then recommends ways to improve in five areas: **reliability, security, performance, cost and operational excellence**. For example, it may suggest resizing or shutting down an underused virtual machine.

### Azure Service Health

**Azure Service Health** tells you how Azure's health affects **you**. It has three parts:

- **Azure status:** a public view of the health of Azure services and regions worldwide.
- **Service Health:** a personalised view of issues, planned maintenance and advisories for the services and regions you use.
- **Resource Health:** the health of an individual resource, such as one virtual machine.

You can create alerts so you hear about problems straight away.

### Azure Monitor

**Azure Monitor** collects, analyses and acts on **telemetry** from Azure, on-premises and other environments. The two main data types are **metrics** (numbers over time, like CPU use) and **logs** (records of events). You can chart the data, query it and set alerts.

### Log Analytics, alerts and Application Insights

- **Log Analytics** is the tool in the Azure portal where you write queries to explore log data collected by Azure Monitor.
- **Azure Monitor alerts** notify people or trigger actions, such as sending an email or running an automation, when a condition is met, for example CPU above 90% for ten minutes.
- **Application Insights** monitors live web applications. It tracks requests, response times, failures and dependencies, and helps you spot and diagnose problems.

## How it looks in real life

A team checks Advisor monthly and acts on its cost and security recommendations. A regional outage is announced, and Service Health shows whether the team's resources are affected. An Azure Monitor alert emails the on-call engineer when the web servers run hot, and Application Insights shows which page is slow.

## Compare and contrast

| Tool | Answers the question | Easy to confuse with |
|---|---|---|
| Azure Advisor | How can I improve my setup? | Service Health (is Azure healthy?) |
| Service Health | Is Azure affecting my resources? | Azure Monitor (telemetry from my resources) |
| Azure Monitor | What is happening in my environment? | Advisor |
| Log Analytics | Let me query the logs | Alerts (notify me) |
| Application Insights | How is my live web app performing? | Azure Monitor as a whole |

## Exam tips

- Advisor gives recommendations in five categories, including cost and security.
- Service Health is about Azure's own health; Monitor is about your telemetry.
- Metrics are numbers over time; logs are event records.
- Application Insights is for application performance.

## Quick recap

- Advisor recommends improvements; Service Health reports Azure issues that affect you.
- Azure Monitor gathers metrics and logs; Log Analytics queries them; alerts notify; Application Insights watches apps.

## Go deeper

- [Azure Advisor overview](https://learn.microsoft.com/azure/advisor/advisor-overview)
- [Azure Service Health overview](https://learn.microsoft.com/azure/service-health/overview)
- [Azure Monitor overview](https://learn.microsoft.com/azure/azure-monitor/overview)

Last reviewed: 2026-10-29
