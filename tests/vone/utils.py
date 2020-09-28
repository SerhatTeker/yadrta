from uuid import UUID


def user_id_to_hex(uuid: str) -> str:
    """Turn uuid4 with dashes to hex:
    From    :  8791f25b-d4ca-4f10-8f60-407a507edefe
    To      :  8791f25bd4ca4f108f60407a507edefe

    :param uuid: uuid string with dashes
    :type uuid: str

    :returns: str - hex of uuid
    """

    return UUID(uuid).hex
