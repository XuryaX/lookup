'''
Created on May 9, 2016

@author: Shauryadeep Chaudhuri
'''

import parsley

from Field import Field
from FieldSet import FieldSet


class QueryParser(object):

    def __init__(self, getter):
        self.__defineParser()
        self.getter = getter

    def __defineParser(self):
        self.parseField = parsley.makeGrammar("""
        neq = <letterOrDigit*>:field ws '!=' ws <letterOrDigit*>:value ->Field(field,value,'!=')
        eq = <letterOrDigit*>:field  ws '==' ws <letterOrDigit*>:value ->Field(field,value,'==')

        lte = <letterOrDigit*>:field ws '<=' ws <digit*'.'?digit*>:value ->Field(field,value,'<=')
        gte = <letterOrDigit*>:field ws '>=' ws <digit*'.'?digit*>:value ->Field(field,value,'>=')

        lt = <letterOrDigit*>:field ws '<' ws <digit*'.'?digit*>:value ->Field(field,value,'<')
        gt = <letterOrDigit*>:field ws '>' ws <digit*'.'?digit*>:value ->Field(field,value,'>')


        has = <letterOrDigit*>:field ws 'has' ws <(letterOrDigit|',')*>:value ->Field(field,value,'has')

        in = <letterOrDigit*>:field ws 'in' ws <(letterOrDigit|',')*>:value ->Field(field,value,'in')

        hasnot = <letterOrDigit*>:field ws 'not has' ws <(letterOrDigit|',')*>:value ->Field(field,value,'hasnot')

        notin = <letterOrDigit*>:field ws 'not in' ws <(letterOrDigit|',')*>:value ->Field(field,value,'notin')

        fieldCondition = ws (neq | eq | lte | lt | gte |gt | has | in | hasnot | notin):evalTuple ws -> evalTuple

        """, {'Field': Field})

        self.parse = parsley.makeGrammar("""

        neq = <letterOrDigit* ws '!=' ws letterOrDigit*>:s ->str(s)
        eq = <letterOrDigit* ws '==' ws letterOrDigit*>:s ->str(s)

        lte = <letterOrDigit* ws '<=' ws digit*'.'?digit*>:s->str(s)
        gte = <letterOrDigit* ws '>=' ws digit*'.'?digit*>:s ->str(s)

        lt = <letterOrDigit* ws '<' ws digit*'.'?digit*>:s->str(s)
        gt = <letterOrDigit* ws '>' ws digit*'.'?digit*>:s ->str(s)

        has = <letterOrDigit* ws 'has' ws (letterOrDigit|',')*  >:s ->str(s)

        in = <letterOrDigit* ws 'in' ws (letterOrDigit|',')*  >:s ->str(s)

        hasnot = <letterOrDigit* ws 'not has' ws (letterOrDigit|',')*  >:s ->str(s)

        notin = <letterOrDigit* ws 'not in' ws (letterOrDigit|',')*  >:s ->str(s)

        parens = ws '(' ws expr:e ws ')' ws -> e
        value = parens | neq | eq | lte | lt | gte |gt | has | in | hasnot | notin
        ws = ' '*

        and = 'AND' ws expr3:n -> ('AND', n)
        or = 'OR' ws expr3:n -> ('OR', n)

        not = 'NOT' ws value:n -> ('NOT', n)

        checknot = ws (value|not)

        andor = ws (and | or)

        expr = expr3:left andor*:right -> performOperations(left, right)
        expr3 = ws checknot:right -> getVal(right)

        """, {"performOperations": self.performOperations, 'getVal': self.getVal})

    def processQuery(self, field):
        if isinstance(field, FieldSet):
            return field
        elif isinstance(field, Field):
            elements = FieldSet(field, self.getter)
            return elements
        else:
            raise Exception("Invalid Input")

    def performOperations(self, start, pairs):

        result = start

        if isinstance(result, Field):
            result = self.processQuery(start)

        for op, value in pairs:
            if op == 'AND':
                secondField = self.processQuery(value)
                result.intersection(secondField)
            elif op == 'OR':
                secondField = self.processQuery(value)
                result.union(secondField)
        return result

    '''This functions will be returning sets'''

    def getVal(self, field):

        if isinstance(field, tuple):
            _op, value = field
            result = self.parseField(value).fieldCondition()
            result.negate()
        elif isinstance(field, FieldSet):
            result = field
        else:
            result = self.parseField(field).fieldCondition()
        return result

    def getResults(self, query):
        return self.parse(query).expr().getSet()
if __name__ == "__main__":
    pae = QueryParser("POP")
    print "ee"
    print pae.getResults("(field not has x)")
