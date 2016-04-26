from ternya import neutron


@neutron("network.create.start")
def test2(body, message):
    print("this is neutron process")
    print(body['event_type'])
    print(body)


@neutron("network.delete.*")
def test2(body, message):
    print("this is neutron process")
    print(body['event_type'])
    print(body)
