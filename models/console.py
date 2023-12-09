#!/usr/bin/python3
'''Command Line Interpreter'''
import cmd
import json
import re
import sys
from models import *
from models import storage


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb)"

    def do_quit(self, *args):
        '''Usage: quit
           Function: Exits the program
        '''
        return True

    def do_EOF(self, *args):
        '''Usage: EOF
           Function: It Exits the program
        '''
        print()
        return True



    def do_create(self, line):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        if line != "" or line is not None:
            if line not in storage.classes():
                print("**The class doesn't exist **")
            else:
                # create an instance from the given class
                obj_intance = storage.classes()[line]()
                obj_intance.save()
                print(obj_intance.id)
        else:
            print("** class name is missing **")

    def do_show(self, line):
        '''Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        '''
        # check if class name and instance id was provided from the user
        if line == "" or line is None:
            print("** class name is missing **")

        else:
            # get all the arguments passed via the command line
            class_info = line.split(" ")
            if len(class_info) < 2:
                print("** instance id is missing **")
            else:
                class_name = class_info[0]
                instance_id = class_info[1]
                # check if class name is existing
                if class_name in storage.classes():
                    # check if instance_id is existing
                    key = f"{class_name}.{instance_id}"
                    if key not in storage.all():
                        print("**There is  no instance found **")
                    else:
                        instance_dict = storage.all()[key]
                        print(instance_dict)

                else:
                    print("** class doesn't exist **")


    def do_all(self, line):
        '''Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects.
        '''
        instance_obj = storage.all()
        instance_list = []

        if line == "" or line is None:
            for key, value in storage.all().items():
                instance_list.append(str(value))
            print(instance_list)

        else:
            if line not in storage.classes():
                print("** class doesn't exist **")
                return
            else:
                for key, value in storage.all().items():
                    class_name, instance_id = key.split(".")
                    if line == class_name:
                        instance_list.append(str(value))
                print(instance_list)

    def do_destroy(self, line):
        '''Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id.
        '''
        # check if class name and instance id was provided from the user
        if line == "" or line is None:
            print("** class name is missing **")

        else:
            # get all the arguments passed via the command line
            class_info = line.split(" ")
            if len(class_info) < 2:
                print("** instance id is missing **")
            else:
                class_name = class_info[0]
                instance_id = class_info[1]
                # check if class name  is existing
                if class_name in storage.classes():
                    # check if instance_id exists
                    key = f"{class_name}.{instance_id}"
                    if key not in storage.all():
                        print("** no instance found **")
                    else:
                        # delete this instance and save to json file
                        del storage.all()[key]
                        storage.save()
                        return

                else:
                    print("** class doesn't exist **")




    def do_update(self, line):
        '''Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary.'''


        checks = re.search(r"^(\w+)\s([\S]+?)\s({.+?})$", line)
        if checks:
            # it is a dictionary
            class_name = checks.group(1)
            instance_id = checks.group(2)
            update_dict = checks.group(3)

            if class_name is None:
                print("** class name missing **")
            elif instance_id is None:
                print("** instance id missing **")
            elif update_dict is None:
                print("** attribute name missing **")
            else:
                if class_name not in storage.classes():
                    print("** class doesn't exist **")
                else:
                    key = f"{class_name}.{instance_id}"
                    if key not in storage.all():
                        print("** no instance found **")
                    else:
                        instance_dict = storage.all()[key]
                        update_dict = json.loads(update_dict)

                        attributes = storage.attributes()[class_name]
                        
                        for key, value in update_dict.items():
                            if key in attributes:
                               
                                value = attributes[key](value)
                               
                                setattr(instance_dict, key, value)
                                storage.save()

        else:
            
            checks = re.search(
                r"^(\w+)\s([\S]+?)\s\"(.+?)\"\,\s\"(.+?)\"", line)
            class_name = checks.group(1)
            instance_id = checks.group(2)
            attribute = checks.group(3)
            value = checks.group(4)

            if class_name is None:
                print("** class name is missing **")
            elif instance_id is None:
                print("** instance id is missing **")
            elif attribute is None:
                print("** attribute name is missing **")
            elif value is None:
                print("** value is missing **")
            else:
                
                if class_name not in storage.classes():
                    print("** class doesn't exist **")
                else:
                    key = f"{class_name}.{instance_id}"
                    if key not in storage.all():
                        print("** no instance found **")
                    else:
                        instance_dict = storage.all()[key]
                        
                        attributes_dict = storage.attributes()[class_name]
                        
                        value = attributes_dict[attribute](
                            value)  
                        setattr(instance_dict, attribute, value)
                        storage.save()

    def emptyline(self):
        pass

    def do_count(self, line):
        '''Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class.
        '''
        count = 0
        for key in storage.all().keys():
            class_name, instance_id = key.split(".")
            if line == class_name:
                count += 1
        print(count)


    def precmd(self, line):
        
        if not sys.stdin.isatty():
            print()

        checks = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
        if checks:
            class_name = checks.group(1)
            command = checks.group(2)
            args = checks.group(3)

            if args is None:
                line = f"{command} {class_name}"
                return ''
            else:
                
                args_checks = re.search(r"^\"([^\"]*)\"(?:, (.*))?$", args)
                instance_id = args_checks[1]

                if args_checks.group(2) is None:
                    line = f"{command} {class_name} {instance_id}"
                else:
                    attribute_part = args_checks.group(2)

                    line = f"{command} {class_name} {instance_id} \
{attribute_part}"
                return ''

        return cmd.Cmd.precmd(self, line)
        # return ''




if __name__ == '__main__':
    HBNBCommand().cmdloop()
