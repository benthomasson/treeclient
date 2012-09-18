#!/usr/bin/env python

import unittest

import treeclient

TEST_SERVER = 'http://localhost:8080'
TEST_USER = 'test'
TEST_PASS = '1234'


class TestRobot(unittest.TestCase):

    def test(self):
        client = treeclient.RobotClient(TEST_SERVER, TEST_USER, TEST_PASS)
        print "Robots:\n", "\n".join(client.robots())

    def test_config(self):
        client = treeclient.RobotClient(TEST_SERVER, TEST_USER, TEST_PASS)
        print "Config:\n", "\n".join(client.get_config('81184a74-2258-4e9b-9270-0f2def0191b1'))

if __name__ == "__main__":
    unittest.main()
