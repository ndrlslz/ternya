from ternya.annotation import nova


@nova("compute.metrics.update")
def test(body, message):
    print("this is service process.")
    print(body['event_type'])
    print(body)