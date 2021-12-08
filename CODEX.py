import argparse
import math
import random

from reportlab.lib.colors import black, white, Color, yellow
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


def ROMAN_NUMBERS_GENERATOR(R, only_length=4):
    for X in R:
        result = int_to_roman(X)
        if len(result) == only_length:
            yield result


def DRAW_PAGE_BACKGROUND(c, w, h, corners_font_size, roman_number, background_color, stroke_colors,
                         corner_decoration_alpha):
    def GET_CORNER_DECORATION_COLOR():
        return Color(random.uniform(0.8, 1),
                     random.uniform(0.8, 1),
                     random.uniform(0.8, 1),
                     corner_decoration_alpha)

    c.saveState()
    c.setFillColor(background_color)
    c.rect(0, 0, w * cm, h * cm, fill=1)
    c.setStrokeColor(stroke_colors[0])

    c.line(0, 0, w * cm, h * cm)
    c.line(w * cm, 0, 0, h * cm)

    K = corners_font_size * 23.8

    for x in range(0, int(w * cm), 2):
        c.setLineWidth(w * cm / K / math.sqrt(abs(w * cm / 2 - x)))

        c.setStrokeColor(stroke_colors[1])
        c.line(x, 0, x, h * cm)

    for y in range(0, int(h * cm), 2):
        c.setLineWidth(h * cm / K * (w / h) / math.sqrt(abs(h * cm / 2 - y)))
        c.line(0, y, w * cm, y)

    c.restoreState()

    MARGIN_WIDTH = 0.1 * cm
    MARGIN_HEIGHT = 0.03 * cm

    c.setFont(FONT_NAME, corners_font_size)

    c.saveState()
    c.translate(MARGIN_WIDTH, MARGIN_HEIGHT)
    angle = -math.atan(w / h / 2)
    c.rotate(math.degrees(angle))

    c.setFillColor(GET_CORNER_DECORATION_COLOR())
    c.drawCentredString(0, 0, f"{roman_number[0]}")
    c.restoreState()

    c.saveState()
    c.translate(w * cm - MARGIN_WIDTH, MARGIN_HEIGHT)
    c.rotate(-math.degrees(angle))

    c.setFillColor(GET_CORNER_DECORATION_COLOR())
    c.drawCentredString(0, 0, f"{roman_number[1]}")
    c.restoreState()

    c.saveState()
    c.translate(w * cm - MARGIN_WIDTH, h * cm - MARGIN_HEIGHT)
    c.rotate(math.degrees(angle) + 180)

    c.setFillColor(GET_CORNER_DECORATION_COLOR())
    c.drawCentredString(0, 0, f"{roman_number[2]}")
    c.restoreState()

    c.saveState()
    c.translate(MARGIN_WIDTH, h * cm - MARGIN_HEIGHT)
    c.rotate(180 - math.degrees(angle))

    c.setFillColor(GET_CORNER_DECORATION_COLOR())
    c.drawCentredString(0, 0, f"{roman_number[3]}")
    c.restoreState()


def MAIN():
    parser = argparse.ArgumentParser(description='THIS PROGRAM PRINTS OUT ITSELF AS A BOOK')
    parser.add_argument('--width', action="store", dest="width", type=float, default=21.0)
    parser.add_argument('--height', action="store", dest="height", type=float, default=29.7)
    parser.add_argument('--font_size_min', action="store", dest="font_size_min", type=int, default=30)
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

    ROMAN_NUMBERS = list(iter(ROMAN_NUMBERS_GENERATOR(range(1, 4000))))

    PAGE = 1
    for FONT_SIZE in reversed(FONT_SIZES[:len(ROMAN_NUMBERS)]):

        try:

            ROMAN_NUMBER = ROMAN_NUMBERS[int(PAGE/2)]

            DRAW_PAGE_BACKGROUND(c, WIDTH, HEIGHT, FONT_SIZE, ROMAN_NUMBER,
                                 background_color=white,
                                 stroke_colors=[Color(1, 0.3, 0.4, 0.1), Color(1, 0.3, 0.4, 0.4)],
                                 corner_decoration_alpha=0.666)

            c.showPage()
            DRAW_PAGE_BACKGROUND(c, WIDTH, HEIGHT, FONT_SIZE, ROMAN_NUMBER,
                                 background_color=black,
                                 stroke_colors=[Color(1, 1, 1, 0.01), Color(0.6, 0.6, 0.6, 0.07)],
                                 corner_decoration_alpha=0.018)

            c.showPage()

            PAGE += 1
            print(f"  -  {ROMAN_NUMBER}")
        except StopIteration:
            break  # WE RUN OUT OF ROMAN NUMBERS
    c.save()

    # Use a breakpoint in the code line below to debug your script.
    print(f'SAVING : {OUTPUT_FILE_NAME}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    MAIN()
