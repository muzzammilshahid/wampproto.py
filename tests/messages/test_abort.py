import pytest

from wampproto.messages import exceptions
from wampproto.messages.abort import Abort


def test_parse_with_invalid_type():
    message = "msg"
    with pytest.raises(ValueError) as exc_info:
        Abort.parse(message)

    assert (
        str(exc_info.value) == f"invalid message type {type(message).__name__} for {Abort.TEXT}, type should be a list"
    )


def test_parse_with_invalid_min_length():
    message = ["foo"]
    with pytest.raises(ValueError) as exc_info:
        Abort.parse(message)

    assert str(exc_info.value) == f"invalid message length {len(message)}, must be at least 3"


def test_parse_with_invalid_max_length():
    message = [1, {}, "io.xconn", 4]
    with pytest.raises(ValueError) as exc_info:
        Abort.parse(message)

    assert str(exc_info.value) == f"invalid message length {len(message)}, must be at most 3"


def test_parse_with_invalid_message_type():
    message = [2, {}, "wamp.error.no_such_realm"]
    with pytest.raises(ValueError) as exc_info:
        Abort.parse(message)

    assert str(exc_info.value) == f"invalid message id 2 for {Abort.TEXT}, expected {Abort.TYPE}"


def test_parse_with_invalid_detail_type():
    message = [3, "detail", "wamp.error.no_such_realm"]
    with pytest.raises(exceptions.InvalidDetailsError) as exc_info:
        Abort.parse(message)

    assert str(exc_info.value) == f"details must be of type dictionary for {Abort.TEXT}"


def test_parse_with_invalid_details_dict_key():
    message = [3, {1: "v"}, "wamp.error.no_such_realm"]
    with pytest.raises(exceptions.InvalidDetailsError) as exc_info:
        Abort.parse(message)

    assert str(exc_info.value) == f"invalid type for key '1' in extra details for {Abort.TEXT}"


def test_parse_with_reason_none():
    message = [3, {}, None]
    with pytest.raises(exceptions.InvalidUriError) as exc_info:
        Abort.parse(message)

    assert str(exc_info.value) == f"uri cannot be null for {Abort.TEXT}"


def test_parse_with_invalid_reason_type():
    message = [3, {}, ["wamp.error.no_such_realm"]]
    with pytest.raises(exceptions.InvalidUriError) as exc_info:
        Abort.parse(message)

    assert str(exc_info.value) == f"uri must be of type string for {Abort.TEXT}"


def test_parse_correctly():
    details = {"message": "The realm does not exist."}
    reason = "wamp.error.no_such_realm"
    message = [3, details, reason]
    abort = Abort.parse(message)

    assert isinstance(abort, Abort)

    assert isinstance(abort.details, dict)
    assert abort.details == details

    assert isinstance(abort.reason, str)
    assert abort.reason == reason


def test_marshal_with_empty_details():
    reason = "wamp.error.no_such_realm"
    message = Abort({}, reason).marshal()

    assert isinstance(message, list)

    assert isinstance(message[0], int)
    assert message[0] == Abort.TYPE

    assert message[1] == dict()

    assert isinstance(message[2], str)
    assert message[2] == reason


def test_marshal_with_details():
    details = {"message": "The realm does not exist."}
    reason = "wamp.error.no_such_realm"
    message = Abort(details, reason).marshal()

    assert isinstance(message, list)

    assert isinstance(message[0], int)
    assert message[0] == Abort.TYPE

    assert isinstance(message[1], dict)
    assert message[1] == details

    assert isinstance(message[2], str)
    assert message[2] == reason
