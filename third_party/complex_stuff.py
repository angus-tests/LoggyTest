import logging

logger = logging.getLogger('complex_stuff')


def complex_add(num1: int, num2: int) -> int:
    """
    Adds two numbers together.

    :param num1: The first number.
    :param num2: The second number.
    :return: The sum of the two numbers.
    """
    logger.debug("Adding some numbers from inside the third party library")
    return num1 + num2
