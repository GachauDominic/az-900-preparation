# Identity and access

## What you will learn

- Describe Microsoft Entra ID and Microsoft Entra Domain Services (M08-O1).
- Describe single sign-on, multifactor authentication and passwordless sign-in (M08-O2).
- Describe external identities (M08-O3).
- Describe Microsoft Entra Conditional Access (M08-O4).
- Describe Azure role-based access control (M08-O5).

## Key ideas

### Authentication and authorization

**Authentication** proves who you are. **Authorization** decides what you are allowed to do once you are signed in. Entra ID handles the first; Azure RBAC is a key part of the second for Azure resources.

### Directory services

**Microsoft Entra ID** (formerly Azure Active Directory) is Microsoft's cloud-based identity and access management service. It stores users, groups and app registrations and signs people in to Azure, Microsoft 365 and thousands of other apps.

**Microsoft Entra Domain Services** gives you managed domain services, such as domain join, group policy, LDAP and Kerberos or NTLM authentication, without you deploying and managing domain controllers. It suits older applications that expect a traditional domain.

### Authentication methods

- **Single sign-on (SSO):** sign in once with one set of credentials and reach many applications.
- **Multifactor authentication (MFA):** require two or more kinds of proof from different categories: something you **know** (password, PIN), something you **have** (phone, security key) and something you **are** (fingerprint, face). A password plus a security question is not MFA, because both are things you know.
- **Passwordless:** replace the password with something you have or are, such as Windows Hello for Business, the Microsoft Authenticator app or a FIDO2 security key.

### External identities

**External identities** let people outside your organisation, such as partners, suppliers or customers, access your apps and resources using their own identities. In business-to-business collaboration, guests sign in with their own work, school or personal accounts, and you control what they can reach.

### Conditional Access

**Conditional Access** is a set of if-then policies. It looks at signals such as who the user is, where they are, what device they use, which app they open and the sign-in risk, then decides to allow, block or require more proof, for example MFA. It usually needs an appropriate Microsoft Entra ID licence.

### Azure role-based access control (RBAC)

**Azure RBAC** manages who can do what with Azure resources. A **role assignment** joins three things: a **security principal** (who), a **role definition** (what permissions) and a **scope** (where). Scopes run from management group to subscription, resource group and resource, and permissions are inherited downward. Common roles are **Owner** (everything, including granting access), **Contributor** (manage resources but not grant access), **Reader** (view only) and **User Access Administrator** (manage access). Give people the least access they need.

## How it looks in real life

A company signs staff in once to reach all its apps (SSO). Admins must approve a prompt on the Authenticator app (MFA). A Conditional Access policy asks for MFA only when someone signs in from an unfamiliar country. A contractor is invited as a guest and given the Reader role on one resource group, so they can look but not change anything.

## Compare and contrast

| Idea | Key point | Easy to confuse with |
|---|---|---|
| Authentication | Who you are | Authorization (what you can do) |
| Entra ID | Cloud identity service | Entra Domain Services (managed domain services) |
| MFA | Different categories of proof | Two passwords |
| Conditional Access | Policy based on signals | RBAC (permissions on resources) |
| Contributor | Manage, cannot grant access | Owner (can grant access) |

## Exam tips

- Authentication is identity; authorization is permissions.
- Two things you know is not MFA.
- Contributor cannot assign roles; Owner can.
- Role assignments are inherited by lower scopes.

## Quick recap

- Entra ID is the cloud identity service; Entra Domain Services adds managed domain features.
- SSO, MFA and passwordless are authentication methods.
- External identities give outsiders controlled access with their own accounts.
- Conditional Access applies if-then policies; RBAC controls Azure resource permissions.

## Go deeper

- [What is Microsoft Entra ID?](https://learn.microsoft.com/entra/fundamentals/whatis)
- [Conditional Access overview](https://learn.microsoft.com/entra/identity/conditional-access/overview)
- [Azure RBAC overview](https://learn.microsoft.com/azure/role-based-access-control/overview)

Last reviewed: 2026-10-29
