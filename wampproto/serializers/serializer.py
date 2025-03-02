from wampproto import messages


class Serializer:
    def serialize(self, message: messages.Message) -> bytes:
        raise NotImplementedError()

    def deserialize(self, data: bytes | str) -> messages.Message:
        raise NotImplementedError()


def to_message(message: list) -> messages.Message:
    if not isinstance(message, list):
        raise TypeError(f"invalid type '{type(message)}', expected a list")

    message_type = message[0]
    if not isinstance(message_type, int):
        raise TypeError(f"invalid message type '{type(message[0])}', expected an integer")

    match message_type:
        case messages.Hello.TYPE:
            return messages.Hello.parse(message)
        case messages.Welcome.TYPE:
            return messages.Welcome.parse(message)
        case messages.Abort.TYPE:
            return messages.Abort.parse(message)
        case messages.Challenge.TYPE:
            return messages.Challenge.parse(message)
        case messages.Authenticate.TYPE:
            return messages.Authenticate.parse(message)
        case messages.Goodbye.TYPE:
            return messages.Goodbye.parse(message)
        case messages.Call.TYPE:
            return messages.Call.parse(message)
        case messages.Invocation.TYPE:
            return messages.Invocation.parse(message)
        case messages.Yield.TYPE:
            return messages.Yield.parse(message)
        case messages.Result.TYPE:
            return messages.Result.parse(message)
        case messages.Register.TYPE:
            return messages.Register.parse(message)
        case messages.Registered.TYPE:
            return messages.Registered.parse(message)
        case messages.UnRegister.TYPE:
            return messages.UnRegister.parse(message)
        case messages.UnRegistered.TYPE:
            return messages.UnRegistered.parse(message)
        case messages.Subscribe.TYPE:
            return messages.Subscribe.parse(message)
        case messages.Subscribed.TYPE:
            return messages.Subscribed.parse(message)
        case messages.UnSubscribe.TYPE:
            return messages.UnSubscribe.parse(message)
        case messages.UnSubscribed.TYPE:
            return messages.UnSubscribed.parse(message)
        case messages.Publish.TYPE:
            return messages.Publish.parse(message)
        case messages.Published.TYPE:
            return messages.Published.parse(message)
        case messages.Event.TYPE:
            return messages.Event.parse(message)
        case messages.Error.TYPE:
            return messages.Error.parse(message)
        case _:
            raise ValueError("unknown message type")
