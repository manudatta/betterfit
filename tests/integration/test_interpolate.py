import requests_mock
from app.interpolate import interpolate_and_post, api_url


def echo_payload(response, context):
    return response.json()


def test_interpolate_and_post(current, prev_two_days, interpolated_result_two_days):
    json_payload = [obj.to_json() for obj in interpolated_result_two_days]
    with requests_mock.Mocker() as m:
        m.register_uri("POST", api_url, json=echo_payload)
        assert json_payload == interpolate_and_post(current, prev_two_days).json()
