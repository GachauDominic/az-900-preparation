# Management and deployment tools

## What you will learn

- Describe the Azure portal (M12-O1).
- Describe Azure Cloud Shell, Azure CLI and Azure PowerShell (M12-O2).
- Describe the purpose of Azure Arc (M12-O3).
- Describe infrastructure as code (M12-O4).
- Describe Azure Resource Manager and ARM templates (M12-O5).

## Key ideas

### The Azure portal

The **Azure portal** is a web-based graphical interface for creating, managing and monitoring resources. It is good for exploring, learning and one-off tasks, and you can build dashboards of the things you care about.

### Cloud Shell, Azure CLI and Azure PowerShell

- **Azure Cloud Shell** is a shell you open in the browser. It comes with Azure CLI and Azure PowerShell already installed and signed in to your account. It needs a storage account to keep your files between sessions.
- **Azure CLI** is a cross-platform command-line tool for Windows, macOS and Linux. Commands start with `az`.
- **Azure PowerShell** is a set of PowerShell commands (cmdlets) for managing Azure, such as `New-AzResourceGroup`.

Both can be scripted to automate repeated tasks, and you can run them in Cloud Shell or on your own computer. Which you pick is mostly personal preference.

### Azure Arc

**Azure Arc** extends Azure management to resources that live outside Azure: on-premises servers, servers in other clouds and Kubernetes clusters. They appear in Azure, so you can apply the same tools to them, such as tags, Azure Policy, role-based access control and monitoring.

### Infrastructure as code

**Infrastructure as code (IaC)** means defining and provisioning infrastructure with files rather than clicking through screens. The files can be kept in version control, reviewed and reused, so environments are **repeatable and consistent** and mistakes from manual steps drop. **Declarative** IaC describes the end state you want (ARM templates, Bicep). **Imperative** scripts list the steps to run (a CLI or PowerShell script).

### Azure Resource Manager and ARM templates

**Azure Resource Manager (ARM)** is the deployment and management service for Azure. Every request to create, update or delete resources goes through it, whether it starts in the portal, Azure CLI, Azure PowerShell, a REST call or an SDK, so you get consistent results. ARM also applies access control, locks and tags.

**ARM templates** are JSON files that describe resources declaratively. You can reuse them, pass in parameters and deploy the same environment again and again. **Bicep** is a shorter language that compiles to an ARM template.

## How it looks in real life

A new engineer explores in the portal, then runs a short Azure CLI script in Cloud Shell to create a test resource group. The team keeps a Bicep file in version control that builds the whole web app environment, so test and production match exactly. Servers in the company's own datacenter are connected through Azure Arc, so they show up in Azure and follow the same policies.

```bash
az group create --name rg-demo --location westeurope
```

## Compare and contrast

| Tool | What it is | Easy to confuse with |
|---|---|---|
| Portal | Web graphical interface | Cloud Shell (browser command line) |
| Azure CLI | Cross-platform `az` commands | Azure PowerShell cmdlets |
| Azure Arc | Azure management for resources outside Azure | Moving the resources into Azure |
| ARM template | Declarative JSON definition | A CLI script (imperative steps) |
| ARM | Service that processes every request | An ARM template (a file it deploys) |

## Exam tips

- Everything you do in Azure goes through Azure Resource Manager.
- ARM templates are declarative; scripts are imperative.
- Azure Arc manages resources where they are; it does not move them.
- Cloud Shell offers both Bash with Azure CLI and PowerShell.

## Quick recap

- The portal is graphical; Cloud Shell, CLI and PowerShell are command-line options.
- Azure Arc brings outside resources under Azure management.
- IaC makes environments repeatable; ARM templates and Bicep are declarative.
- ARM is the service behind every deployment and management request.

## Go deeper

- [Azure Resource Manager overview](https://learn.microsoft.com/azure/azure-resource-manager/management/overview)
- [Azure Cloud Shell overview](https://learn.microsoft.com/azure/cloud-shell/overview)
- [Azure Arc overview](https://learn.microsoft.com/azure/azure-arc/overview)

Last reviewed: 2026-10-29
