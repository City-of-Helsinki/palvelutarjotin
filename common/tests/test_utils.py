import enum
from datetime import datetime, timedelta
from datetime import timezone as datetime_timezone
from enum import auto
from zoneinfo import ZoneInfo

import graphene
import pytest
from django.http import HttpRequest
from django.test.utils import override_settings
from django.utils import timezone

from common.utils import (
    deepfix_enum_values,
    get_client_ip,
    is_enum_value,
    map_enums_to_values_in_kwargs,
    to_local_datetime_if_naive,
)


class _OrderEnum(graphene.Enum):
    FIRST = 1
    SECOND = 2


class _TestEnum(enum.Enum):
    TEST = "test_1"
    TEST_2 = 2


class _TestGrapheneEnum(graphene.Enum):
    FIRST_ENUM_NAME = "FIRST_ENUM_VALUE"
    ENUM_NAME_1 = "ENUM_VALUE_1"
    ENUM_NAME_2 = "ENUM_VALUE_2"
    LAST_ENUM_NAME = "LAST_ENUM_VALUE"


class _TestGrapheneEnumAuto(graphene.Enum):
    _123 = auto()
    test = auto()


@pytest.mark.parametrize(
    "value",
    [
        _TestEnum.TEST,
        _TestEnum.TEST_2,
        _TestGrapheneEnum.FIRST_ENUM_NAME,
        _TestGrapheneEnum.ENUM_NAME_1,
        _TestGrapheneEnum.ENUM_NAME_2,
        _TestGrapheneEnum.LAST_ENUM_NAME,
        _TestGrapheneEnumAuto._123,
        _TestGrapheneEnumAuto.test,
    ],
)
def test_is_enum_value_true(value):
    assert is_enum_value(value) is True


@pytest.mark.parametrize(
    "value",
    [
        None,
        0,
        1,
        2,
        "0",
        "1",
        "2",
        "FIRST_ENUM_VALUE",
        "ENUM_VALUE_1",
        "ENUM_VALUE_2",
        "LAST_ENUM_VALUE",
    ],
)
def test_is_enum_value_false(value):
    assert is_enum_value(value) is False


@pytest.mark.parametrize(
    "input",
    [
        None,
        0,
        1,
        2,
        "0",
        "1",
        "2",
        "FIRST_ENUM_VALUE",
        "ENUM_VALUE_1",
        "ENUM_VALUE_2",
        "LAST_ENUM_VALUE",
        {1, 2, 3, "test"},
        (1, 2, 3, "test", 2),
        [1, 2, 3, "test", 2],
        (1, [2, {3: {4, (11, (12,), 13, None, "test")}}]),
    ],
)
def test_deepfix_enum_values_unchanged(input):
    assert deepfix_enum_values(input) == input


def test_deepfix_enum_values_changes_output_but_not_input():
    """
    Test that the input is not modified even when the output is.
    """
    input = {_TestEnum.TEST: "test"}
    assert deepfix_enum_values(input) == {"test_1": "test"}
    assert input == {_TestEnum.TEST: "test"}


