# -*- coding: utf-8 -*-

import unittest

from xml.etree.ElementTree import tostring

from asciimathml import *

class ParseTestCase(unittest.TestCase):
    def assertTreeEquals(self, a, b):
        self.assertEquals(tostring(a), tostring(remove_private(b)))

    def assertRendersTo(self, asciimathml, xmlstring):
        mathml = parse(asciimathml)
        self.assertEquals(tostring(mathml), '<math><mstyle>%s</mstyle></math>' % xmlstring)

    def testEmpty(self):
        self.assertTreeEquals(parse(''), El('math', El('mstyle')))

    def testNumber(self):
        self.assertTreeEquals(parse('3.1415'), El('math', El('mstyle', El('mn', text='3.1415'))))

    def testSymbol(self):
        self.assertTreeEquals(parse('alpha'), El('math', El('mstyle', El('mi', text=u'\u03b1'))))

    def testSymbols(self):
        self.assertTreeEquals(parse('alpha beta'), El('math', El('mstyle', El('mi', text=u'\u03b1'), El('mi', text=u'\u03b2'))))

    def testFrac(self):
        self.assertTreeEquals(parse('alpha / beta'),
            El('math', El('mstyle',
                El('mfrac',
                    El('mi', text=u'\u03b1'),
                    El('mi', text=u'\u03b2')))))

    def testSub(self):
        self.assertTreeEquals(parse('alpha _ beta'),
            El('math', El('mstyle',
                El('msub',
                    El('mi', text=u'\u03b1'),
                    El('mi', text=u'\u03b2')))))

    def testSup(self):
        self.assertTreeEquals(parse('alpha ^ beta'),
            El('math', El('mstyle',
                El('msup',
                    El('mi', text=u'\u03b1'),
                    El('mi', text=u'\u03b2')))))

    def testSubSup(self):
        self.assertTreeEquals(parse('alpha _ beta ^ gamma'),
            El('math', El('mstyle',
                El('msubsup',
                    El('mi', text=u'\u03b1'),
                    El('mi', text=u'\u03b2'),
                    El('mi', text=u'\u03b3')))))

    def testSupSub(self):
        self.assertTreeEquals(parse('alpha ^ beta _ gamma'),
            El('math', El('mstyle',
                El('msubsup',
                    El('mi', text=u'\u03b1'),
                    El('mi', text=u'\u03b3'),
                    El('mi', text=u'\u03b2')))))

    def testUnary(self):
        self.assertTreeEquals(parse('sin alpha'),
            El('math', El('mstyle',
                El('mrow',
                    El('mo', text='sin'),
                    El('mi', text=u'\u03b1')))))

    def testUnary2(self):
        self.assertTreeEquals(parse('dot alpha'),
            El('math', El('mstyle',
                El('mover',
                    El('mi', text=u'\u03b1'),
                    El('mo', text='.')))))

    def testUnary3(self):
        self.assertTreeEquals(parse('sqrt alpha'),
            El('math', El('mstyle',
                El('msqrt',
                    El('mi', text=u'\u03b1')))))

    def testUnary4(self):
        self.assertTreeEquals(parse('text alpha'),
            El('math', El('mstyle',
                El('mtext',
                    El('mi', text=u'\u03b1')))))

    def testBinary(self):
        self.assertTreeEquals(parse('frac alpha beta'),
            El('math', El('mstyle',
                El('mfrac',
                    El('mi', text=u'\u03b1'),
                    El('mi', text=u'\u03b2')))))

    def testTripleFrac(self):
        self.assertRendersTo('a/b/c/d',
            '<mfrac><mi>a</mi><mi>b</mi></mfrac><mo>/</mo><mfrac><mi>c</mi><mi>d</mi></mfrac>')

    def testUnderOver(self):
        self.assertTreeEquals(parse('sum_alpha^beta'),
            El('math', El('mstyle',
                El('munderover',
                    El('mo', text=u'\u2211'),
                    El('mi', text=u'\u03b1'),
                    El('mi', text=u'\u03b2')))))

    def testParens(self):
        self.assertTreeEquals(parse('(alpha + beta) / gamma'),
            El('math', El('mstyle',
                El('mfrac',
                    El('mrow',
                        El('mi', text=u'\u03b1'),
                        El('mo', text='+'),
                        El('mi', text=u'\u03b2')),
                    El('mi', text=u'\u03b3')))))

    def testUnbalancedParens(self):
        self.assertRendersTo('(alpha + beta / gamma',
            '<mrow><mo>(</mo><mi>&#945;</mi><mo>+</mo><mfrac><mi>&#946;</mi><mi>&#947;</mi></mfrac></mrow>')

    def testNestedParens(self):
        self.assertRendersTo('(alpha + [ beta + { gamma } ] )',
            '<mrow><mo>(</mo><mi>&#945;</mi><mo>+</mo><mrow><mo>[</mo><mi>&#946;</mi><mo>+</mo><mrow><mo>{</mo><mi>&#947;</mi><mo>}</mo></mrow><mo>]</mo></mrow><mo>)</mo></mrow>')

    def testNesting(self):
        self.assertRendersTo('sqrt sqrt root3x',
            '<msqrt><msqrt><mroot><mi>x</mi><mn>3</mn></mroot></msqrt></msqrt>')

    def testBar(self):
        self.assertRendersTo('(a,b]={x in RR | a < x <= b}',
            '<mrow><mo>(</mo><mi>a</mi><mo>,</mo><mi>b</mi><mo>]</mo></mrow><mo>=</mo><mrow><mo>{</mo><mi>x</mi><mo>&#8712;</mo><mo>&#8477;</mo><mrow><mo>|</mo></mrow><mi>a</mi><mo>&lt;</mo><mi>x</mi><mo>&#8804;</mo><mi>b</mi><mo>}</mo></mrow>')

    def testNegative(self):
        self.assertRendersTo('abc-123.45^-1.1',
            '<mi>a</mi><mi>b</mi><mi>c</mi><mo>-</mo><msup><mn>123.45</mn><mrow><mo>-</mo><mn>1.1</mn></mrow></msup>')

    def testHat(self):
        self.assertRendersTo('hat(ab) bar(xy) ulA vec v dotx ddot y',
            '<mover><mrow><mi>a</mi><mi>b</mi></mrow><mo>^</mo></mover><mover><mrow><mi>x</mi><mi>y</mi></mrow><mo>&#175;</mo></mover><munder><mi>A</mi><mo>&#818;</mo></munder><mover><mi>v</mi><mo>&#8594;</mo></mover><mover><mi>x</mi><mo>.</mo></mover><mover><mi>y</mi><mo>..</mo></mover>')

    def testMatrix(self):
        self.assertRendersTo('[[a,b],[c,d]]((n),(k))',
            '<mrow><mo>[</mo><mtable><mtr><mtd><mi>a</mi></mtd><mtd><mi>b</mi></mtd></mtr><mtr><mtd><mi>c</mi></mtd><mtd><mi>d</mi></mtd></mtr></mtable><mo>]</mo></mrow><mrow><mo>(</mo><mtable><mtr><mtd><mi>n</mi></mtd></mtr><mtr><mtd><mi>k</mi></mtd></mtr></mtable><mo>)</mo></mrow>')

    def testMatrix2(self):
        self.assertRendersTo('x/x={(1,if x!=0),(text{undefined},if x=0):}',
            '<mfrac><mi>x</mi><mi>x</mi></mfrac><mo>=</mo><mrow><mo>{</mo><mtable columnalign="left"><mtr><mtd><mn>1</mn></mtd><mtd><mrow><mspace width="1ex"/><mo>if</mo><mspace width="1ex"/></mrow><mi>x</mi><mo>≠</mo><mn>0</mn></mtd></mtr><mtr><mtd><mrow><mtext>undefined</mtext></mrow></mtd><mtd><mrow><mspace width="1ex"/><mo>if</mo><mspace width="1ex"/></mrow><mi>x</mi><mo>=</mo><mn>0</mn></mtd></mtr></mtable></mrow>')

if __name__ == '__main__':
    unittest.main()

