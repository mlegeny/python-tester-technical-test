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
from unittest.mock import patch, mock_open
import builtins

def get(a):
    # Performs a http request, returning a string
    response = requests.get(a)
    return response.text

'''
Get HTML tag count
Inputs:
    - url: the URL to get the web page from
    - tag: the HTML tag to be counted
Outputs:
    - The number of occurrences the HTML tags were found
'''
def element_count(url, tag):
    # Raise ValueError exception if the URL provided
    # does not start with http:// or https://
    rex = re.compile(r'^(http|https)\:\/\/')
    if (not rex.match(url)):
        raise ValueError('This is not a URL!')

    output = get(url)
    soup = BeautifulSoup(output, 'html.parser')

    return len(soup.find_all(tag))

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

'''
Print output to file and to STDOUT
This function takes exactly four arguments
'''
def app_output(*args):
    with open('output.txt', 'a') as fd:
        fd.write('{} = {} = {} = {}\n'.format(*args))
    print('{} = {} = {} = {}\n'.format(*args))

'''
Main applicaton
Inputs:
    - url: the URL to get the webpage from
    - tag: the HTML tag to be counted
Outputs: string -> <url> = <tag> = <count> = <output of fizz_or_buzz>
'''
def app(url,tag):
    count = element_count(url,tag)
    fizzBuzzOutput = fizz_or_buzz(count)
    app_output(url,tag,count,fizzBuzzOutput)

'''
Unit tests for fizz_or_buzz
'''
class ut_fizzBuzz(unittest.TestCase):
    # Integer that can be divided by 3 but not by 5
    def test_fizz_3(self):
        output = fizz_or_buzz(3)
        self.assertEqual(output, 'fizz')

    # Negative value
    # -> should work as it was a positive
    def test_fizz_3_negative(self):
        output = fizz_or_buzz(-6)
        self.assertEqual(output, 'fizz')

    # Float value
    # -> should work if it can be divided by 3 / 5
    def test_fizz_3_float(self):
        output = fizz_or_buzz(3.0)
        self.assertEqual(output, 'fizz')

    # Integer that can be divided by 5 but not by 3
    def test_fizz_5(self):
        output = fizz_or_buzz(5)
        self.assertEqual(output, 'buzz')

    # Negative value
    # -> should work as it was a positive
    def test_fizz_5_negative(self):
        output = fizz_or_buzz(-10)
        self.assertEqual(output, 'buzz')

    # Float value
    # -> should work if it can be divided by 3 / 5
    def test_fizz_5_float(self):
        output = fizz_or_buzz(10.0)
        self.assertEqual(output, 'buzz')

    # Integer that can be divided by both 3 and 5
    def test_fizz_15(self):
        output = fizz_or_buzz(15)
        self.assertEqual(output, 'fizzbuzz')

    # Float value
    # -> should work if it can be divided by 3 / 5
    def test_fizz_15_float(self):
        output = fizz_or_buzz(15.0)
        self.assertEqual(output, 'fizzbuzz')

    # Negative value
    # -> should work as it was a positive
    def test_fizz_15_negative(self):
        output = fizz_or_buzz(-45)
        self.assertEqual(output, 'fizzbuzz')

    # 0 can be divided by all integers
    def test_fizz_0(self):
        output = fizz_or_buzz(0)
        self.assertEqual(output, 'fizzbuzz')

    # Float value
    # -> should work as well (0.0)
    def test_fizz_0_float(self):
        output = fizz_or_buzz(0.0)
        self.assertEqual(output, 'fizzbuzz')

    # Integer that can't be divided by either
    # 3 or 5
    # -> should return nothing
    def test_fizz_2(self):
        output = fizz_or_buzz(2)
        self.assertEqual(output, '')

    # Negative value
    # -> should work as it was a positive
    def test_fizz_2_negative(self):
        output = fizz_or_buzz(-2)
        self.assertEqual(output, '')

    # Float value
    # -> should work as well (2.19876)
    def test_fizz_2_float(self):
        output = fizz_or_buzz(2.19876)
        self.assertEqual(output, '')

    # NaN - string
    # -> should raise a TypeError
    def test_fizz_string(self):
        self.assertRaises(TypeError, fizz_or_buzz, 'string')

    # NaN - list
    # -> should raise a TypeError
    def test_fizz_list(self):
        self.assertRaises(TypeError, fizz_or_buzz, ['item1', 'item2'])

    # NaN - dictionary
    # -> should raise a TypeError
    def test_fizz_dict(self):
        self.assertRaises(TypeError, fizz_or_buzz, {'item1': 'value1', 'item2': 'value2'})

