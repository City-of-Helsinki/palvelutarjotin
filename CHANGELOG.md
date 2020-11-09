<!-- REMINDER: While updating changelog, also remember to update
the version in palvelutarjotin/__init.py__ -->


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
    
[Unreleased]: https://github.com/City-of-Helsinki/palvelutarjotin/compare/release-v0.1.0...HEAD
[0.2.0]: https://github.com/City-of-Helsinki/palvelutarjotin/compare/release-v0.1.0...v0.2.0
[0.1.0]: https://github.com/City-of-Helsinki/palvelutarjotin/releases/tag/release-v0.1.0

