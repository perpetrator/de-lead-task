import logging
from schema import Schema, And, Use, Optional, SchemaError


def validate_data(data: dict) -> (list, list):
    """
    Function to validate data
    :param data: data to validate
    :return: tuple of two lists (valid_jokes, invalid_jokes)
    """

    try:
        l1 = Schema({'total':int, 'result': list})
        validated = l1.validate(data)
    except SchemaError:
        logging.error("Unexpected data format, probably missing 'result' section")
        raise

    validated_l1 = validated['result']

    valid_jokes = []
    invalid_jokes = []

    for joke in validated_l1:
        sd = {'categories': list,'created_at': str, 'icon_url': str, 'id': str, 'updated_at': str, 'url': str, 'value': str}
        l2 = Schema(sd)
        if l2.is_valid(joke):
           valid_jokes.append(joke)
        else:
            invalid_jokes.append(joke)

    return valid_jokes, invalid_jokes
