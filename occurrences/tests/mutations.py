ADD_OCCURRENCE_MUTATION = """
    mutation addOccurrence($input: AddOccurrenceMutationInput!){
      addOccurrence(input: $input){
        occurrence{
          minGroupSize
          maxGroupSize
          contactPersons{
            edges {
              node {
                name
              }
            }
          }
          startTime
          endTime
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
    }
"""


UPDATE_OCCURRENCE_MUTATION = """
mutation updateOccurrence($input: UpdateOccurrenceMutationInput!){
  updateOccurrence(input: $input){
    occurrence{
      minGroupSize
      maxGroupSize
      contactPersons{
        edges {
          node {
            name
          }
        }
      }
      startTime
      endTime
      pEvent{
        contactEmail
        contactPhoneNumber
        neededOccurrences
        enrolmentEndDays
        enrolmentStart
        externalEnrolmentUrl
        linkedEventId
        mandatoryAdditionalInformation
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
}
"""


DELETE_OCCURRENCE_MUTATION = """
mutation DeleteOccurrence($input: DeleteOccurrenceMutationInput!) {
  deleteOccurrence(input: $input) {
    __typename
  }
}
"""

ADD_VENUE_MUTATION = """
mutation AddVenue($input: AddVenueMutationInput!) {
  addVenue(input: $input) {
    venue {
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
"""

UPDATE_VENUE_MUTATION = """
mutation updateVenue($input: UpdateVenueMutationInput!) {
  updateVenue(input: $input) {
    venue {
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
"""

DELETE_VENUE_MUTATION = """
mutation DeleteVenue($input: DeleteVenueMutationInput!) {
  deleteVenue(input: $input) {
    __typename
  }
}
"""


ADD_STUDY_GROUP_MUTATION = """
mutation addStudyGroup($input: AddStudyGroupMutationInput!){
  addStudyGroup(input:$input) {
    studyGroup{
      unitId
      unitName
      unit {
        ... on ExternalPlace {
            name {
                fi
            }
        }
        ... on Place {
            internalId
            name {
                fi
            }
        }
      }
      person{
        name
        emailAddress
        phoneNumber
        language
      }
      groupSize
      groupName
      amountOfAdult
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
      extraNeeds
    }
  }
}
"""


UPDATE_STUDY_GROUP_MUTATION = """
mutation updateStudyGroup($input: UpdateStudyGroupMutationInput!){
  updateStudyGroup(input:$input) {
    studyGroup{
      unitId
      unitName
      unit {
        ... on ExternalPlace {
            name {
                fi
            }
        }
        ... on Place {
            internalId
            name {
                fi
            }
        }
      }
      person{
        name
        emailAddress
        phoneNumber
        language
      }
      groupSize
      groupName
      amountOfAdult
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
      extraNeeds
    }
  }
}
"""


DELETE_STUDY_GROUP_MUTATION = """
mutation deleteStudyGroup($input: DeleteStudyGroupMutationInput!){
  deleteStudyGroup(input: $input){
    __typename
  }
}
"""

ENROL_OCCURRENCE_MUTATION = """
mutation enrolOccurrence($input: EnrolOccurrenceMutationInput!){
  enrolOccurrence(input: $input){
    enrolments{
      studyGroup{
        unitName
      }
      occurrence{
        startTime
        seatsTaken
        seatsApproved
        remainingSeats
        amountOfSeats
        seatType
      }
      notificationType
      status
    }
  }
}
"""

UNENROL_OCCURRENCE_MUTATION = """
mutation unenrolOccurrence($input: UnenrolOccurrenceMutationInput!){
  unenrolOccurrence(input: $input){
    occurrence{
       startTime
       seatsTaken
       seatsApproved
       remainingSeats
       amountOfSeats
    }
    studyGroup{
        unitName
    }
  }
}
"""
APPROVE_ENROLMENT_MUTATION = """
mutation approveEnrolmentMutation($input: ApproveEnrolmentMutationInput!){
  approveEnrolment(input: $input){
    enrolment{
       status
    }
  }
}
"""

DECLINE_ENROLMENT_MUTATION = """
mutation declineEnrolmentMutation($input: DeclineEnrolmentMutationInput!){
  declineEnrolment(input: $input){
    enrolment{
       status
    }
  }
}
"""


UPDATE_ENROLMENT_MUTATION = """
mutation updateEnrolmentMutation($input: UpdateEnrolmentMutationInput!){
  updateEnrolment(input: $input){
    enrolment{
      studyGroup{
        unitName
        groupName
        amountOfAdult
        groupSize
        enrolments{
            edges{
               node{
                   notificationType
               }
            }
        }
      }
      occurrence{
        startTime
        seatsTaken
        seatsApproved
        remainingSeats
        amountOfSeats
      }
      notificationType
      status
    }
  }
}
"""


CANCEL_OCCURRENCE_MUTATION = """
mutation cancelOccurrenceMutation($input: CancelOccurrenceMutationInput!){
    cancelOccurrence(input: $input){
        occurrence{
            cancelled
        }
    }
}
"""

CANCEL_ENROLMENT_MUTATION = """
    mutation cancelEnrolmentMutation($input: CancelEnrolmentMutationInput!){
        cancelEnrolment(input: $input){
            enrolment{
                status
            }
        }
    }
"""


MASS_APPROVE_ENROLMENTS_MUTATION = """
mutation massApproveEnrolmentsMutation($input: MassApproveEnrolmentsMutationInput!){
  massApproveEnrolments(input: $input){
    enrolments{
       status
    }
  }
}
"""

ENROL_EVENT_QUEUE_MUTATION = """
mutation enrolEventQueue($input: EnrolEventQueueMutationInput!){
  enrolEventQueue(input: $input){
    eventQueueEnrolment{
      studyGroup{
        unitName
      }
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
      notificationType
      status
    }
  }
}
"""
