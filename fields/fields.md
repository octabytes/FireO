---
layout: default
title: Fields
nav_order: 6
has_children: true
permalink: fields
---

# FireO Fields

The following data types supported by FireO. It also describes the sort order used when comparing values of the same type
{: .fs-6 .fw-300 }

---

## Value type ordering

When a query involves a field with values of mixed types, Cloud Firestore uses a deterministic ordering based on the 
internal representations. The following list shows the order

- Null values
- Boolean values
- Integer and floating-point values, sorted in numerical order
- Date values
- Text string values
- Byte values
- Cloud Firestore references
- Geographical point values
- Array values
- Map values
