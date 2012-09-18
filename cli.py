#!/usr/bin/env python

from settings import SERVER, USER, PASS
from rest import RobotClient
from IPython import embed
from IPython.core.magic import Magics, magics_class, line_magic
from IPython.frontend.terminal.embed import InteractiveShellEmbed
from IPython.frontend.terminal.interactiveshell import TerminalInteractiveShell
from IPython.frontend.terminal.ipapp import load_default_config

_client = RobotClient(SERVER, USER, PASS)

@magics_class
class RobotMagics(Magics):

    @line_magic
    def robots(self, parameter_s=''):
        return _client.robots()

    @line_magic
    def get_config(self, parameter_s=''):
        print parameter_s
        return _client.get_config(parameter_s)


class CliInteractiveShellEmbed(InteractiveShellEmbed):

    def init_magics(self):
        super(CliInteractiveShellEmbed, self).init_magics()
        self.register_magics(RobotMagics)

if __name__ == "__main__":
    config = load_default_config()
    config.InteractiveShellEmbed = config.TerminalInteractiveShell
    CliInteractiveShellEmbed(config=config)(header='Yo!')

