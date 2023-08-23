# Release Notes

## [Unreleased](https://github.com/octabytes/project/compare/v2.1.0...HEAD)

### Added
* Added CHANGELOG.md to the project ([Adrian Dankiv](https://github.com/adr-007))
* Improved model.to_dict() functionality. Now it uses field names by default and includes `include_id`, `include_key`, and `include_parent` arguments ([Adrian Dankiv](https://github.com/adr-007))
* Added "count" method to FilterQuery ([Adrian Dankiv](https://github.com/adr-007))
* Fix reverse order in cursor ([Adrian Dankiv](https://github.com/adr-007))

### Changes
* Updated node version to 17.x in python-package-testing.yml ([Azeem Haider](https://github.com/AzeemHaider))

### Fixes
* Fixed DateTime with both `required=True` and `auto=True` ([Adrian Dankiv](https://github.com/adr-007))
* Fixed Model.collection.update with nested values ([Adrian Dankiv](https://github.com/adr-007))

## [v2.1.0](https://github.com/octabytes/FireO/compare/v2.0.0...v2.1.0) (2023-04-05)

### Added
* Added ability to manage documents by their IDs: get, get_all, update, delete, delete_all ([Adrian Dankiv](https://github.com/adr-007))
* Added initial type hinting ([Adrian Dankiv](https://github.com/adr-007))
* Added manager.get_key_by_id method ([Adrian Dankiv](https://github.com/adr-007))
* Added manager update tests ([Adrian Dankiv](https://github.com/adr-007))
* Added manager.update ([Adrian Dankiv](https://github.com/adr-007))
* Added model.populate_from_doc ([Adrian Dankiv](https://github.com/adr-007))

### Changes
* Modified delete(key=None) to delete_every() to delete all documents ([Adrian Dankiv](https://github.com/adr-007))
* Updated and unified codebase ([Adrian Dankiv](https://github.com/adr-007))

### Fixes
* Fixed ListField(<ItemField>) for Union and Remove ([Adrian Dankiv](https://github.com/adr-007))
* Fixed fireo.Increment for NumberField ([Adrian Dankiv](https://github.com/adr-007))
* Fixed Manager.copy ([Adrian Dankiv](https://github.com/adr-007))
* Fixed Meta inheritance ([Adrian Dankiv](https://github.com/adr-007))
* Fixed annotation_resolver_cls in TypedModelMeta ([Adrian Dankiv](https://github.com/adr-007))
* Fixed auto-creation of nested models for required fields only ([Adrian Dankiv](https://github.com/adr-007))
* Fixed limit with cursor ([Adrian Dankiv](https://github.com/adr-007))
* Fixed custom fields in meta ([Adrian Dankiv](https://github.com/adr-007))

---

## [v2.0.0](https://github.com/octabytes/FireO/compare/v1.7.0...v2.0.0) (2023-03-02)

### Added
* Added TypedModel ([Adrian Dankiv](https://github.com/adr-007))
* Added DateTime.auto_update ([Adrian Dankiv](https://github.com/adr-007))
* Added EnumField ([Adrian Dankiv](https://github.com/adr-007))
* Added IDField.include_in_document ([Adrian Dankiv](https://github.com/adr-007))
* Added Model.refresh and Model.merge_with_dict ([Adrian Dankiv](https://github.com/adr-007))
* Added Meta.column_name_generator ([Adrian Dankiv](https://github.com/adr-007))
* Added tests for ordering with nested and for Model.from_dict ([Adrian Dankiv](https://github.com/adr-007))

### Changes
* Updated google-cloud-firestore version to 2.10.0 ([AxeemHaider](https://github.com/axeemhaider))
* Updated docstring ([Adrian Dankiv](https://github.com/adr-007))
* Updated store default values in Meta class namespace ([Adrian Dankiv](https://github.com/adr-007))
* Updated minor change in _is_field_unchanged ([Adrian Dankiv](https://github.com/adr-007))
* Updated collection.parent() or .create() ([Adrian Dankiv](https://github.com/adr-007))
* Updated Meta.collection_name_generator ([Adrian Dankiv](https://github.com/adr-007))
* Updated Meta.abstract = True in default model ([Adrian Dankiv](https://github.com/adr-007))

### Fixes
* Fixed model.list_subcollections ([Adrian Dankiv](https://github.com/adr-007))
* Fixed Model._is_field_unchanged ([Adrian Dankiv](https://github.com/adr-007))
* Fixed updated with ListField ([Adrian Dankiv](https://github.com/adr-007))
* Fixed filter by document.id ([Adrian Dankiv](https://github.com/adr-007))
* Fixed Meta.collection_name_generator ([Adrian Dankiv](https://github.com/adr-007))
* Fixed unexpected attribute check ([Adrian Dankiv](https://github.com/adr-007))
* Fixed saving doc.id on batch create ([Adrian Dankiv](https://github.com/adr-007))
* Fixed error message ([Adrian Dankiv](https://github.com/adr-007))
* Fixed refactor create query to fix meta.ignore_none_field = True ([Adrian Dankiv](https://github.com/adr-007))

---

## [v1.7.0](https://github.com/octabytes/FireO/compare/v1.6.0...v1.7.0) (2023-01-31)

### Added
* Added ability to specify nested_field in ListField ([Adrian Dankiv](https://github.com/adr-007))

### Changes
* Changed error message for missing required field ([Adrian Dankiv](https://github.com/adr-007))

### Fixes
* Fixed update nested from init params ([Adrian Dankiv](https://github.com/adr-007))
* Improved error message and refactored some parts of the code ([Adrian Dankiv](https://github.com/adr-007))
* Fixed model.update ([Adrian Dankiv](https://github.com/adr-007))
* Fixed memory leak ([Adrian Dankiv](https://github.com/adr-007))
* Set Meta.ignore_none_field=False ([Adrian Dankiv](https://github.com/adr-007))

For more detailed information, please refer to the [project repository](https://github.com/octabytes/FireO).
