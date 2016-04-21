from ternya.annotation import nova, cinder


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
