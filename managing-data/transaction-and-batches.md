---
layout: default
title: Transaction and batches
parent: Managing Data
nav_order: 3
---

# Transactions and batched writes
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---
FireO supports atomic operations for reading and writing data. In a set of atomic operations, 
either all of the operations succeed, or none of them are applied. 
There are two types of atomic operations in FireO:

- **Transactions:** a transaction is a set of read and write operations on one or more documents.
- **Batched Writes:** a batched write is a set of write operations on one or more documents.

Each transaction or batch of writes can write to a maximum of 500 documents. 
For additional limits related to writes, see [Quotas and Limits.](https://cloud.google.com/firestore/docs/quotas#writes_and_transactions)

## Updating data with transactions
Using the FireO library, you can group multiple operations into a single transaction. 
Transactions are useful when you want to update a field's value based on its current value, 
or the value of some other field.

A transaction consists of any number of `get()` operations followed by any number of write operations 
such as `create()`, `update()`, or `delete()`. In the case of a concurrent edit, Cloud Firestore runs 
the entire transaction again. For example, if a transaction reads documents and another client 
modifies any of those documents, Cloud Firestore retries the transaction. This feature ensures 
that the transaction runs on up-to-date and consistent data.

Transactions never partially apply writes. All writes execute at the end of a successful transaction.

When using transactions, note that:

- Read operations must come before write operations.
- A function calling a transaction (transaction function) might run more than once if a 
    concurrent edit affects a document that the transaction reads.
- Transaction functions should not directly modify application state.
- Transactions will fail when the client is offline.

The following example shows how to create and run a transaction:

```python
transaction = fireo.transaction()

@fireo.transactional
def update_in_transaction(transaction, city_key):
    city = City.collection.get(city_key, transaction)
    city.population = city.population + 1
    city.update(transaction=transaction)

update_in_transaction(transaction, city_key)
```

## Passing information out of transactions
Do not modify application state inside of your transaction functions. 
Doing so will introduce concurrency issues, because transaction functions can run 
multiple times and are not guaranteed to run on the UI thread. Instead, pass information 
you need out of your transaction functions. The following example builds on the previous 
example to show how to pass information out of a transaction:

```python
transaction = fireo.transaction()

@fireo.transactional
def update_in_transaction(transaction, city_key):
    city = City.collection.get(city_key, transaction)
    new_population = city.population + 1
    if new_population < 1000000:
        city.population = new_population
        city.update(transaction=transaction)
        return True
    else:
        return False

result = update_in_transaction(transaction, city_key)
if result:
    print('Population updated')
else:
    print('Sorry! Population is too big.')
```

## Transaction in filter query
You can also apply transaction on filter queries.

```python
transaction = fireo.transaction()

@fireo.transactional
def update_in_transaction(transaction):
    city = City.collection.filter('state', '==', 'CA').transaction(transaction).get()
    city.population = city.population + 1
    city.update(transaction=transaction)

update_in_transaction(transaction)
```

## Transaction failure
A transaction can fail for the following reasons:

- The transaction contains read operations after write operations. Read operations must 
    always come before any write operations.
- The transaction read a document that was modified outside of the transaction. In this case, 
    the transaction automatically runs again. The transaction is retried a finite number of times.
- The transaction exceeded the maximum request size of 10 MiB.
    Transaction size depends on the sizes of documents and index entries modified by 
    the transaction. For a delete operation, this includes the size of the target document 
    and the sizes of the index entries deleted in response to the operation.

A failed transaction returns an error and does not write anything to the database. 
You do not need to roll back the transaction; Cloud Firestore does this automatically.

## Batched writes
If you do not need to read any documents in your operation set, you can execute multiple write operations 
as a single batch that contains any combination of `create()`, `update()`, or `delete()` operations. 
A batch of writes completes atomically and can write to multiple documents. 
The following example shows how to build and commit a write batch:

```python
batch = fireo.batch()

# Create the data for NYC
City.collection.create(batch=batch, state='NYC', population=500000)

# Update the population for SF
city = City()
city.population = 1000000
city.update(batch=batch)

# Delete LA
City.collection.delete(key=city.key, batch=batch)

# Commit the batch
batch.commit()
```

Document can also `delete()` by `filter` operation

```python
City.collection.filter('state', '==', 'CA').batch(batch).delete()
```

A batched write can contain up to 500 operations. Each operation in the batch counts separately 
towards your Cloud Firestore usage. Within a write operation, field transforms like `serverTimestamp`, 
`ListUnion`, and `increment` each count as an additional operation.

Like transactions, batched writes are atomic. Unlike transactions, batched writes do not need to ensure 
that read documents remain un-modified which leads to fewer failure cases.