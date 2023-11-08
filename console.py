#!/usr/bin/python3



"""
The hbnb console
"""
import cmd
from models.base_model import BaseModel
import models

class HBNBCommand(cmd.Cmd):
    """Implements a command interpreter"""

    prompt = '(hbnb) '
    
    def validate_input(self, model_id):
        """Validates interpreter input"""
        if model_id:
            model_list = model_id.split(' ', 1)
            if model_list[0] in globals():
                if len(model_list) >= 2:
                    model_id = model_id.replace(" ", ".")
                    objects = models.storage.all()
                    if model_id in objects.keys():
                        return True
                    else:
                        print("** no instance found **")
                else:
                    print("** instance id missing **")
            else:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")
        return False
    
    def do_all(self, class_name=None):
        """
        Prints string representation of all instances
        based on class_name
        """
        objects = models.storage.all()
        obj_list = []
        if class_name is not None:
            for key, value in objects.items():
                if value.__class__.__name__ == class_name:
                    obj_list.append(str(value))
        else:
            for key, value in objects.items():
                obj_list.append(str(value))

        print(obj_list)

    def do_create(self, class_name):
        """Validates the classname and creates new instance"""

        if class_name:
            if class_name in globals():
                obj = eval("{}()".format(class_name))
                obj.save()
                print(obj.id)
            else:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")

    def do_show(self, model_id):
        """Prints the string representation of an object"""
        if self.validate_input(model_id):
            model_id = model_id.replace(" ", ".")
            objects = models.storage.all()
            print(objects[model_id])

    def do_destroy(self, model_id):
        """Deletes an instance based on class name and id"""
        if self.validate_input(model_id):
            model_id = model_id.replace(" ", ".")
            objects = models.storage.all()
            del objects[model_id]
            models.storage.save()


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
