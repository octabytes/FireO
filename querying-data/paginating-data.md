---
layout: default
title: Paginating Data
parent: Querying Data
nav_order: 5
---

# Paginating Data
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

FireO split data returned by a query into batches according to the parameters you define in your query.

## Next Fetch
You can easily fetch next batch by using `next_fetch()` method.

### Usage Example

```python
cities = City.collection.filter('state', '==', 'CA').order('population').fetch(10)

# Print first 10 cities with this matching condition
for city in cities:
    print(city)

# Fetch next batch
cities.next_fetch()

# Print 10 more cities with this matching condition
for city in cities:
    print(city)
```

You can call `next_fetch()` method as many time as you want until the records finish.
In `next_fetch()` you can also change the limit. But this limit is only for this fetch and will not effect
further `next_fetch()`

### Example with limit

```python
cities = City.collection.filter('state', '==', 'CA').order('population').fetch(10)

# Print first 10 cities with this matching condition
for city in cities:
    print(city)

# Fetch next batch
cities.next_fetch(5)

# Print 5 more cities with this matching condition
for city in cities:
    print(city)

# Another next fetch batch
cities.next_fetch()

# Print more 10 cities with this matching condition
for city in cities:
    print(city)
```

## Query cursor
This is powerful tool by FireO. You can create `cursor` from your query and save it as `string` and use it later.

### Example Usage

```python
cities = City.collection.filter('state', '==', 'CA').order('population').fetch(10)

# city list contain the first 10 matching cities
city_list = list(cities)

city_cursor = cities.cursor
```

`cities.cursor` return the `string` that you can use later at some place to start the query at this specific 
point.

```python
# Fetch another 10 cities 
cities = City.collection.cursor(city_cursor).fetch()

for city in cities:
    print(city)
```

You can also change the limit when using `fetch()` unlike `next_fetch()` this will effect the further `fetch()`

```python
# Fetch another 5 cities 
cities = City.collection.cursor(city_cursor).fetch(5)

city_list = list(cities)

city_cursor = cities.cursor

# it will fetch the next 5 cities
cities = City.collection.cursor(city_cursor).fetch()

for city in cities:
    print(city)
```

### Important Note

`cursor` use the last document or offset to point the query. It is recommend to use the last document for further
fetch batches. You need to understand how to create `cursor` with last document

```python
cities = City.collection.filter('state', '==', 'CA').order('population').fetch(10)

offset_cursor = cities.cursor

# city list contain the first 10 matching cities
city_list = list(cities)

last_doc_cursor = cities.cursor

print(offset_cursor)
print(last_doc_cursor)
```

You will see both `cursor` are different generating from same query. If you call the `cities.cursor` before 
consuming the `cities` then `cursor` save the **offset** for next fetch because it does not know the last 
document until you use all the results generating from the query. 

**Important tip always save cursor after using the results if possible**

## Start After
Use the `start_after()` methods to define the start point for a query. 

For example if you use `start_after(A)` it returns alphabet from `B-Z`

### Usage Example
{: .no_toc }

```python
cities = City.collection.order('state').start_after(population=1000000)
```

You can also pass the model `key` to define the query point where to start

### Example
{: .no_toc }

```python
cities = City.collection.order('state').start_after(key=model.key)
```

## Start At
Use the `start_at()` methods to define the start point for a query. 

For example if you use `start_at(A)` it returns entire alphabet.

### Usage Example
{: .no_toc }

```python
cities = City.collection.order('state').start_at(population=1000000)
```

## End Before
Use the `end_before()` methods to define the end point for a query. 

### Usage Example
{: .no_toc }

```python
cities = City.collection.order('state').end_before(population=1000000)
```

## End At
Use the `end_at()` methods to define where to end the query.

### Usage Example
{: .no_toc }

```python
cities = City.collection.order('state').end_at(population=1000000)
```