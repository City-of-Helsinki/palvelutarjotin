<!-- REMINDER: While updating changelog, also remember to update
the version in palvelutarjotin/__init.py__ -->

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
