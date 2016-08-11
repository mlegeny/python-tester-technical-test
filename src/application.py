# Marton Legeny, 11/08/2016, 17:08

# Python 2,3 support
from __future__ import print_function
from six.moves import input

import os
import sys
import re
import requests
from bs4 import BeautifulSoup
import unittest

def get(a):
    # Performs a http request, returning a string
    response = requests.get(a)
    return response.text

def element_count(a, b):
    # element count
    output = get(a)

    soup = BeautifulSoup(output)

    return len(soup.find_all(b))

def fizz_or_buzz(number):
    # Return fizz or buzz or fizzbuzz
    # number/3 then fizz
    # number/5 then buzz
    # number/(3,5) then fizz buzz
    # number !/ (3,5) then <empty>
    is_three = True if number % 3 == 0 else False
    is_five = True if number % 5 == 0 else False

    # Specify a return value
    returnText = ''

    # If the number can be divided by three, add 'fizz'
    if is_three:
        returnText += 'fizz'
    # If the number can be divided by five, add 'buzz'
    if is_five:
        returnText += 'buzz'
    # Return text
    return returnText

def app_output(*args):
    with open('output.txt', 'a') as fd:
        fd.write('{} = {} = {} = {}\n'.format(*args))
    print('{} = {} = {} = {}\n'.format(*args))

def app(a,b):
    count = element_count(a,b)
    FizzBuzz = fizz_or_buzz(count)
    app_output(a,b,count,FizzBuzz)

'''
Unit tests for fizz_or_buzz
'''
class ut_fizzBuzz(unittest.TestCase):
    # Integer that can be divided by 3 but not by 5
    def test_fizz_3(self):
        output = fizz_or_buzz(3)
        self.assertEqual(output, 'fizz')

    # Integer that can be divided by 5 but not by 3
    def test_fizz_5(self):
        output = fizz_or_buzz(5)
        self.assertEqual(output, 'buzz')

    # Integer that can be divided by both 3 and 5
    def test_fizz_15(self):
        output = fizz_or_buzz(15)
        self.assertEqual(output, 'fizzbuzz')

    # 0 can be divided by all integers
    def test_fizz_0(self):
        output = fizz_or_buzz(0)
        self.assertEqual(output, 'fizzbuzz')

    # Integer that can't be divided by either
    # 3 or 5
    # -> should return nothing
    def test_fizz_2(self):
        output = fizz_or_buzz(2)
        self.assertEqual(output, '')

import sys
if __name__ == '__main__':
        # application will take two args url, html tag type (a, ul, div, ...etc)
        if len(sys.argv) < 3:
            url = input('Url: ')
            tag = input('Tag: ')
        else:
            url = sys.argv[1]
            tag = sys.argv[2]

        app(url, tag)

'''
Code Review

- os and re are not used at all and can be removed (however, they would be useful for unit testing)
- sys is imported twice (the second one is on line #54)
- No comment header for the functions (input parameters, output, what does the function do
- Input arguments could be parsed (argparse) instead of using positional arguments
- KeyboardInterrupt (Ctrl-C / SIGINT) is not handled

-> get(a)
   - parameter 'a' do not have a descriptive name
   - no input sanity check, backtrace will be printed if the URL is not valid
   - no exception handling
   - 'response' might be None and calling .text will not be possible
-> element_count(a)
   - parameters 'a' & 'b' do not have a descriptive name
   - useless comment '# element count'
   - the value of 'output' is not checked
   - no default parser passed to BeautifulSoup - it prints a warning on Windows 7 64 bit / Python 3
   - the value of 'soup' is not checked, it might be None
-> fizz_or_buzz(number)
   - comment states that "fizz buzz" should be returned if 'number' can be divided by both 3 and 5,
     but "fizzbuzz" is returned by the code
   - the logical construct is wrong: the code will return immediately if 'number' can be divided by 3 or by 5,
     making 'return 'fizzbuzz'' dead code
-> app_output(*args)
   - no exception handling (what if the file is write-protected
   - output is always appended to the existing file, I'm not sure if this is desired by the application
   - this could be assigned to a variable to avoid code duplication: '{} = {} = {} = {}\n'.format(*args)
-> app(a,b)
   - parameters 'a' & 'b' do not have a descriptive name
   - no input sanity checks
   - 'FizzBuzz' does not match with the existing naming convention
'''
