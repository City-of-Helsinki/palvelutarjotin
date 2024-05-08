from unittest.mock import patch

GET_SCHOOLS_AND_KINDERGARTENS_LIST_QUERY = """
  query ServicemapSchoolsAndKindergartensList($search: String) {
    schoolsAndKindergartensList(search: $search) {
      meta {
        count
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
    api_client,
    snapshot,
    mock_get_servicemap_schools_and_kindergartens_data,
):
    executed = api_client.execute(
        GET_SCHOOLS_AND_KINDERGARTENS_LIST_QUERY, variables={}
    )
    snapshot.assert_match(executed)


@patch(
    "servicemap.rest_client.ServicemapApiClient.list_helsinki_schools_and_kindergartens"
)
def test_list_helsinki_schools_and_kindergartens_with_search_param(
    mock_list_helsinki_schools_and_kindergartens,
    api_client,
):
    search_term = "Kannel"
    api_client.execute(
        GET_SCHOOLS_AND_KINDERGARTENS_LIST_QUERY, variables={"search": search_term}
    )
    mock_list_helsinki_schools_and_kindergartens.assert_called_once_with(
        filters={"search": search_term}
    )
