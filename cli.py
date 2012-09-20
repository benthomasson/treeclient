#!/usr/bin/env python

from settings import SERVER, USER, PASS
from rest import RobotClient
from IPython import embed
from IPython.core.magic import Magics, magics_class, line_magic
from IPython.frontend.terminal.embed import InteractiveShellEmbed
from IPython.frontend.terminal.interactiveshell import TerminalInteractiveShell
from IPython.frontend.terminal.ipapp import load_default_config
import tempfile
import os
import json

_client = RobotClient(SERVER, USER, PASS)


@magics_class
class RobotMagics(Magics):

    @line_magic
    def robots(self, _=''):
        for uuid, alias in _client.robots_aliases():
            if alias:
                print "{0} <{1}>".format(uuid, alias)
            else:
                print uuid

    @line_magic
    def get_data(self, s=''):
        print json.dumps(_client.get_data(s), indent=4, sort_keys=True)

    @line_magic
    def set_alias(self, s=''):
        robot, _, alias = s.partition(' ')
        _client.set_alias(robot, alias)

    @line_magic
    def create_robot(self, s=''):
        print _client.create_robot()


def _get_robot_completer(*args, **kwargs):
    robots = []
    robots.extend(_client.robots())
    robots.extend(_client.aliases.keys())
    return robots


class CliInteractiveShellEmbed(InteractiveShellEmbed):

    def init_magics(self):
        super(CliInteractiveShellEmbed, self).init_magics()
        self.register_magics(RobotMagics)

    def init_completer(self):
        super(CliInteractiveShellEmbed, self).init_completer()
        self.set_hook('complete_command', _get_robot_completer, str_key='%get_data')
        self.set_hook('complete_command', _get_robot_completer, str_key='%set_alias')


if __name__ == "__main__":
    config = load_default_config()
    config.InteractiveShellEmbed = config.TerminalInteractiveShell
    CliInteractiveShellEmbed(config=config)(header='Yo!')
