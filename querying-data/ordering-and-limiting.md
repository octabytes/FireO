---
layout: default
title: Ordering and Limiting
parent: Querying Data
nav_order: 4
---

# Ordering and Limiting
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

FireO provides powerful query functionality for specifying which documents you want to retrieve from a 
collection. These queries can also be used with either `get()` or `fetch()`

## Order and limit data
By default, a query retrieves all documents that satisfy the query in ascending order by document ID. 
You can specify the sort order for your data using `order()`, and you can limit the number of documents 
retrieved using `limit()` or passing number of documents in `fetch(limit)`.

For example, you could query for the first 3 cities alphabetically with:
```python
City.collection.order('name').limit(3).fetch()

# Same thing can be achieved by passing limit in fetch() method
City.collection.order('name').fetch(3)
```

You could also sort in descending order to get the last 3 cities:
```python
City.collection.order('-name').fetch(3)
```
You can also order by multiple fields. For example, if you wanted to order by state, 
and within each state order by population in descending order:
```python
City.collection.order('state').order('-population')
```

You can combine `filter()` with `order()` and `limit()`. In the following example, 
the queries define a population threshold, sort by population in ascending order, 
and return only the first few results that exceed the threshold:

```python
City.collection.filter('population', '>', 2500000).order('population').limit(2).fetch()
```
However, if you have a filter with a range comparison (`<`, `<=`, `>`, `>=`), your first ordering 
must be on the same field:

**Valid:** Range filter and orderBy on the same field
```python
City.collection.filter('population', '>', 2500000).order('population').fetch()
```

**Invalid:** Range filter and first orderBy on different fields
```python
City.collection.filter('population', '>', 2500000).order('country')
```

## Sub collection
Sub collection queries work in same fashion but you need to pass `parent_key` to search in specific 
collection. Ordering and limiting apply same like other root collection

### Sample Data
{: .no_toc }

```python
class Post(Model):
    title = TextField()
    content = TextField()


class Review(Model):
    name = TextField()
    stars = NumberField()


p = Post(title="First Post", content="Some Content")
p.save()

r1 = Review(parent=p.key)
r1.name = 'Azeem'
r1.stars = 5
r1.save()

r2 = Review(parent=p.key)
r2.name = 'Arfan'
r2.stars = 3
r2.save()
```

### Example Usage
{: .no_doc }

The following query returns all reviews order by **review stars**

```python
reviews = Review.collection.parent(post_key).order('stars').fetch()
```