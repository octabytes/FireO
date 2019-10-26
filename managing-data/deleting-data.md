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

## Delete child document
To delete child document just pass the child `key`

*Suppose **Review** is child of **Post** model*
```python
Review.collection.delete(review_key)
```

## Delete child collection
Delete all documents from child collection

```python
Review.collection.parent(post_key).delete()
```