@pytest.mark.parametrize(
    "input,expected_output",
    [
        (_TestEnum.TEST, "test_1"),
        (_TestEnum.TEST_2, 2),
        (_TestGrapheneEnum.FIRST_ENUM_NAME, "FIRST_ENUM_VALUE"),
        (_TestGrapheneEnum.ENUM_NAME_1, "ENUM_VALUE_1"),
        (_TestGrapheneEnum.ENUM_NAME_2, "ENUM_VALUE_2"),
        (_TestGrapheneEnum.LAST_ENUM_NAME, "LAST_ENUM_VALUE"),
        (_TestGrapheneEnumAuto._123, 1),
        (_TestGrapheneEnumAuto.test, 2),
        (
            [_TestGrapheneEnumAuto.test, _TestEnum.TEST, 123, "TEST"],
            [2, "test_1", 123, "TEST"],
        ),
        ({_TestEnum.TEST: "test"}, {"test_1": "test"}),
        (
            {
                _TestEnum.TEST: [
                    "test",
                    "123",
                    1234,
                    _TestGrapheneEnumAuto.test,
                    (
                        _TestEnum.TEST_2,
                        _TestGrapheneEnum.ENUM_NAME_1,
                        _TestGrapheneEnumAuto.test,
                    ),
                    {
                        _TestGrapheneEnumAuto.test,
                        "not_enum",
                        _TestEnum.TEST,
                        _TestEnum.TEST_2,
                    },
                    {
                        "not_enum_key": "not_enum_value",
                        _TestEnum.TEST: _TestGrapheneEnumAuto.test,
                    },
                    (_TestGrapheneEnumAuto.test, _TestEnum.TEST, "not_enum"),
                    [_TestEnum.TEST, _TestGrapheneEnumAuto.test],
                    _TestGrapheneEnumAuto.test,
                ],
                _TestGrapheneEnum.ENUM_NAME_1: {
                    _TestEnum.TEST_2,
                    _TestGrapheneEnumAuto.test,
                    _TestGrapheneEnum.ENUM_NAME_1,
                },
            },
            {
                "test_1": [
                    "test",
                    "123",
                    1234,
                    2,
                    (2, "ENUM_VALUE_1", 2),
                    {2, "not_enum", "test_1"},
                    {"not_enum_key": "not_enum_value", "test_1": 2},
                    (2, "test_1", "not_enum"),
                    ["test_1", 2],
                    2,
                ],
                "ENUM_VALUE_1": {
                    2,
                    "ENUM_VALUE_1",
                },
            },
        ),
        (
            (
                _TestEnum.TEST,
                [
                    _TestEnum.TEST_2,
                    {
                        _TestGrapheneEnum.FIRST_ENUM_NAME: {
                            _TestGrapheneEnum.ENUM_NAME_1,
                            (_TestGrapheneEnum.ENUM_NAME_2,),
                            _TestGrapheneEnum.LAST_ENUM_NAME,
                        }
                    },
                ],
            ),
            (
                "test_1",
                [
                    2,
                    {
                        "FIRST_ENUM_VALUE": {
                            "ENUM_VALUE_1",
                            ("ENUM_VALUE_2",),
                            "LAST_ENUM_VALUE",
                        }
                    },
                ],
            ),
        ),
    ],
)
def test_deepfix_enum_values_changed(input, expected_output):
    assert deepfix_enum_values(input) == expected_output


@pytest.mark.parametrize("args", [(), ("testing", 1234, ["a", 1, 2, "b"])])
@pytest.mark.parametrize(
    "kwargs,expected_kwargs",
    [
        ({"x": _OrderEnum.FIRST}, {"x": 1}),
        ({"x": _OrderEnum.SECOND}, {"x": 2}),
        ({"x": _OrderEnum.FIRST, "y": _OrderEnum.SECOND}, {"x": 1, "y": 2}),
        (
            {
                "order_priority_reverse_mapping": [
                    {
                        1: [_OrderEnum.SECOND, _OrderEnum.FIRST],
                        2: [_OrderEnum.FIRST, _OrderEnum.SECOND],
                    },
                    "test",
                    1,
                    2,
                    3,
                    _OrderEnum.FIRST,
                    _OrderEnum.SECOND,
                    3,
                ]
            },
            {
                "order_priority_reverse_mapping": [
                    {
                        1: [2, 1],
                        2: [1, 2],
                    },
                    "test",
                    1,
                    2,
                    3,
                    1,
                    2,
                    3,
                ]
            },
        ),
    ],
)
def test_map_enums_to_values_in_kwargs(args, kwargs, expected_kwargs):
    @map_enums_to_values_in_kwargs
    def method(*args, **kwargs):
        return (args, kwargs)

    assert method(*args, **kwargs) == (args, expected_kwargs)


@pytest.mark.parametrize(
    "value,expected_output",
    [
        ("2020-12-30", datetime(2020, 12, 30, tzinfo=ZoneInfo("Asia/Tokyo"))),
        ("2023-05-21", datetime(2023, 5, 21, tzinfo=ZoneInfo("Asia/Tokyo"))),
        (
            "2024-03-29T12:34:56.123456+05:00",
            datetime(
                2024,
                3,
                29,
                12,
                34,
                56,
                microsecond=123456,
                # +05:00 UTC offset from input string
                tzinfo=datetime_timezone(timedelta(seconds=5 * 60 * 60)),
            ),
        ),
    ],
)
@override_settings(USE_TZ=True, TIMEZONE="Asia/Tokyo")
def test_to_local_datetime_if_naive(settings, value, expected_output):
    with timezone.override(settings.TIMEZONE):
        assert to_local_datetime_if_naive(value) == expected_output


@pytest.mark.parametrize("value", [None, False, 0, 123, _TestEnum.TEST])
def test_to_local_datetime_if_naive_raises_type_error(value):
    with pytest.raises(TypeError):
        to_local_datetime_if_naive(value)


