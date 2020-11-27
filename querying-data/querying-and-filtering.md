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

For equality(`==`) operator you can direct assign value and this will work.  
For example:
```python
City.collection.filter(state='CA') # Equal to 'state', '==', 'CA'
``` 

Multiple equality operator can also apply in same single `filter`

```python
City.collection.filter(state='CA', capital=True)
```

Direct assignment is only work with equality(`==`) operator for others user regular `filter`  
For example:

Get cities with state  `CA` and `population` is greater than `1000000`

```python
City.collection.filter(state='CA').filter('population', '>', 1000000)
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
The comparison can be `<`, `<=`, `==`, `>`, `>=`, `array-contains`, `in` and `array-contains-any`.

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

## in and array-contains-any
Use the `in` operator to combine up to 10 equality (`==`) clauses on the same field with a logical `OR`. 
An `in` query returns documents where the given field matches any of the comparison values. For example:

```python
query = City.filter('country', 'in', ['USA', 'Japan'])
```

This query returns every `city` document where the `country` field is set to `USA` or `Japan`. 
From the example data, this includes the `SF`, `LA`, `DC`, and `TOK` documents.

Similarly, use the `array-contains-any` operator to combine up to 10 `array-contains` clauses on the same field 
with a logical `OR`. An `array-contains-any` query returns documents where the given field is an array that contains 
one or more of the comparison values:

```python
query = City.filter(
    'regions', 'array_contains_any', ['west_coast', 'east_coast']
)
```

This query returns every city document where the `region` field is an array that contains `west_coast` or `east_coast`. 
From the example data, this includes the `SF`, `LA`, and `DC` documents.

Results from `array-contains-any` are de-duped. Even if a document's array field matches more than one of the 
comparison values, the result set includes that document only once.

`array-contains-any` always filters by the array data type. For example, the query above would not return a 
city document where instead of an array, the `region` field is the string `west_coast`.

You can use an array value as a comparison value for `in`, but unlike `array_contains_any`, 
the clause matches for an exact match of array length, order, and values. For example:

```python
query = City.filter(
    'regions', 'in', [['west_coast'], ['east_coast']]
)
```

This query returns every city document where the `region` field is an array that contains 
exactly one element of either `west_coast` or `east_coast`. From the example data, only the `DC` 
document qualifies with its `region` field of `["east_coast"]`. The `SF` document, however, does 
not match because its `region` field is `["west_coast", "norcal"]`.

### Limitations
{: .no_toc }
Note the following limitations for `in` and `array-contains-any`:

- `in` and `array-contains-any` support up to 10 comparison values.
- You can use only one `in` or `array-contains-any` clause per query. You can't use both `in` and `array-contains-any` 
in the same query.
- You can combine `array-contains` with `in` but not with `array-contains-any`.

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

## Filter with nested Model
You can `filter` models with `nested_models` fields using `dot(.)` notation.

### Example Usage
{: .no_toc }

```python
class Level1(Model):
    name = TextField()


class Level2(Model):
    name = TextField()
    lev1 = NestedModel(Level1)


class Level3(Model):
    name = TextField()
    lev2 = NestedModel(Level2)

# Adding data
l = Level3()
l.name = 'level 1'
l.lev2.name = 'level 2'
l.lev2.lev1.name = 'level 3'
l.save()

# Filtering data 
l = Level3.collection.filter('lev2.lev.name', '==', 'level 3').get()
```

## Filter with Reference Model
You can `filter` models with reference model `key`.

### Example Usage
{: .no_toc }

```python
class Company(Model):
    name = TextField()


class Employee(Model):
    name = TextField()
    company = ReferenceField(Company, auto_load=False)

# Adding data
c = Company(name="Abc_company")
c.save()

e = Employee()
e.name = 'Employee Name'
e.company = c
e.save()

# Filtering data 
el = Employee.collection.filter(company=c.key).fetch()
```

## Collection group queries
A collection group consists of all collections with the same ID. By default, queries retrieve 
results from a single collection in your database. Use a collection group query to retrieve 
documents from a collection group instead of from a single collection.

For example, you can create a `landmarks` collection group by adding a landmarks subcollection to each city:
```python
class City(Model):
    state = TextField()


class Landmarks(Model):
    type = TextField()
    name = TextField()


c = City.collection.create(state='SF')
Landmarks.collection.parent(c.key).create(type='bridge', name='Golden Gate Bridge')
Landmarks.collection.parent(c.key).create(type='museum', name='Legion of Honor')

c = City.collection.create(state='LA')
Landmarks.collection.parent(c.key).create(type='park', name='Griffith Park')
Landmarks.collection.parent(c.key).create(type='museum', name='The Getty')

c = City.collection.create(state='DC')
Landmarks.collection.parent(c.key).create(type='memorial', name='Lincoln Memorial')
Landmarks.collection.parent(c.key).create(type='museum', name='National Air and Space Museum')
```

We can use the simple and compound query described earlier to query a single city's `landmarks` 
subcollection, but you might also want to retrieve results from every city's `landmarks` subcollection at once.

The `landmarks` collection group consists of all collections with the ID `landmarks`, and you 
can query it using a collection group query. For example, this collection group query retrieves all `museum` 
landmarks across all cities:

```python
museums = Landmarks.collection.filter('type', '==', 'museum').group_fetch()
for museum in museums:
    print(museum.name)
```

## Query limitations
Cloud Firestore does not support the following types of queries:

- Queries with range filters on different fields, as described in the previous section.
- Queries with a `!=` clause. In this case, you should split the query into a greater-than query 
and a less-than query. For example, although the query clause `filter("age", "!=", "30")` is not supported, 
you can get the same result set by combining two queries, one with the clause `filter("age", "<", "30")` and 
one with the clause `filter("age", ">", 30)`.
- Cloud Firestore provides limited support for logical `OR` queries. The `in` and `array-contains-any` operators 
support a logical `OR` of up to 10 equality (`==`) or `array-contains` conditions on a single field. For other cases, 
create a separate query for each `OR` condition and merge the query results in your app.