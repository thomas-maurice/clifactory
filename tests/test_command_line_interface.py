# -*- coding: utf-8 -*-

import unittest
import mock

class TestCommandLineInterface(unittest.TestCase):
    def test_basic_routing(self):
        from command_line_interface import CommandLineInterface
        cli = CommandLineInterface()

        @cli.endpoint()
        def do_help(args):
            return "Usage: nosetests"

        @cli.endpoint()
        def do_version(args):
            return "1.7.2"

        self.assertEqual("Usage: nosetests", cli.parse(["help"]))
        self.assertEqual("1.7.2", cli.parse(["version"]))

    def test_nested_routing(self):
        from command_line_interface import CommandLineInterface
        cli = CommandLineInterface()

        @cli.endpoint()
        def do_link_list(args):
            return "eth0"

        @cli.endpoint()
        def do_addr_list(args):
            return "127.0.0.1"

        self.assertEqual("eth0", cli.parse(["link", "list"]))
        self.assertEqual("127.0.0.1", cli.parse(["addr", "list"]))

