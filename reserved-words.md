---
layout: default
title: Reserved Words
nav_order: 8
---

# Reserved Words
{: .no_toc }

Following list is reserved words by FireO. Don't use these words in Model or in custom fields
{: .fs-6 .fw-300 }

---

| Word            | Description                                                                      |
|:----------------|:---------------------------------------------------------------------------------|
| id              | Used to store model id, You can use it but only for [IDField](/fields/id-field)  |
| key, _key             | Store the model key, Don't use it                                                |
| parent          | Save the parent model key                                                        |
| update_doc      | Contain information for updating the model                                       |
| collection_name | Name of the collection, don't override it manually, See [Meta class](/meta-class/#collection-name)|
| collection      | Default Manager to operate Firestore operation                                   |
| field_list      | list of fields |
| field_changed   | Changed fields when updating |
| instance_modified | Model is modified after saving or updating |
| _meta           | Store information about model |