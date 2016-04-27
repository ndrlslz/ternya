from ternya import nova


@nova("compute.metrics.update")
def test(body, message):
    """

    :param body: notification dict
    :param message: kombu Message class
    """
    print("this is service process.")
    print(body['event_type'])
    print(body)


@nova("compute.instance.exists")
def test(body, message):
    print("this is service process.")
    print(body['event_type'])
    print(body)
