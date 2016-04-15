from ternya.annotation import nova


@nova("123")
def test(body, message):
    print("1")
