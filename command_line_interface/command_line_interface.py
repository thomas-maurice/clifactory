#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (C) 2015  Thomas Maurice <thomas@maurice.fr>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import argparse

class Argument(object):
    """Argument: An interface to argparse's add_argument function
    
    Arguments are simply built using add_argument parameters.
    """
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

class ExclusiveGroup(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.required = False
        if 'required' in kwargs:
            self.required = kwargs['required']

class CommandLineInterface(object):
    """CommandLineInterface: Provides a convenient way of building CLIs
    
    This is a wrapper around argparse allowing you to define git-like
    subcommand based CLIs with minimal efforts. You basically just have to
    define your functions following a pattern like "do_some_shit" and
    decorate them using the CommandLineInterface.endpoint function.
    
    This will allow you to do things like ./cli.py some shit <args>.
    """
    def __init__(self):
        """__init__: Performs basic initialisations"""
        # Root parser
        self.parser = argparse.ArgumentParser()
        # Subparsers
        self.subparsers = self.parser.add_subparsers()
        # Parser dictionary, to avoir overwriting existing parsers
        self.parsers = {}
    
    def add_root_arguments(self, *args):
        for argument in args:
            if type(argument) == Argument:
                self.parser.add_argument(*argument.args, **argument.kwargs)
            elif type(argument) == ExclusiveGroup:
                group = self.parser.add_mutually_exclusive_group(required=argument.required)
                for arg in argument.args:
                    group.add_argument(*arg.args, **arg.kwargs)
    
    def parse(self, line=None):
        """parses the line provided, if None then uses sys.argv"""
        args = self.parser.parse_args(args=line)
        return args.func(args)
        
    
    def endpoint(self, *args):
        """endpoint: Decorates a function to make it a CLI endpoint
        
        The function must be called do_<some>_<action> and accept one 'args'
        parameter. It will be converted into a ./cli some action commandline
        endpoint.
        
        A set of Arguments can be passed to the decorator, the syntax is the
        same than the argparse add_argument function.
        """
        # Decorator function
        def decorator(func):
            func_name = func.__name__
            func_name = func_name.replace("do_", "")
            actions = func_name.split("_")
            cmd_parser = None
            sub = self.subparsers
            wcount = 0
            # For each word in the command we build the parsing tree
            for word in actions:
                parser_name = '_'.join(actions[:wcount+1])
                # If the parser exist, we use it, otherwise we create it
                if self.parsers.has_key(parser_name):
                    cmd_parser = self.parsers[parser_name]
                else:
                    cmd_parser = sub.add_parser(word)
                    self.parsers[parser_name] = cmd_parser
                # We don't want to add a subparser to the final endpoint,
                # since it would require a void positional argument and
                # fuck up the whole thing.
                if wcount != len(actions) - 1:
                    # Same that with the parsers, it it exist we use it
                    # otherwise we create it. It avoids overwrites
                    if self.parsers.has_key("sub_"+parser_name):
                        sub = self.parsers["sub_"+parser_name]
                    else:
                        sub = cmd_parser.add_subparsers()
                        self.parsers["sub_"+parser_name] = sub
                wcount += 1
            # Bind the endpoint to the function
            cmd_parser.set_defaults(func=func)
            # We add the arguments to the function
            for argument in args:
                if type(argument) == Argument:
                    cmd_parser.add_argument(*argument.args, **argument.kwargs)
                elif type(argument) == ExclusiveGroup:
                    group = cmd_parser.add_mutually_exclusive_group(required=argument.required)
                    for arg in argument.args:
                        group.add_argument(*arg.args, **arg.kwargs)
            
            # Standard inner function
            def inner(*args, **kwargs):
                return func(*args, **kwargs)
                
            return inner
        return decorator