@pytest.mark.parametrize(
    "value", ["today", "2300-02-32", "approved", "Enrolment.STATUS_APPROVED"]
)
def test_to_local_datetime_if_naive_raises_value_error(value):
    with pytest.raises(ValueError):
        to_local_datetime_if_naive(value)


@override_settings(USE_TZ=True)
def test_to_local_datetime_if_naive_uses_current_timezone(settings):
    settings.TIMEZONE = "Europe/Helsinki"
    with timezone.override(settings.TIMEZONE):
        assert to_local_datetime_if_naive("2020-12-30").tzinfo == ZoneInfo(
            "Europe/Helsinki"
        )
    settings.TIMEZONE = "Australia/Sydney"
    with timezone.override(settings.TIMEZONE):
        assert to_local_datetime_if_naive("2020-12-30").tzinfo == ZoneInfo(
            "Australia/Sydney"
        )
    settings.TIMEZONE = "America/New_York"
    with timezone.override(settings.TIMEZONE):
        assert to_local_datetime_if_naive("2020-12-30").tzinfo == ZoneInfo(
            "America/New_York"
        )


class TestGetClientIP:
    def test_get_client_ip_x_forwarded_for(self):
        request = HttpRequest()
        request.META = {"HTTP_X_FORWARDED_FOR": "192.168.1.1, 10.0.0.1"}
        assert get_client_ip(request) == "192.168.1.1"

    def test_get_client_ip_x_forwarded_for_with_whitespace(self):
        request = HttpRequest()
        request.META = {"HTTP_X_FORWARDED_FOR": "  192.168.1.1  , 10.0.0.1"}
        assert get_client_ip(request) == "192.168.1.1"

    def test_get_client_ip_remote_addr(self):
        request = HttpRequest()
        request.META = {"REMOTE_ADDR": "127.0.0.1"}
        assert get_client_ip(request) == "127.0.0.1"

    def test_get_client_ip_no_headers(self):
        request = HttpRequest()
        request.META = {}
        assert get_client_ip(request) is None

    def test_get_client_ip_remote_addr_and_x_forwarded_for(self):
        request = HttpRequest()
        request.META = {
            "REMOTE_ADDR": "127.0.0.1",
            "HTTP_X_FORWARDED_FOR": "192.168.1.1",
        }
        assert get_client_ip(request) == "192.168.1.1"

    def test_get_client_ip_x_forwarded_for_empty(self):
        request = HttpRequest()
        request.META = {"HTTP_X_FORWARDED_FOR": ""}
        assert get_client_ip(request) is None

    def test_get_client_ip_remote_addr_empty(self):
        request = HttpRequest()
        request.META = {"REMOTE_ADDR": ""}
        assert get_client_ip(request) is None


