from ternya import cinder


@cinder("volume.create.start")
def test1(body, message):
    print("this is cinder process")
    print(body['event_type'])
    print(body)


@cinder("volume.delete.*")
def test1(body, message):
    print("this is cinder process")
    print(body['event_type'])
    print(body)
