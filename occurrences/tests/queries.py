LANGUAGES_QUERY = """
    query Languages{
        languages {
            edges {
                node {
                    id
                    name
                }
            }
        }
    }
"""

LANGUAGE_QUERY = """
    query Language($id: ID!){
        language(id: $id) {
            id
            name
        }
    }
"""


STUDY_LEVELS_QUERY = """
    query StudyLevels{
        studyLevels {
            edges {
                node {
                    id
                    label
                    level
                    translations {
                        languageCode
                        label
                    }
                }
            }
        }
    }
"""

STUDY_LEVEL_QUERY = """
    query StudyLevel($id: ID!){
        studyLevel(id: $id){
            id
            label
            level
            translations {
                languageCode
                label
            }
        }
    }
"""

OCCURRENCES_QUERY = """
query Occurrences(
    $upcoming: Boolean,
    $enrollable: Boolean,
    $date: Date,
    $time: Time,
    $cancelled: Boolean,
    $pEvent: ID,
    $orderBy: [String]
){
  occurrences(
      upcoming: $upcoming,
      enrollable: $enrollable,
      date: $date,
      time: $time,
      cancelled: $cancelled,
      pEvent: $pEvent,
      orderBy: $orderBy
  ){
    edges{
      node{
        placeId
        amountOfSeats
        remainingSeats
        seatsTaken
        seatsApproved
        seatType
        pEvent{
            contactEmail
            contactPhoneNumber
            neededOccurrences
            enrolmentEndDays
            enrolmentStart
            externalEnrolmentUrl
            linkedEventId
            autoAcceptance
            mandatoryAdditionalInformation
        }
        startTime
        endTime
        minGroupSize
        maxGroupSize
        contactPersons {
          edges {
            node {
              name
            }
          }
        }
      }
    }
  }
}
"""

OCCURRENCE_QUERY = """
query Occurrence($id: ID!){
  occurrence(id: $id){
    placeId
    pEvent{
        contactEmail
        contactPhoneNumber
        neededOccurrences
        enrolmentEndDays
        enrolmentStart
        externalEnrolmentUrl
        linkedEventId
        autoAcceptance
        mandatoryAdditionalInformation
    }
    linkedEvent{
        name {
           en
           fi
           sv
        }
    }
    startTime
    endTime
    amountOfSeats
    remainingSeats
    seatsTaken
    seatsApproved
    minGroupSize
    maxGroupSize
    contactPersons {
      edges {
        node {
          name
        }
      }
    }
    languages{
        edges {
            node {
                id
                name
            }
        }
    }
  }
}
"""


VENUES_QUERY = """
query Venues {
  venues {
    edges {
      node {
        id
        description
        translations {
          description
        }
        hasClothingStorage
        hasSnackEatingPlace
        outdoorActivity
        hasToiletNearby
        hasAreaForGroupWork
        hasIndoorPlayingArea
        hasOutdoorPlayingArea
      }
    }
  }
}
"""

VENUE_QUERY = """
query venue($id:ID!){
  venue(id: $id){
    id
    description,
    translations{
      description
    }
    hasClothingStorage
    hasSnackEatingPlace
    outdoorActivity
    hasToiletNearby
    hasAreaForGroupWork
    hasIndoorPlayingArea
    hasOutdoorPlayingArea
  }
}
"""


NOTIFICATION_TEMPLATE_QUERY = """
query NotificationTemplate($type: NotificationTemplateType!, $language: Language!,
$context:JSONString!){
  notificationTemplate(templateType: $type, language: $language, context: $context){
    template{
        type
    }
    customContextPreviewHtml
    customContextPreviewText
  }
}
"""


ENROLMENT_QUERY = """
query enrolment($id: ID!){
  enrolment(id: $id){
    occurrence{
      seatsTaken
      startTime
      endTime
      pEvent{
        linkedEventId
      }
    }
    studyGroup{
      groupName
    }
    status
  }
}
"""

ENROLMENTS_SUMMARY_QUERY = """
query enrolmentSummary($organisationId: ID!, $status: EnrolmentStatus){
  enrolmentSummary(organisationId: $organisationId, status:$status){
    count
    edges{
      node{
        status
      }
    }
  }
}
"""

CANCEL_ENROLMENT_QUERY = """
query cancellingEnrolment($id: ID!){
    cancellingEnrolment(id: $id){
        enrolmentTime
        status
        occurrence{
            seatsTaken
        }
        studyGroup{
            unitName
            groupSize
        }
    }
}
"""


EVENT_QUEUE_ENROLMENTS_QUERY = """
query eventQueueEnrolments(
  $pEventId: ID,
  $orderBy: [String],
  $first: Int,
  $after: String
){
  eventQueueEnrolments(
    pEventId: $pEventId,
    orderBy: $orderBy,
    first: $first,
    after: $after
  ){
    count
    edges{
      cursor
      node{
        pEvent{
          linkedEventId
        }
        studyGroup{
          groupName
        }
        status
      }
    }
  }
}
"""

EVENT_QUEUE_ENROLMENT_QUERY = """
query eventQueueEnrolment(
  $id: ID!
){
  eventQueueEnrolment(
    id: $id,
  ){
    pEvent{
      linkedEventId
    }
    studyGroup{
      groupName
    }
    status
  }
}
"""
