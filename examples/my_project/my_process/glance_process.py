from ternya import glance


@glance("image.create")
def test4(body, message):
    print("this is glance process")
    print(body['event_type'])
    print(body)


@glance("image.delete")
def test4(body, message):
    print("this is glance process")
    print(body['event_type'])
    print(body)
