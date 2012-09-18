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

_client = RobotClient(SERVER, USER, PASS)


@magics_class
class RobotMagics(Magics):

    @line_magic
    def robots(self, _=''):
        print "\n".join(_client.robots())

    @line_magic
    def get_config(self, s=''):
        print "\n".join(_client.get_config(s))

    @line_magic
    def edit_config(self, s=''):
        config =  "\n".join(_client.get_config(s))
        f, name = tempfile.mkstemp()
        os.write(f,config)
        os.close(f)
        self.shell.hooks.editor(name,1)
        with open(name) as f:
            new_config = f.read()
        print new_config
        os.unlink(name)



def _get_config_completer(*args, **kwargs):
    return _client.robots()


class CliInteractiveShellEmbed(InteractiveShellEmbed):

    def init_magics(self):
        super(CliInteractiveShellEmbed, self).init_magics()
        self.register_magics(RobotMagics)

    def init_completer(self):
        super(CliInteractiveShellEmbed, self).init_completer()
        self.set_hook('complete_command', _get_config_completer, str_key='%get_config')
        self.set_hook('complete_command', _get_config_completer, str_key='%edit_config')


if __name__ == "__main__":
    config = load_default_config()
    config.InteractiveShellEmbed = config.TerminalInteractiveShell
    CliInteractiveShellEmbed(config=config)(header='Yo!')
