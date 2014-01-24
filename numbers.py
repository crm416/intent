import re


class NumberService(object):
    __small__ = {
        'zero': 0,
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
        'ten': 10,
        'eleven': 11,
        'twelve': 12,
        'thirteen': 13,
        'fourteen': 14,
        'fifteen': 15,
        'sixteen': 16,
        'seventeen': 17,
        'eighteen': 18,
        'nineteen': 19,
        'twenty': 20,
        'thirty': 30,
        'forty': 40,
        'fifty': 50,
        'sixty': 60,
        'seventy': 70,
        'eighty': 80,
        'ninety': 90
    }

    __magnitude__ = {
        'thousand':     1000,
        'million':      1000000,
        'billion':      1000000000,
        'trillion':     1000000000000,
        'quadrillion':  1000000000000000,
        'quintillion':  1000000000000000000,
        'sextillion':   1000000000000000000000,
        'septillion':   1000000000000000000000000,
        'octillion':    1000000000000000000000000000,
        'nonillion':    1000000000000000000000000000000,
        'decillion':    1000000000000000000000000000000000,
    }

    __ordinals__ = {
        'first': 'one',
        'second': 'two',
        'third': 'three',
        'fourth': 'four',
        'fifth': 'five',
        'sixth': 'six',
        'seventh': 'seventh',
        'eighth': 'eight',
        'ninth': 'nine',
        'tenth': 'ten',
        'eleventh': 'eleven',
        'twelth': 'twelve',
        'thirteenth': 'thirteen',
        'fifteenth': 'fifteen',
        'sixteenth': 'sixteen',
        'seventeenth': 'seventeen',
        'eighteenth': 'eighteen',
        'nineteenth': 'nineteen',
        'twentieth': 'twenty',
        'thirtieth': 'thirty',
        'fortieth': 'forty',
        'fiftieth': 'fifty',
        'sixtieth': 'sixty',
        'seventieth': 'seventy',
        'eightieth': 'eighty',
        'ninetieth': 'ninety',
        'hundredth': 'hundred'
    }

    __fractions__ = {
        'quarter': 'four',
        'half': 'two',
        'halve': 'two'
    }

    class NumberException(Exception):

        def __init__(self, msg):
            Exception.__init__(self, msg)

    def parse(self, words):
        """
            A general method for parsing word-representations of numbers.
            Supports floats and integers.

            Arguments:
            words -- word representation of a numerical value.

            Returns:
            floating-point representation of the words
        """
        def exact(words):
            """If already represented as float or int, convert."""
            try:
                return int(words)
            except:
                try:
                    return float(words)
                except:
                    return None

        if exact(words):
            return exact(words)

        split = words.split(' ')

        # Replace final ordinal/fraction with number
        if split[-1] in self.__fractions__:
            split[-1] = self.__fractions__[split[-1]]
        elif split[-1] in self.__ordinals__:
            split[-1] = self.__ordinals__[split[-1]]

        parsed_ordinals = ' '.join(split)

        return self.parseFloat(parsed_ordinals)

    def parseFloat(self, words):
        """
            Convert a floating-point number described in words to a double.
            Supports two kinds of descriptions: those with a 'point' (e.g.,
            "one point two five") and those with a fraction (e.g., "one and
            a quarter").

            Arguments:
            words -- description of the floating-point number

            Returns:
            double representation of the words
        """
        def pointFloat(words):
            m = re.search(r'(.*) point (.*)', words)
            if m:
                whole = m.group(1)
                frac = m.group(2)
                total = 0.0
                coeff = 0.10
                for digit in frac.split(' '):
                    total += coeff * self.parse(digit)
                    coeff /= 10.0

                return self.parseInt(whole) + total
            return None

        def fractionFloat(words):
            m = re.search(r'(.*) and (.*)', words)
            if m:
                whole = self.parseInt(m.group(1))
                frac = m.group(2)

                # Replace plurals
                frac = re.sub(r'(\w+)s(\b)', '\g<1>\g<2>', frac)

                # Convert 'a' to 'one' (e.g., 'a third' to 'one third')
                frac = re.sub(r'(\b)a(\b)', '\g<1>one\g<2>', frac)

                split = frac.split(' ')

                # Split fraction into num (regular integer), denom (ordinal)
                num = split[:1]
                denom = split[1:]

                while denom:
                    try:
                        # Test for valid num, denom
                        num_value = self.parse(' '.join(num))
                        denom_value = self.parse(' '.join(denom))
                        return whole + float(num_value) / denom_value
                    except:
                        # Add another word to num
                        num += denom[:1]
                        denom = denom[1:]
            return None

        # Extract "one point two five"-type float
        result = pointFloat(words)
        if result:
            return result

        # Extract "one and a quarter"-type float
        result = fractionFloat(words)
        if result:
            return result

        # Parse as integer
        return self.parseInt(words)

    def parseInt(self, words):
        """
            Parses words to the integer they describe.

            Arguments:
            words -- description of the integer

            Returns:
            integer representation of the words
        """
        # Remove 'and', case-sensitivity
        words = words.replace(" and ", " ").lower()
        # 'a' -> 'one'
        words = re.sub(r'(\b)a(\b)', '\g<1>one\g<2>', words)

        def textToNumber(s):
            """
                Converts raw number string to an integer.
                Based on text2num.py by Greg Hewill.
            """
            a = re.split(r"[\s-]+", s)
            n = 0
            g = 0
            for w in a:
                x = NumberService.__small__.get(w, None)
                if x is not None:
                    g += x
                elif w == "hundred":
                    g *= 100
                else:
                    x = NumberService.__magnitude__.get(w, None)
                    if x is not None:
                        n += g * x
                        g = 0
                    else:
                        raise NumberService.NumberException(
                            "Unknown number: " + w)
            return n + g

        return textToNumber(words)

    def isValid(self, input):
        try:
            self.parse(input)
            return True
        except:
            return False

    def longestNumber(self, input):
        """
            Attempts to extract the longest valid numerical description from a string.
            Not guaranteed to return a result even if some valid numerical description exists
            (i.e., not particularly advanced).
        """
        split = input.split(' ')

        # Assume just a single number
        numStart = None
        numEnd = None
        for i, w in enumerate(split):
            if self.isValid(w):
                if numStart is None:
                    numStart = i
                numEnd = i
            else:
                # Check for ordinal, which would signify end
                w = re.sub(r'(\w+)s(\b)', '\g<1>\g<2>', w)
                if w in self.__ordinals__:
                    if self.isValid(' '.join(split[numStart:i + 1])):
                        numEnd = i
                        break
        description = ' '.join(split[numStart:numEnd + 1])
        return self.parse(description)
