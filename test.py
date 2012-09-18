#!/usr/bin/env python

import unittest

import treeclient

TEST_SERVER = 'http://localhost:8080'
TEST_USER = 'test'
TEST_PASS = '1234'


class TestRobot(unittest.TestCase):

    def test(self):
        client = treeclient.RobotClient(TEST_SERVER, TEST_USER, TEST_PASS)
        print client.robots()

if __name__ == "__main__":
    unittest.main()
