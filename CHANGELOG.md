<!-- REMINDER: While updating changelog, also remember to update
the version in palvelutarjotin/__init.py__ -->

## [0.3.3] - 20 May 2021

### Fixed

- Added no-cache headers to LinkedEvents REST GET calls, since LinkedEvents cache is now more aggressive.

## [0.3.2] - 17 May 2021

### Added

- Add staff-status to MyProfile -query
- JWT authentication to reports view (with DRF APIView)

### Updated

- Added a contact column to events' enrolments report

### Fixed

- Fixed mass approve mutation custom message

## [0.3.1] - 5 May 2021

### Updated

- Dependencies security patches
- Synchronize production and staging environment variables

### Fixed

- Fixed email template to use correct fallback language.

## [0.3.0] - 27 April 2021

### Added

- Send daily enrolment summary query
- Added `category` and `additional-criterial` to p_event
- Added support to query events by `keywordAnd` and `keywordNot`
- Added occurrence time validations
- Added count seats by number of enrolment
- Added `mandatory_additional_information` to p_event
- Added support for teacher to cancel their own enrolment from email
- Added `StudyLevel` query, `StudyLevel` now can be dynamically created from database
- Added support to sending notification to multiple contact people of a single enrolment
- Added index to `p_event`.`linked_event_id` to improve look up speed
- New options to `Venue` custom data
- Auto update LinkedEvent languages if occurrence `in_language` changed
- CSV export users data and enrolment data in django-admin interface

### Updated

- Limit max uploaded file size to 2MB
- Switch pipeline from Gitlab to Github Action
- Better README.md
- The amount of adults are now calculated in total study group size
- Only count the number of seat taken if enrolment is approved
- Update email templates
- Use K8s cronjob instead of uwsgi cronjob
- Staging and Production now use separated Mailgun API Key
- Dependencies security patches
- Better occurrence validation
- Only allow manual approval for single-enrolment-required events
- Improve django-admin usability

### Fixed

- Fixed `divisions` events filter
- Fixed events string argument format
- Fixed captcha handler in local development
- Fixed authentication problem by update `drf-oidc-auth` version

## [0.2.0] - 9 Nov 2020

### Added

- API to query keyword sets
- Provider API: Unpublish event API
- Added `outdoor_activity` to p_event

### Updated

- Remove duration field from occurrence
- Move `auto_acceptance` from occurrence to p_event
- `min_group_size` and `max_group_size` now become optional in occurrence
- Update README.md
- Make occurrence `seat_taken` and `seat_approved` not-nullable in the GraphQL API

### Fixed

- Fixed email header in email template

## [0.1.0] - 2 Oct 2020

### Added

- Tunnistamo authentication
- Provider APIs:
  - GraphQL API wrapper for LinkedEvent Rest API
  - API for signup/login and query provider profile
  - API to get/list add/update/delete user organisation
  - API to get/list add/update/delete LinkedEvent
  - API to get/list add/update/delete native Kultus event (linkedEvent extension data)
  - API to get/list add/update/delete event occurrence
  - API to view/approve/decline/cancel enrolment
  - API to modify study group
  - Notification service integration
  - Send notifications (SMS/Email) when receive/approve/decline/cancel enrolment
  - Send notifications (SMS/Email) when cancel occurrence
- Teacher APIs:
  - API to enrol event
  - API to query published event
  - Filtering published event by name/location/time...

[unreleased]: https://github.com/City-of-Helsinki/palvelutarjotin/compare/release-v0.3.1...HEAD
[0.3.1]: https://github.com/City-of-Helsinki/palvelutarjotin/compare/release-v0.3.0...v0.3.1
[0.3.0]: https://github.com/City-of-Helsinki/palvelutarjotin/compare/release-v0.2.0...v0.3.0
[0.2.0]: https://github.com/City-of-Helsinki/palvelutarjotin/compare/release-v0.1.0...v0.2.0
[0.1.0]: https://github.com/City-of-Helsinki/palvelutarjotin/releases/tag/release-v0.1.0
