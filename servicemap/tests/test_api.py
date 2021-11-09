GET_SCHOOLS_AND_KINDERGARTENS_LIST_QUERY = """
  query ServicemapSchoolsAndKindergartensList {
    schoolsAndKindergartensList {
      meta {
        count
        next
        previous
      }
      data {
        id
        name {
          fi
          sv
          en
        }
      }
    }
  }
  """


def test_list_helsinki_schools_and_kindergartens(
    api_client, snapshot, mock_get_servicemap_schools_and_kindergartens_data
):
    executed = api_client.execute(GET_SCHOOLS_AND_KINDERGARTENS_LIST_QUERY)
    snapshot.assert_match(executed)
