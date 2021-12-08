import argparse
import math
import random

from reportlab.lib.colors import black, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch, cm
from reportlab.pdfbase.ttfonts import TTFont

FONT_NAME = "AnglicanText"
pdfmetrics.registerFont(TTFont(FONT_NAME, 'AnglicanText.ttf'))


def int_to_roman(input):
    """ Convert an integer to a Roman numeral. """

    if not isinstance(input, type(1)):
        raise TypeError("expected integer, got %s" % type(input))
    if not 0 < input < 4000:
        raise ValueError("Argument must be between 1 and 4000")
    ints = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
    nums = ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
    result = []
    for i in range(len(ints)):
        count = int(input / ints[i])
        result.append(nums[i] * count)
        input -= ints[i] * count
    return ''.join(result)


def primes(n):
    """ Returns  a list of primes < n """
    sieve = [True] * n
    for i in range(3, int(n ** 0.5) + 1, 2):
        if sieve[i]:
            sieve[i * i::2 * i] = [False] * ((n - i * i - 1) // (2 * i) + 1)
    return [2] + [i for i in range(3, n, 2) if sieve[i]]


def ROMAN_NUMBERS(R, only_length=4):
    for X in R:
        ROMAN_NUMBER = int_to_roman(X)
        if len(ROMAN_NUMBER) == only_length:
            yield ROMAN_NUMBER


def MAIN():
    parser = argparse.ArgumentParser(description='THIS PROGRAM PRINTS OUT ITSELF AS A BOOK')
    parser.add_argument('--width', action="store", dest="width", type=float, default=21.0)
    parser.add_argument('--height', action="store", dest="height", type=float, default=29.7)
    parser.add_argument('--font_size_min', action="store", dest="font_size_min", type=int, default=20)
    parser.add_argument('--font_size_max', action="store", dest="font_size_max", type=int, default=6660)
    parser.add_argument('--prime_font_sizes_only', dest='prime_font_sizes_only', action='store_true', default=True)
    ARGS = parser.parse_args()
    OUTPUT_FILE_NAME = "BOOK.pdf"
    (WIDTH, HEIGHT) = (ARGS.width, ARGS.height)
    (FONT_SIZE_MIN, FONT_SIZE_MAX) = (ARGS.font_size_min, ARGS.font_size_max)

    PRIME_FONT_SIZES_ONLY = ARGS.prime_font_sizes_only
    # CREATES (PDF)[https://ru.wikipedia.org/wiki/Portable_Document_Format] FILE
    c = Canvas(OUTPUT_FILE_NAME, pagesize=(WIDTH * cm, HEIGHT * cm))

    FONT_SIZES = range(FONT_SIZE_MIN, FONT_SIZE_MAX)
    if PRIME_FONT_SIZES_ONLY:
        ALL_PRIMES = primes(FONT_SIZE_MAX)
        FONT_SIZES = ALL_PRIMES
        while FONT_SIZES[0] < FONT_SIZE_MIN:
            FONT_SIZES = FONT_SIZES[1:]

    print(f"FONT SIZES: {FONT_SIZES}")

    ROMAN_NUMBERS_GENERATOR = iter(ROMAN_NUMBERS(range(1, 4000)))

    for FONT_SIZE in FONT_SIZES:
        c.setFillColor(black)
        c.rect(0, 0, WIDTH * cm, HEIGHT * cm)  # breaks preview in chrome
        c.setFillColor(white)

        c.setStrokeColorRGB(1, 0.3, 0.4, 0.1)

        c.line(0, 0, WIDTH * cm, HEIGHT * cm)
        c.line(WIDTH * cm, 0, 0, HEIGHT * cm)

        K =FONT_SIZE * 23.8

        for x in range(0, int(WIDTH * cm), 2):
            c.setLineWidth(WIDTH * cm/K/ math.sqrt(abs(WIDTH * cm / 2 - x)))

            c.setStrokeColorRGB(1, 0.3, 0.4, 0.4)
            c.line(x, 0, x, HEIGHT * cm)

        for y in range(0, int(HEIGHT * cm), 2):
            c.setLineWidth(HEIGHT * cm/K*(WIDTH/HEIGHT)/ math.sqrt(abs(HEIGHT * cm / 2 - y)))
            c.line(0, y, WIDTH *cm, y)


        c.setFont(FONT_NAME, FONT_SIZE)
        MARGIN_WIDTH = 0.1 * cm
        MARGIN_HEIGHT = 0.03 * cm
        try:
            ROMAN_NUMBER = next(ROMAN_NUMBERS_GENERATOR)
            ROMAN_NUMBER = ''.join(random.sample(ROMAN_NUMBER, len(ROMAN_NUMBER)))
            c.saveState()
            c.translate(MARGIN_WIDTH, MARGIN_HEIGHT)
            angle = -math.atan(WIDTH / HEIGHT / 2)
            c.rotate(math.degrees(angle))
            c.drawCentredString(0, 0, f"{ROMAN_NUMBER[0]}")
            c.restoreState()

            c.saveState()
            c.translate(WIDTH * cm - MARGIN_WIDTH, MARGIN_HEIGHT)
            c.rotate(-math.degrees(angle))
            c.drawCentredString(0, 0, f"{ROMAN_NUMBER[1]}")
            c.restoreState()

            c.saveState()
            c.translate(WIDTH * cm - MARGIN_WIDTH, HEIGHT * cm - MARGIN_HEIGHT)
            c.rotate(math.degrees(angle) + 180)
            c.drawCentredString(0, 0, f"{ROMAN_NUMBER[2]}")
            c.restoreState()

            c.saveState()
            c.translate(MARGIN_WIDTH, HEIGHT * cm - MARGIN_HEIGHT)
            c.rotate(180 - math.degrees(angle))
            c.drawCentredString(0, 0, f"{ROMAN_NUMBER[3]}")
            c.restoreState()

            c.showPage()
            print(f"  -  {ROMAN_NUMBER}")
        except StopIteration:
            break  # WE RUN OUT OF ROMAN NUMBERS
    c.save()

    # Use a breakpoint in the code line below to debug your script.
    print(f'SAVING : {OUTPUT_FILE_NAME}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    MAIN()
