/* eslint-disable */
import { sleep } from 'k6';
import http from 'k6/http';

export const options = {
  duration: '10m',
  vus: 20,
  //  vus: 1,
  thresholds: {
    //avg is around ?800ms? on https://palvelutarjotin-api.test.kuva.hel.ninja
    http_req_duration: ['p(95)<5000'],
  },
};

export default () => {
  const url = 'https://palvelutarjotin-api.test.kuva.hel.ninja/graphql';
  const data = 'query=query Organisations {organisations {edges {node {id } } } }';
  const res = http.post(url, data, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });

  //10 loads per minute
  sleep(6);
};
