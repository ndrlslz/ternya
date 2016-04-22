from ternya import nova, cinder, neutron, glance


@nova("compute.metrics.update")
def test(body, message):
    print("this is service process.")
    print(body['event_type'])
    print(body)


@cinder("volume.delete.*")
def test1(body, message):
    print("this is cinder process")
    print(body['event_type'])
    print(body)


@neutron("network.create.start")
def test2(body, message):
    print("this is neutron process")
    print(body['event_type'])
    print(body)


@neutron("network.delete.*")
def test3(body, message):
    print("this is neutron process")
    print(body['event_type'])
    print(body)


@glance("image.create")
def test4(body, message):
    print("this is glance process")
    print(body['event_type'])
    print(body)
