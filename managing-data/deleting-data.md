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
User.collection.delete_every()
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

## Delete sub collection
Deleting any document not delete it's sub collection you need to delete them separately but you can pass `child=True`
to delete all its `subcollections`

Suppose you want to delete `post` and all it's `reviews`

```python
Post.collection.delete(post_key, child=True)
```

This will delete the `post` and all it's `subcollection` in this case `reviews` if `reviews` has any other `subcollection`
these will also delete.

## Delete by key list
FireO also allow you to delete multiple documents by providing **key list**

```python
Post.collection.delete_all(key_list)
```