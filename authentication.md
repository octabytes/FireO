---
layout: default
title: Authentication
nav_order: 2
---

# Authentication
{: .no_toc }

To use FireO you first need to connect it with Google Firestore
{: .fs-6 .fw-300 }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

[Read more about](https://googleapis.dev/python/google-api-core/latest/auth.html) How to authenticate FireO.

## Google Cloud Platform

If you’re running in Compute Engine or App Engine, authentication should “just work”.

## Local Development

If you’re developing locally, the easiest way to authenticate is using the [Google Cloud SDK](http://cloud.google.com/sdk)

```shell
$ gcloud auth application-default login
``` 

Note that this command generates credentials for client libraries. To authenticate the CLI itself, use

```shell
$ gcloud auth login
``` 

Previously, gcloud auth login was used for both use cases. If your gcloud installation does not support the new command, please update it


```shell
$ gcloud components update
``` 

## Service Account

If you’re running your application elsewhere, you should download a service [account JSON](https://cloud.google.com/storage/docs/authentication#generating-a-private-key) keyfile and point to it using an environment variable

```shell
$ export GOOGLE_APPLICATION_CREDENTIALS="/path/to/keyfile.json"
```

or you can pass JSON file in FireO connection

```python
db.connect(from_file="/path/to/keyfile.json")
```

## Explicit Credentials

The Application Default Credentials discussed above can be useful if your code needs to run in many different environments or if you just don’t want authentication to be a focus in your code.

However, you may want to be explicit because

- your code will only run in one place
- you may have code which needs to be run as a specific service account every time (rather than with the locally inferred credentials)
- you may want to use two separate accounts to simultaneously access data from different projects

In these situations, you can create an explicit [Credentials](https://google-auth.readthedocs.io/en/stable/reference/google.auth.credentials.html#google.auth.credentials.Credentials) object suited to your environment. After creation, you can pass it directly to a Connection

```python
db.connect(credentials=credentials)
```

## Read more

[Read more about](https://googleapis.dev/python/google-api-core/latest/auth.html) How to authenticate FireO.
