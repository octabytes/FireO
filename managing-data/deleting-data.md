---
layout: default
title: Deleting Data
parent: Managing Data
nav_order: 2
---

# Deleting Data
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---
Delete single model or all collection. 

*NOTE: Deleting any document not delete it's sub collection you need to delete them separately*

## Delete document
To delete single document pass `key` to manager

### Example Usage
{: .no_toc }

```python
User.collection.delete(user_key)
```

## Delete collection
Delete all documents from collection

### Example Usage
{: .no_toc }

```python
User.collection.delete()
```
