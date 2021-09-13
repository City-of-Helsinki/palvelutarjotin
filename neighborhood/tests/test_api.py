GET_NEIGHBORHOOD_LIST_QUERY = """
  query NeighborhoodList {
    neighborhoodList {
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


def test_get_neighborhood_list(api_client, snapshot, mock_get_neighborhood_list_data):
    executed = api_client.execute(GET_NEIGHBORHOOD_LIST_QUERY)
    snapshot.assert_match(executed)
