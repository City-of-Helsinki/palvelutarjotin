import enum
from enum import auto

import graphene
import pytest

from common.utils import (
    deepfix_enum_values,
    is_enum_value,
    map_enums_to_values_in_kwargs,
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
        {1, 2, 3, "test", 2},
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
