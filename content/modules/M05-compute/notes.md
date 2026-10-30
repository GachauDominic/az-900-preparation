# Compute services

## What you will learn

- Compare virtual machines, containers and functions (M05-O1).
- Describe virtual machine options: scale sets, availability sets and Azure Virtual Desktop (M05-O2).
- List the resources a virtual machine needs (M05-O3).
- Choose an application hosting option (M05-O4).
- Describe Azure AI, machine learning and IoT/Edge service categories (M05-O5).

## Key ideas

### Compute types

- **Virtual machines (VMs)** are IaaS. You choose the operating system and manage it. They give the most control and the most responsibility.
- **Containers** package an application with what it needs to run. They share the host operating system, so they are lighter and start faster than VMs, and they run the same everywhere. Azure Container Instances runs containers without servers to manage; Azure Kubernetes Service manages many containers at scale.
- **Functions** (Azure Functions) are serverless. Small pieces of code run in response to events, scale automatically and are billed per execution.

### Virtual machine options

- **Virtual Machine Scale Sets** create and manage a group of identical, load-balanced VMs that can scale out and in automatically.
- **Availability sets** spread VMs across fault domains (separate power and network) and update domains (rebooted at different times) inside one datacenter. They protect against hardware failure and planned maintenance, not against losing the whole datacenter. Availability zones cover that.
- **Azure Virtual Desktop** delivers Windows desktops and apps hosted in Azure to users on almost any device.

### Resources a VM needs

A VM is more than compute. Expect to create or choose: a **size** (CPU and memory), an **image** (the operating system), an **OS disk** and optional data disks, a **virtual network and subnet**, a **network interface**, and an IP address. They all live in a resource group.

### Application hosting options

- **Azure App Service** (PaaS) hosts web apps and APIs without managing servers or the operating system.
- **Containers** suit portable, packaged apps.
- **Virtual machines** suit apps that need full control or a specific configuration.

### AI, machine learning and IoT/Edge services

Azure groups these into a few categories:

- **Azure AI services** give you prebuilt capabilities, such as language, speech, vision and document processing, through APIs, so you do not have to train your own model first. **Azure OpenAI Service** supports generative AI scenarios such as chat and content generation.
- **Azure Machine Learning** is for building, training and managing your own custom machine learning models.
- **Azure IoT services** help with connected devices: **IoT Hub** provides secure two-way communication between the cloud and devices, **IoT Central** is a simplified software-as-a-service IoT platform, and **IoT Edge** runs some workloads on devices closer to where data is produced.

"Agentic" applications combine an AI model, instructions, context and tools to complete multi-step goals. In Azure you build them from AI services and your own application code; they are a pattern, not a separate compute service.

## How it looks in real life

A shop runs its website on App Service so developers never patch servers. An image-resizing function runs only when a photo is uploaded. A vendor's legacy program needs a specific Windows setup, so it runs on a VM inside an availability set. A call centre gives staff Azure Virtual Desktop so they can work from home on their own laptops.

## Compare and contrast

| Option | Control | Best for |
|---|---|---|
| Virtual machine | Highest | Full control, legacy apps |
| Container | Medium | Portable, fast-starting apps |
| Function | Lowest | Short, event-driven code |
| Scale set | Group of identical VMs | Autoscaling a workload |
| Availability set | VMs spread inside one datacenter | Surviving hardware faults and maintenance |

## Exam tips

- "Event-driven, pay per execution" means Azure Functions.
- "Identical VMs that autoscale" means a scale set.
- Availability sets do not protect against a datacenter or region failure.
- "Windows desktop in the cloud" means Azure Virtual Desktop.
- Prebuilt AI through APIs points to Azure AI services; custom models point to Azure Machine Learning; connected devices point to IoT services.

## Quick recap

- VMs give control, containers give portability, functions give event-driven simplicity.
- Scale sets autoscale identical VMs; availability sets spread VMs across fault and update domains.
- A VM needs a size, image, disk, network, network interface and IP address.
- App Service is the PaaS choice for web apps.
- Azure AI services are prebuilt, Azure Machine Learning is custom, and IoT Hub, IoT Central and IoT Edge cover connected devices.

## Go deeper

- [Azure Virtual Machines overview](https://learn.microsoft.com/azure/virtual-machines/overview)
- [App Service overview](https://learn.microsoft.com/azure/app-service/overview)
- [Azure Virtual Desktop overview](https://learn.microsoft.com/azure/virtual-desktop/overview)
- [What are Azure AI services?](https://learn.microsoft.com/azure/ai-services/what-are-ai-services)
- [Azure Machine Learning overview](https://learn.microsoft.com/azure/machine-learning/overview-what-is-azure-machine-learning)
- [IoT Hub concepts](https://learn.microsoft.com/azure/iot-hub/iot-concepts-and-iot-hub)

Last reviewed: 2026-10-29
