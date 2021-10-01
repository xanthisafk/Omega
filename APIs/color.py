import random

async def get_color() -> int:
    """
    Generates a random hexadecimal color.
    Returns:
        color: int - a hexadecimal number.
    """ 

    # Generate a random color
    color = "%06x" % random.randint(0, 0xFFFFFF)

    # Convert to int for it to work
    color = int(color, 16)

    return color