'''
Mock the requests.get call
This will be called as a 'side effect' when calling the Mock object
'''
def mock_requestsGet(*args):
    class responseObjectMock:
        def __init__(self, text):
            self.text = text

        def text(self):
            return self.text

    # Return data encapsulated in <>
    return responseObjectMock("<{}>".format(args[0]))

'''
Unit tests for the mocked functions:
    - requests.get
    - builtins.open
'''
class mock_testClass(unittest.TestCase):
    """
    Mock the get function so that a network connection is not needed to write tests
    Mock the open function so that a file won't be opened
    """
    @unittest.mock.patch('requests.get', side_effect = mock_requestsGet)
    @unittest.mock.patch('builtins.open', unittest.mock.mock_open())

    # Test that output.txt will not be created on the test rig
    # Test that a network connection is not required for testing get(a)
    def test_mockedFunctions(self, mock_get):
        # Call app_output
        app_output('param1', 'param2', 'param3','param4')
        # Check that 'output.txt' does not exist
        self.assertFalse(os.path.isfile('output.txt'))
        # Check that the mocked 'open' function was called
        builtins.open.assert_called_once_with('output.txt', 'a')

        # Call get(a)
        url = 'a href=http://github.com/'
        output = get(url)

        # Check output
        self.assertEqual(output, "<{}>".format(url))

        # Check that the mocked 'get' function was called
        mock_get.assert_called_once_with(url)

    '''
    Unit tests for element_count
    '''
    @unittest.mock.patch('requests.get', side_effect = mock_requestsGet)
    def test_elementCount_nomatch(self, mock_get):
        '''
        Input: 'http://a', 'a'
        Output: 0
        '''
        # Invoke element_count
        url, tag = 'http://a', 'a'
        count = element_count(url, tag)

        # Check output
        self.assertEqual(count, 0)

    @unittest.mock.patch('requests.get', side_effect = mock_requestsGet)
    def test_elementCount_wrong_url(self, mock_get):
        '''
        Input: 'a', 'a'
        Output: Exception (not a URL)
        '''

        url, tag = 'a', 'a'

        # Invoke element_count & check output
        self.assertRaises(ValueError, element_count, url, tag)

if __name__ == '__main__':
    # Catch KeyboardInterrupt
    try:
        # application will take two args url, html tag type (a, ul, div, ...etc)
        if len(sys.argv) < 3:
            url = input('Url: ')
            tag = input('Tag: ')
        else:
            url = sys.argv[1]
            tag = sys.argv[2]

            app(url, tag)
    except KeyboardInterrupt as e:
        print("Caught KeyboardInterrupt")
    finally:
        exit(0)

'''
Code Review

- os and re are not used at all and can be removed (however, they would be useful for unit testing)
- sys is imported twice (the second one is on line #54)
- No comment header for the functions (input parameters, output, what does the function do
- Input arguments could be parsed (argparse) instead of using positional arguments

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
   - no exception handling (what if the file is write-protected)
   - output is always appended to the existing file, I'm not sure if this is desired by the application
   - this could be assigned to a variable to avoid code duplication: '{} = {} = {} = {}\n'.format(*args)
-> app(a,b)
   - parameters 'a' & 'b' do not have a descriptive name
   - no input sanity checks
   - 'FizzBuzz' does not match with the existing naming convention
'''
