---
layout: default
title: Querying and Filtering
parent: Querying Data
nav_order: 3
---

# Querying and Filtering
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

FireO provides powerful query functionality for specifying which documents you want to retrieve from a 
collection. These queries can also be used with either `get()` or `fetch()`

## Example data
To get started, write some data about cities so we can look at different ways to read it back:

```python
class City(Model):
    short_name = IDField()
    name = TextField()
    state = TextField()
    country = TextField()
    capital = BooleanField()
    population = NumberField()
    regions = ListField()

City.collection.create(
short_name='SF', name='San Francisco', state='CA', country='USA', 
capital=False, population=860000, regions=['west_coast', 'norcal']
)

City.collection.create(
short_name='LA', name='Los Angeles', state='CA', country='USA', 
capital=False, population=3900000, regions=['west_coast', 'socal']
)

City.collection.create(
short_name='DC', name='Washington D.C.', state='CA', country='USA', 
capital=True, population=680000, regions=['east_coast']
)

City.collection.create(
short_name='TOK', name='Tokyo', country='Japan', 
capital=True, population=9000000, regions=['kanto', 'honshu']
)

City.collection.create(
short_name='BJ', name='Beijing', country='China', 
capital=True, population=21500000, regions=['hebei']
)
```

## Simple Queries
The following query returns all cities with state **CA**

```python
cities = City.collection.filter('state', '==', 'CA').fetch()
```

The following query returns all the capital cities

```python
cities = City.collection.filter('capital', '==', True).fetch()
```

## Get First result
After creating a query object, use the `get()` function to retrieve the first matching result.
`fetch()` return `generator` for retrieve all mating result.

The following query returns first matching city with state **CA**

```python
city = City.collection.filter('state', '==', 'CA').get()
```

## Query operators
The `filter()` method takes three parameters: a field to filter on, a comparison operation, and a value. 
The comparison can be `<`, `<=`, `==`, `>`, `>=`, or `array-contains`.

Some example filters:
```python
City.collection.filter('state', '==', 'CA')
City.collection.filter('population', '<', 1000000)
City.collection.filter('name', '>=', 'San Francisco')
```

## List membership
You can use the `array-contains` operator to filter based on list values. For example:
```python
query = City.collection.filter('regions', 'array_contains', 'west_coast')
```

This query returns every **city** document where the **regions** field is an array that contains **west_coast**. 
If the array has multiple instances of the value you query on, the document is included in the results only once.

## Compound queries
You can also chain multiple `filter()` methods to create more specific queries (logical `AND`). 
However, to combine the equality operator (`==`) with a range or array-contains 
clause (`<`, `<=`, `>`, `>=`, or `array-contains`), make sure to create a [composite index](https://cloud.google.com/firestore/docs/query-data/indexing).

```python
sydney_query = City.collection.filter('state', '==', 'CO').filter('name', '==', 'Denver')

large_us_cities_query = City.collection.filter('state', '==', 'CA').filter('population', '>', 1000000)
```

You can only perform range comparisons (`<`, `<=`, `>`, `>=`) on a single field, and you can include at 
most one `array-contains` clause in a compound query:

**Valid:** Range filters on only one field
```python
City.collection.filter('state', '>=', 'CA').filter('state', '<=', 'IN')
```

**Invalid:** Range filters on different fields
```python
City.collection.filter('state', '>=', 'CA').filter('population', '>=', 1000000)
```

## Custom Query Method
Instead of creating query again and again you can create `@classmethod`

### Example Usage
{: .no_toc }

```python
class City(Model):
    # .. code ..

    @classmethod
    def get_capital_cities(cls):
        return cls.collection.filter('capital', '==', True).fetch()

# The following query returns all the capital cities
capital_cities = City.get_capital_cities()
```

### More useful Example
{: .no_toc }

```python
class Post(Model):
    title = TextField()
    content = TextField()

    @classmethod
    def get_detail(cls, key):
        post = cls.collection.get(key)
        recent_review = Review.collection.parent(key).order('-created_on').fetch(3)

        return post, recent_review

class Review(Model):
    name = TextField()
    stars = NumberField()
    created_on = DateTime(auto=True)

p = Post(title="First Post", content="Post Content")
p.save()

r1 = Review(parent=p.key)
r1.name = "Azeem"
r1.stars = 5
r1.save()

r2 = Review(parent=p.key)
r2.name = "Azeem"
r2.stars = 4
r2.save()

r2 = Review(parent=p.key)
r2.name = "Arfan"
r2.stars = 3
r2.save()
```

Get **Post** and most recent **Reviews**

```python
post, reviews = Post.get_detail(post_key)

print(post.title)

for r in reviews:
    print(r.name, r.stars)
```

## Sub collection
Sub collection queries work in same fashion but you need to pass `parent_key` to search in specific 
collection.

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

The following query returns all reviews which is posted by **Azeem**

```python
reviews = Review.collection.parent(post_key).filter('name', '==', 'Azeem').fetch()
```

## Query limitations
Cloud Firestore does not support the following types of queries:

- Queries with range filters on different fields, as described in the previous section.
- Logical `OR` queries. In this case, you should create a separate query for each `OR` condition 
and merge the query results in your app.
- Queries with a `!=` clause. In this case, you should split the query into a greater-than query 
and a less-than query. For example, although the query clause `filter("age", "!=", "30")` is not supported, 
you can get the same result set by combining two queries, one with the clause `filter("age", "<", "30")` and 
one with the clause `filter("age", ">", 30)`.