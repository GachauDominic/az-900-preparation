# Storage services

## What you will learn

- Compare Azure Storage services (M07-O1).
- Describe storage account options and types (M07-O2).
- Describe access tiers (M07-O3).
- Describe redundancy options (M07-O4).
- Choose tools for moving files (M07-O5).
- Describe migration options (M07-O6).

## Key ideas

### Storage services

An **Azure storage account** is a container for your storage services, with a globally unique name. It can hold:

- **Blob storage:** unstructured objects such as images, video, documents and backups.
- **Azure Files:** managed file shares you reach with standard protocols such as SMB.
- **Queue storage:** messages that let application components communicate.
- **Table storage:** NoSQL key-attribute data.
- **Managed disks:** block storage for virtual machines.

### Account options and types

Standard general-purpose v2 accounts suit most needs. Premium accounts use solid-state storage for low latency and high performance. You also choose a redundancy option and a default access tier for blobs.

### Access tiers

Tiers trade storage cost against access cost and speed:

- **Hot:** frequently accessed data; highest storage cost, lowest access cost.
- **Cool:** infrequently accessed data kept for at least about 30 days.
- **Cold:** rarely accessed data kept for at least about 90 days.
- **Archive:** very rarely accessed data kept for at least about 180 days. It is offline, lowest in storage cost, and takes hours to rehydrate before you can read it.

Minimum periods can change, so check Microsoft Learn.

### Redundancy

- **LRS (locally redundant):** three copies in one datacenter. Lowest cost; does not survive losing the datacenter.
- **ZRS (zone-redundant):** copies across three availability zones in one region.
- **GRS (geo-redundant):** LRS in the primary region plus a copy in a secondary region far away.
- **GZRS (geo-zone-redundant):** ZRS in the primary region plus a copy in a secondary region.

Read-access variants (RA-GRS, RA-GZRS) let you read from the secondary.

### Moving files and migrating

- **AzCopy:** command-line tool to copy data to and from storage.
- **Azure Storage Explorer:** desktop app with a graphical interface for managing storage data.
- **Azure File Sync:** syncs on-premises Windows file servers with Azure Files and caches frequently used files locally.
- **Azure Migrate:** central hub to assess and migrate servers, databases and apps to Azure.
- **Azure Data Box:** a physical device shipped to you to move very large amounts of data offline.

## How it looks in real life

A photo site keeps recent pictures in the hot tier and moves old ones to cool, then archive. It chooses GZRS for customer invoices so they survive a datacenter or region problem. A company with 200 TB to move and a slow internet link orders Azure Data Box, while a small team copies a folder with AzCopy.

## Compare and contrast

| Choice | Key point | Easy to confuse with |
|---|---|---|
| Blob | Unstructured objects | Files (shares) |
| Azure Files | SMB file shares | Blob storage |
| LRS | One datacenter | ZRS (three zones) |
| GRS | Two regions | GZRS (zones plus a second region) |
| AzCopy | Command-line copy | Storage Explorer (graphical) |
| Data Box | Offline physical transfer | AzCopy (network transfer) |

## Exam tips

- Archive is the cheapest to store but must be rehydrated before reading.
- LRS does not protect against datacenter loss; ZRS protects against a zone failure; GRS and GZRS add a second region.
- "Too much data for the network" points to Data Box.
- "Sync on-premises file servers" points to Azure File Sync.

## Quick recap

- A storage account holds Blob, Files, Queue, Table and disk storage.
- Hot, cool, cold and archive tiers balance storage cost and access cost.
- LRS, ZRS, GRS and GZRS differ in where the copies live.
- AzCopy, Storage Explorer and File Sync move files; Azure Migrate and Data Box migrate.

## Go deeper

- [Storage redundancy](https://learn.microsoft.com/azure/storage/common/storage-redundancy)
- [Blob access tiers](https://learn.microsoft.com/azure/storage/blobs/access-tiers-overview)
- [Azure Data Box overview](https://learn.microsoft.com/azure/databox/data-box-overview)

Last reviewed: 2026-10-29
