<!-- REMINDER: While updating changelog, also remember to update
the version in palvelutarjotin/__init.py__ -->

## [1.14.1](https://github.com/City-of-Helsinki/palvelutarjotin/compare/palvelutarjotin-v1.14.0...palvelutarjotin-v1.14.1) (2024-06-19)


### Bug Fixes

* Remove CREATE_SUPERUSER variable and its use ([c5a1ea1](https://github.com/City-of-Helsinki/palvelutarjotin/commit/c5a1ea1f6bea74c0b8b644ef52034930b1fcbc60))

## [1.14.0](https://github.com/City-of-Helsinki/palvelutarjotin/compare/palvelutarjotin-v1.13.0...palvelutarjotin-v1.14.0) (2024-05-16)


### Features

* Use palvelukarttaws v4 service instead of servicemap v2 ([29fbc19](https://github.com/City-of-Helsinki/palvelutarjotin/commit/29fbc19017a32cf237e8c47522a4589ab87eb89f))


### Documentation

* Updated the servicemap api root url to env file examples ([73478ce](https://github.com/City-of-Helsinki/palvelutarjotin/commit/73478ce52ae09f1f08e39e56cd9660eaeb07befc))

## [1.13.0](https://github.com/City-of-Helsinki/palvelutarjotin/compare/palvelutarjotin-v1.12.1...palvelutarjotin-v1.13.0) (2024-04-26)


### Features

* Add is_queueing_allowed & preferred_times fields ([60cb87f](https://github.com/City-of-Helsinki/palvelutarjotin/commit/60cb87fe9372c80de002123c3e1f941fc77a22f3))


### Bug Fixes

* Use correct keyword set IDs (no "qq:" prefix), remove qq altogether ([f931384](https://github.com/City-of-Helsinki/palvelutarjotin/commit/f93138461f5a4da0983e66fd121541698353eb75))
* Use correct Linked Events test URL in testing ([cf851bc](https://github.com/City-of-Helsinki/palvelutarjotin/commit/cf851bc1f22039f1e399c17161c5ef20cdcfaa24))


### Documentation

* Tidy up README.md, word wrap, fix data source, shorten wordings ([2c8f318](https://github.com/City-of-Helsinki/palvelutarjotin/commit/2c8f31828309756fb043a65ff0718ee8f52cc846))

## [1.12.1](https://github.com/City-of-Helsinki/palvelutarjotin/compare/palvelutarjotin-v1.12.0...palvelutarjotin-v1.12.1) (2024-03-14)


### Bug Fixes

* Search_fields for study group ([723e48e](https://github.com/City-of-Helsinki/palvelutarjotin/commit/723e48ea6ef31a8e01bc14701ce4cd7879d28baf))
* Slowness in the certain admin pages ([28837ba](https://github.com/City-of-Helsinki/palvelutarjotin/commit/28837ba9c34d32236c8476e2edc05551518a3d41))

## [1.12.0](https://github.com/City-of-Helsinki/palvelutarjotin/compare/palvelutarjotin-v1.11.0...palvelutarjotin-v1.12.0) (2024-02-26)


### Features

* Add keyword_OR_set event query parameters ([d704598](https://github.com/City-of-Helsinki/palvelutarjotin/commit/d7045986041c2230186a636dd6efaccb919a3a91))
* Event queue enrolment counts are included in the enrolment summary ([b0768f2](https://github.com/City-of-Helsinki/palvelutarjotin/commit/b0768f2613ffe2282a9985208527e34f570ef70e))


### Bug Fixes

* Fix OIDC tests by setting token auth settings properly in tests ([b9dbbde](https://github.com/City-of-Helsinki/palvelutarjotin/commit/b9dbbdec82d31192ff4c5ef83e0260c3c5627b2e))

## [1.11.0](https://github.com/City-of-Helsinki/palvelutarjotin/compare/palvelutarjotin-v1.10.0...palvelutarjotin-v1.11.0) (2023-12-21)


### Features

* Filter events with contact info query ([c2e2437](https://github.com/City-of-Helsinki/palvelutarjotin/commit/c2e243747a5087ca1c395b95f56390c4becd3c48))

## [1.10.0](https://github.com/City-of-Helsinki/palvelutarjotin/compare/palvelutarjotin-v1.9.0...palvelutarjotin-v1.10.0) (2023-12-11)


### Features

* Add send_upcoming_occurrence_sms_reminders management command ([a441f1b](https://github.com/City-of-Helsinki/palvelutarjotin/commit/a441f1b34c5ac959c90c7f00e3daddc2291d5dd9))


### Bug Fixes

* Type hint that does not work in CI ([065321f](https://github.com/City-of-Helsinki/palvelutarjotin/commit/065321f999bd920d415002ba387920da9a1a3281))
* Use term "place" instead of an event when place fetching fails ([98bde29](https://github.com/City-of-Helsinki/palvelutarjotin/commit/98bde2959fa4e8dcbe8d3599d596697cb18bd7c4))

## [1.9.0](https://github.com/City-of-Helsinki/palvelutarjotin/compare/palvelutarjotin-v1.8.2...palvelutarjotin-v1.9.0) (2023-09-19)


### Features

* Enforce non-empty publisher ID in organisation & new/updated event ([9f5510a](https://github.com/City-of-Helsinki/palvelutarjotin/commit/9f5510aabbeeaad520b5ec75bcf974b6ba1bff73))


### Bug Fixes

* Dockerfile base on ubi image DEVOPS-570 ([#325](https://github.com/City-of-Helsinki/palvelutarjotin/issues/325)) ([1cb08b1](https://github.com/City-of-Helsinki/palvelutarjotin/commit/1cb08b1906e224ce26cb5f9fad5f3da21e728f22))

## [1.8.2](https://github.com/City-of-Helsinki/palvelutarjotin/compare/palvelutarjotin-v1.8.1...palvelutarjotin-v1.8.2) (2023-08-23)


### Bug Fixes

* App version number PT-1652 ([#321](https://github.com/City-of-Helsinki/palvelutarjotin/issues/321)) ([ff8c5a4](https://github.com/City-of-Helsinki/palvelutarjotin/commit/ff8c5a4329a1bcf8f75776c1b8b9f91c051c6dfe))
* Don't paginate Organisations query and persons in organisations ([cbc11b8](https://github.com/City-of-Helsinki/palvelutarjotin/commit/cbc11b830873633f9d36846befa7b1cab675b53d))
* Review fixes for api/version PT-1652 ([#323](https://github.com/City-of-Helsinki/palvelutarjotin/issues/323)) ([051ccbf](https://github.com/City-of-Helsinki/palvelutarjotin/commit/051ccbfc34de6a76857ddb62b30a56cc91b57211))

## [1.8.1](https://github.com/City-of-Helsinki/palvelutarjotin/compare/palvelutarjotin-v1.8.0...palvelutarjotin-v1.8.1) (2023-06-29)


### Bug Fixes

* Netcat package update DEVOPS-541 ([#318](https://github.com/City-of-Helsinki/palvelutarjotin/issues/318)) ([83a15e5](https://github.com/City-of-Helsinki/palvelutarjotin/commit/83a15e5438ecdb5f90ed6ab5cb7b8a9219324879))

## [1.8.0] - 11 May 2023

- Allow enrolling to occurrence without notifications sending
- Fixes to the enrolment queue implementation
- Add the GDPR-person-deletion feature to the event queue enrolments
- Add PickEnrolmentFromQueueMutation to convert an event queue enrolment to an occurrence enrolment

## [1.7.0] - 27 April 2023

- Removed the enrolments, the studyGroups and the studyGroup (single) query fields from the occurrences API
- Improved data security by restricting the enrolments and study groups data with new permission checks
- Added event queue enrolments
- Refactored the long occurrence schema and test files by splitting content to new files

## [1.6.1] - 27 March 2023

- Platta configurations
- Remove beta status (affects notification templates)

## [1.6.0] - 20 January 2023

- Support for person deletion
- Support for event contact info deletion
- Add management command for deleting too old contact info
- Add enrollee person data to admin UI
- Add retention period exceeding contact info deletion cronjobs
- Filter the enrolment reports in admin by "has publisher" -filter
- Save user's last activity if the configured interval has passed
- Important fixes to test mocks

## [1.5.0] - 8 November 2022

- Tweak event enrolments CSV
- Add amount of adults to notifications

## [1.4.0] - 19 September 2022

- Disallow enrolling with an empty group

## [1.3.0] - 7 September 2022

- SMS-service can be configured off
- On multi occurrence enrolment, the related notifications are sent after all the enrolments are validated and saved

## [1.2.0] - 15 June 2022

- Dropdown filter for organisations in the person admin view
- Export features for persons in the person admin view

## [1.1.4] - 22 April 2022

### Fixed

- Event list requests to Linked events always include data source parameter
- Only sanitize keys in JSON responses from linked events

## [1.1.3] - 15 March 2022

### Updated

- Added more resources to the production environment

## [1.1.2] - 24 January 2022

### Fixed

- Prevent calling LinkedEvents API with illegal null ids

## [1.1.1] - 24 January 2022

### Updated

- Raising the errors from connection issues to LinkedEvents API when fetching data from there.
- Added more memory to production service.
- Deleting the one sided events from LinkedEvents API if an error occures while creating a PalvelutarjotinEvent to Kultus DB.

### Fixed

- Some fixes to possible null pointers.
- Fixed some setting imports for better testing abilities.
- Places and events should not be fetched when the place ids are not given

## [1.1.0] - 11 January 2022

### Added

- Search nearby events feature in API.
- Enrolment reports can be filtered with a LinkedEvent id (in admin).
- Enrolment report divisions information given in more detailed format.
- Enrolment report location information given in more detailed format.
- Added translatable auto acceptance message field to PalvelutarjotinEvent.

### Updated

- Upcoming occurrences filter returns also the ongoing occurrences.

### Fixed

- Handle HTTP410 from LinkedEvents when sending enrolment reports summary.

## [1.0.0] - 8 December 2021

### Added

- Enrolment reports model and interfaces.
- Extra needs -field added to the Enrolment report cvs's.

### Updated

- Schools and kindergartens query makes a recursive load from the Service map and returns all the results with a single query.
- Occurrences "upcoming" -filter is now renamed to "enrollable" and a new upcoming -filter that ignores the enrolmen days is created.
- Upcoming occurrences meta -field is replaced with a new pageInfo Node.

### Fixed

- Refactored and fixed the enrolment summary notifications: Only the upcoming occurrences are now summarized.
- Fixed the Graphql API enrolment groups size validation.

## [0.8.0] - 11 November 2021

### Added

- The published occurrences can now be updated if there are no enrolments yet, and deleted if they are first cancelled. New occurrences can also be added to a published event.
- Events will be republished to LinkedEvents API if the occurrences are saved and the event time range changes.
- A full Place can now be linked to a study group instead of a just name.
- Servicemap rest-client and graphql schema for schools and kindergartens query

### Updated

- Improved error handling on LinkedEvents API calls.
- Old Course-extension is removed from the Event interface and the fields are now moved to the root of the event object.

### Removed

- Unused neighborhoods API is removed.

## [0.7.3] - 8 October 2021

### Fixed

- Hotfixed PalvelutarjotinNode occurrences limit from 100 to 400 because of a real life use case.

## [0.7.2] - 8 October 2021

### Fixed

- Report view authentication.
- hel.ninja mail address changed to hel.fi (staging and production).

## [0.7.1] - 29 September 2021

### Fixed

- LinkedEvents timeout raised to 20s.

## [0.7.0] - 28 September 2021

### Added

- Notification importer: Notification templates can be imported from files (and Google sheets).

## [0.6.2] - 24 September 2021

### Fixed

- Added connection timeouts to external API requests.

## [0.6.1] - 22 September 2021

### Fixed

- Upcoming occurrences filter when enrolment end days is null.

## [0.6.0] - 21 September 2021

### Added

- Neighborhood API that fetches a list of city divisions from kartta.hel.fi.
- ExternalEnrolmentUrl field added to PalvelutarjotinEvent to offer different event enrolment types: internal enrolment, external enrolment and nonenrollable event.
- Support for event queries with all_ongoing_AND and all_ongoing_OR params.
- Added place_ids to Person to list persons own places they want to follow.

### Updated

- Increased production server limits

### Fixed

- Events pagination
- Cancelled occurrences are no longer set as next occurrence or last occurrence.
- Don't log healthchecks in production to avoid spam on server logging.

## [0.5.0] - 9 September 2021

### Updated

- Django from v. 2.2.24 to v. 3.2.5
- Django-helusers to v. 0.7.0.
- Django-ilmoitin graphql-api to v. 0.6.0.
- All the dependencies to resolve version missmatches.

### Fixed

- OIDC authentication claims validation's amr-value reading fixed by converting strings to lists.
- Checks the PalvelutarjotinEvent link existence when fetching events from LinkedEvents API.
- Occurrence deletion signals are no longer preventing deletion.
- Enrolment seats taken calculation fixed.

## [0.4.0] - 18 August 2021

### Added

- Organisation proposal model for 3rd party organisations.
- An user can be set as an administrator with a new is_admin -field. Administrators receives emails from new users.
- New users will receive a notification when their account is ready for use after registration.
- New permission "can_administrate_user_permissions" which can be used to limit the editable fields in user admin change form.
- ENVIRONMENT_URL environment variable is set to a new SITE_URL setting, which stores the server domain information.
- Type filter for organisations GraphQL -query.

### Updated

- Django updated from 2.2.20 to v. 2.2.24.
- Disallowed organisation changes on update my profile mutation. MyProfile mutations does not allow organisation changes anymore, because of security concerns.
- Improvements to multiple admin views.

### Fixed

- Report -app CSV-files support for Microsoft Excel improved.
- Multiple notification templates updated.

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