class TestGetClientIPWithPort:
    """Tests the get_client_ip function's ability to handle IP addresses
    that include port numbers in the request metadata.
    """

    def test_get_client_ip_remote_addr_with_ipv4_port(self):
        """
        Tests retrieving an IPv4 address from REMOTE_ADDR when it includes a
        port number. The function should return only the IP address.

        Case Example: A direct connection from a client with IP '192.168.1.1'
        using port '12345' to the server. REMOTE_ADDR might be '192.168.1.1:12345'.
        """
        request = HttpRequest()
        request.META = {"REMOTE_ADDR": "192.168.1.1:12345"}
        assert get_client_ip(request) == "192.168.1.1"

    def test_get_client_ip_remote_addr_with_ipv6_port(self):
        """
        Tests retrieving an IPv6 address from REMOTE_ADDR (with brackets) when it
        includes a port number. The function should return only the IP address.

        Case Example: A direct IPv6 connection where the client's address is '[::1]'
        and the connection uses port '8080'. REMOTE_ADDR might be '[::1]:8080'.
        """
        request = HttpRequest()
        request.META = {"REMOTE_ADDR": "[::1]:8080"}
        assert get_client_ip(request) == "::1"

    def test_get_client_ip_remote_addr_with_ipv6_port_complex(self):
        """
        Tests retrieving a more complex IPv6 address from REMOTE_ADDR (with brackets)
        when it includes a port number. The function should return only the IP address.

        Case Example: A direct IPv6 connection with a more involved address
        '[2001:0db8:85a3:0000:0000:8a2e:0370:7334]' using port '5432'.
        REMOTE_ADDR might be '[2001:0db8:85a3:0000:0000:8a2e:0370:7334]:5432'.
        """
        request = HttpRequest()
        request.META = {"REMOTE_ADDR": "[2001:0db8:85a3:0000:0000:8a2e:0370:7334]:5432"}
        assert get_client_ip(request) == "2001:0db8:85a3:0000:0000:8a2e:0370:7334"

    def test_get_client_ip_remote_addr_ipv4_with_non_numeric_port(self):
        """
        Tests handling an edge case where REMOTE_ADDR contains an IPv4 address
        followed by a non-numeric port. The function should still extract the IP.

        Case Example: A misconfigured client or intermediary sends a non-standard
        REMOTE_ADDR like '192.168.1.1:abc'.
        """
        request = HttpRequest()
        request.META = {"REMOTE_ADDR": "192.168.1.1:abc"}
        assert get_client_ip(request) == "192.168.1.1"

    def test_get_client_ip_remote_addr_ipv6_with_non_numeric_port(self):
        """
        Tests handling an edge case where REMOTE_ADDR contains an IPv6 address
        (with brackets) followed by a non-numeric port. The function should still
        extract the IP.

        Case Example: A misconfigured client or intermediary sends a non-standard
        REMOTE_ADDR like '[::1]:xyz'.
        """
        request = HttpRequest()
        request.META = {"REMOTE_ADDR": "[::1]:xyz"}
        assert get_client_ip(request) == "::1"

    def test_get_client_ip_x_forwarded_for_with_port_should_ignore(self):
        """
        Tests that if the X-Forwarded-For header (which typically doesn't include
        ports) contains an IP with a port, the function correctly extracts the IP.

        Case Example: A proxy might incorrectly forward the client's IP with a port
        in the X-Forwarded-For header as '192.168.1.1:9999'.
        """
        request = HttpRequest()
        request.META = {"HTTP_X_FORWARDED_FOR": "192.168.1.1:9999"}
        assert get_client_ip(request) == "192.168.1.1"

    def test_get_client_ip_x_forwarded_for_multiple_with_port(self):
        """
        Tests handling the X-Forwarded-For header with multiple IP addresses, where
        the first IP (the client's original IP) includes a port number. The function
        should return the IP without the port.

        Case Example: Multiple proxies are involved, and the first proxy (closest
        to the client) forwards the IP with a port: '192.168.1.1:1111, 10.0.0.1'.
        """
        request = HttpRequest()
        request.META = {"HTTP_X_FORWARDED_FOR": "192.168.1.1:1111, 10.0.0.1"}
        assert get_client_ip(request) == "192.168.1.1"

    def test_get_client_ip_x_forwarded_for_multiple_with_whitespace_and_port(self):
        """
        Tests handling the X-Forwarded-For header with multiple IP addresses, where
        the first IP has leading/trailing whitespace and includes a port number.
        The function should return the clean IP without the port.

        Case Example: Poorly formatted X-Forwarded-For header:
        '  192.168.1.1:2222  , 10.0.0.1'.
        """
        request = HttpRequest()
        request.META = {"HTTP_X_FORWARDED_FOR": "  192.168.1.1:2222  , 10.0.0.1"}
        assert get_client_ip(request) == "192.168.1.1"

    def test_get_client_ip_remote_addr_ipv6_no_brackets_with_port(self):
        """
        Tests retrieving an IPv6 address from REMOTE_ADDR (without brackets), which
        might occur in some older systems, when it includes a port number. The
        function should return only the IP address.

        Case Example: A direct IPv6 connection from an older client or through
        a system that doesn't use brackets in REMOTE_ADDR: '::1:80'.
        """
        request = HttpRequest()
        request.META = {"REMOTE_ADDR": "::1:80"}
        assert get_client_ip(request) == "::1"

    def test_get_client_ip_remote_addr_ipv6_complex_no_brackets_with_port(self):
        """
        Tests retrieving a more complex IPv6 address from REMOTE_ADDR (without
        brackets) when it includes a port number. The function should return only
        the IP address.

        Case Example: A direct complex IPv6 connection without brackets where the
        port is appended: '2001:db8:85a3::8a2e:370:7334:65535'.
        """
        request = HttpRequest()
        request.META = {"REMOTE_ADDR": "2001:db8:85a3::8a2e:370:7334:65535"}
        assert get_client_ip(request) == "2001:db8:85a3::8a2e:370:7334"
