#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                   Version 2, December 2004
 
Copyright (C) 2015 Thoms Maurice <thomas@maurice.fr>
 
Everyone is permitted to copy and distribute verbatim or modified
copies of this license document, and changing it is allowed as long
as the name is changed.
 
           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
  TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
 
 0. You just DO WHAT THE FUCK YOU WANT TO.
"""

from clifactory import CommandLineInterface, Argument

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
