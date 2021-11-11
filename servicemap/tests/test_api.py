from unittest.mock import patch

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


@patch("servicemap.schema.Query.resolve_schools_and_kindergartens_list")
def test_list_helsinki_schools_and_kindergartens(
    mock_recursive_call,
    api_client,
    snapshot,
    mock_get_servicemap_schools_and_kindergartens_data,
):
    executed = api_client.execute(GET_SCHOOLS_AND_KINDERGARTENS_LIST_QUERY)
    assert mock_recursive_call.call_count == 1
    snapshot.assert_match(executed)
