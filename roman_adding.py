#! /usr/bin/env python3

"""Support for adding two roman numbers.

The idea is to write a function, add, that takes two strings as arguments,
each of which is a roman number. The function returns the sum of the two
arguments, also as a string representing a roman number. Ideally, this is
done only using string operations, without any use of "normal" numbers.

The rules for representing roman numbers are (stealing liberally from
https://en.wikipedia.org/wiki/Roman_numerals):

* The numerals are: I (1), V (5), X (10), L (50), C (100), D (500), M (1000)
* Numbers above 3000 are not supported (so you don't need to worry about
  inputs *or outputs* above that amount) - although it's OK if they do work.
* Generally, numbers are formed by adding adjacent values - so

  * CCVII is 100 + 100 + 5 + 1 + 1 which is 207, and
  * MLXVI is 1000 + 50 + 10 + 1, which is 1066,

* In special cases, four repeating characters are instead always replaced by 
  "subtractive notation", e.g., IV means 4, instead of IIII.

  * So we have IV (4), IX (9), XL (40), XC (90), CD (400), CM (900)
  * The rule is that a numeral may be placed before either of the next two
    larger digits. This means you are not allowed represent 49 as IL (1 less
    than 50), but must instead do XLIX (40 + 9).
  * Other examples are MCMIV (1000 + 900 + 4) for 1904,
    MCMLIV (1000 + 900 + 50 + 4) for 1954 and
    MCMXC (1000 + 900 + 90) for 1990

Output should always be in these tidy forms.

I believe it is possible to do addition of these forms entirely with string
operations.

If you want to be extra clever, after you've got that working, you can try
to also allow a more "relaxed" form of input, where the restriction on always
turning four repeated sybmols into the substractive form is relaxed - so for
instance, allowing IIII as well as IV, and even XXXXXX instead of LX.
(Although it's possible that it might just work...)
"""

import sys
from collections import OrderedDict

ROMAN_DIGITS = 'IVXLCDM'

# Maps subtractive representation of numerals to longer additive notation
# Ordered to enable swapping largest numbers first
ADDITIVE_MAP = OrderedDict()
ADDITIVE_MAP['CM']='DCCCC'
ADDITIVE_MAP['CD']='CCCC'
ADDITIVE_MAP['XC']='LXXXX'
ADDITIVE_MAP['XL']='XXXX'
ADDITIVE_MAP['IX']='VIIII'
ADDITIVE_MAP['IV']='IIII'

# Maps additive representations of numerals to shorthand subtractive notation
REDUCTION_MAP = {}
REDUCTION_MAP['IIIII']='V'
REDUCTION_MAP['VIV']='IX'
REDUCTION_MAP['VV']='X'
REDUCTION_MAP['XXXXX']='L'
REDUCTION_MAP['LXL']='XC'
REDUCTION_MAP['LL']='C'
REDUCTION_MAP['CCCCC']='D'
REDUCTION_MAP['DCD']='CM'
REDUCTION_MAP['DD']='M'


def check_roman(s):
    """If 's' is not a roman number, raise a Value Error.
    """
    if not all(x in ROMAN_DIGITS for x in s):
        raise ValueError('{!r} is not a sequence of I, V, X, L, C, D or M'.format(s))

def replace_subtractive(number):
    """Replace subtractive form with additive form equivalent: 'IX' -> 'VIIII'."""
    for sub,add in ADDITIVE_MAP.items():
        if sub in number:
            number = number.replace(sub,add)
    return number

def replace_additive(number):
    """Replace series of roman digits with subtractive form: 'IIII' -> 'IV'."""
    for key, value in ADDITIVE_MAP.items():
        if value in number:
            number = number.replace(value, key)
    return number

def fold_digits(number):
    """Fold series of roman digits into a single digit: IIIII -> V
       
       fold_digits will apply this reduction as many times as possible.
       
       >>> fold_digits('VIIIII')
       >>> 'X'
    """
    while True:
        number_before_fold = number
        for digits, reduction in REDUCTION_MAP.items():
            if digits in number:
                number = number.replace(digits, reduction)
        if number_before_fold == number:
            return number

def add(*numbers):
    """Add strings representing roman numbers.
    
      >>> add('IV', 'V')
      'IX'
      >>> add('XVII', 'X', 'XIII')
      'XL'

    Raises:
        ValueError: if numbers contain characters other then IVXLCDM.
    """
    for n in numbers:
        check_roman(n)       

    additive_form = (replace_subtractive(n) for n in numbers)
    additive_sum = ''.join(additive_form)
    
    # Sum must be sorted to enable further reduction ie. swaping 'IIIII' for 'V'
    sorted_sum_gen = sorted(additive_sum, 
                            key=lambda x: ROMAN_DIGITS.index(x),
                            reverse=True)
    sorted_sum = ''.join(sorted_sum_gen)
    
    reduced_sum = fold_digits(sorted_sum)
    
    # change additive representation to shortened form ie. swap 'IIII' for 'IV'    
    return replace_additive(reduced_sum)


def main(args):
    """Allow adding roman numbers from the command line."""
    if len(args) <= 1:
        print('Usage: roman_adding.py <roman-number-1> [...] <roman-number-n>')
    else:
        print(add(*args))

if __name__ == '__main__':
    main(sys.argv[1:])
