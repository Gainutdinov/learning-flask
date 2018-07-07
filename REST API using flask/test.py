def validMovieObject(movieObject):
    if ("name" in movieObject and "price" in movieObject and "identity" in movieObject):
        return True
    else:
        return False

valid_object = {
    'name': 'F',
    'price': 6.99,
    'identity': 1234567890
}

missing_name = {
    'price': 6.99,
    'identity': 1234567890
}


missing_name = {
    'name': 'F',
    'identity': 1234567890
}

missing_identity = {
    'name': 'F',
    'identity': 1234567890
}

empty_dictionary = {}
