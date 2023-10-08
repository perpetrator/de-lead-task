import logging

def validate_data(data:dict) -> dict:
    """
    Function to validate data
    :param data: data to validate
    :return: validated data
    """
    try:
        print(data)
    except Exception as e:
        logging.ERROR("Error while validating data: {}".format(e))
        raise e
    return data