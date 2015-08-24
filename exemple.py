#!/usr/bin/env python
# -*- coding: utf-8 -*-

from command_line_interface import CommandLineInterface, Argument

cli = CommandLineInterface()
users = ["John Doe", "Dick Head"]

@cli.endpoint(Argument('user', help='username to add'))
def do_user_add(args):
    users.append(args.user)
    print users

@cli.endpoint()
def do_user_list(args):
    print users

cli.parse()
