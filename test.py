#!/usr/bin/env python

import unittest

import treeclient

TEST_SERVER = 'http://localhost:8080'
TEST_USER = 'test'
TEST_PASS = '1234'


class TestRobot(unittest.TestCase):

    def setUp(self):
        self.client = treeclient.RobotClient(TEST_SERVER, TEST_USER, TEST_PASS)

    def test_robots(self):
        print "Robots:\n", "\n".join(self.client.robots())

    def test_robot_aliases(self):
        print "Aliases:", "\n".join(map(lambda x: "{0} {1}".format(*x),self.client.robots_aliases()))

    def test_abilities(self):
        print "Abilities:\n", "\n".join(self.client.abilities())

    def test_create_robot(self):
        print self.client.create_robot()

    def test_get_data(self):
        self.client.robots_aliases()
        print self.client.get_data('099c4a07-5d81-4ec3-a60c-eb70364a5ed2')
        self.assertTrue('test' in self.client.aliases)
        print self.client.get_data('test')

    def test_set_alias(self):
        print self.client.set_alias('099c4a07-5d81-4ec3-a60c-eb70364a5ed2','test')

if __name__ == "__main__":
    unittest.main()
