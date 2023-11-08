#!/usr/bin/python3



"""
The hbnb console
"""
import cmd

class HBNBCommand(cmd.Cmd):
    """Implements a command interpreter"""

    prompt = '(hbnb) '

    def do_EOF(self):
        """Exits the interpreter"""

        return True

    def do_quit(self, line):
        """Exits the interpreter"""

        return True

    def emptyline(self):
        """Handles empty lines"""
        pass

    def postloop(self):
        print()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
