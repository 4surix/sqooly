# encode: utf-8
# Python 3.10.12
# ----------------------------------------------------------------------------

import os
import logging
import sqlite3
import traceback

from typing import List, Tuple, Any, Union


logger = logging.getLogger(__name__)


class DatabaseGroupCommands:

    def __init__(self):
        self.__commands = {}

    @property
    def commands(self) -> dict:
        return self.__commands

    def add(self, name:str, value):
        self.__commands[name] = value

    def get_command_or_group(self, name:str):
        return self.__commands.get(name, None)

    def __getattr__(self, attr:str):

        command = self.get_command_or_group(attr)

        if not command:
            logger.warn(f"Command '{attr}' not exist.")

        return command


class Database(DatabaseGroupCommands):

    def __init__(self, path:str):

        super().__init__()

        self.__path = path
        self.__database = sqlite3.connect(f'{self.__path}/database.db')
        self.__cursor = self.__database.cursor()

        def get(main_path:str, main_instance:Database):

            for path_file in os.listdir(main_path):

                path = f'{main_path}/{path_file}'

                if os.path.isdir(path):
                    instance = DatabaseGroupCommands()
                    get(path, instance)
                    main_instance.add(path_file, instance)

                elif os.path.isfile(path):
                    name_file, *exts_file = path_file.split('.')

                    if exts_file[-1] == 'sql':

                        with open(path, encoding='utf-8') as file:
                            data = file.read()

                        main_instance.add(
                            name_file, self.__command_execute(data)
                        )

        get(path, self)

        __init__ = self.get_command_or_group('__init__')

        if __init__:
            __init__()

    def __command_execute(self, text:str):

        data:List[str] = text.split('\n\n')

        tuple_empty = tuple()
        tuples_empty = (tuple_empty,) * len(data)

        return lambda *args: self.result([
            self.execute(content, args or tuple_empty)
            for content, args in zip(data, args + tuples_empty)
        ])

    def result(self, results:list) -> sqlite3.Cursor:
        return results[0] if len(results) == 1 else results

    def execute(self, content:str, args:Tuple[Any]):

        if not isinstance(args, tuple):
            args = (args,)

        try: result = self.__cursor.execute(content, args)
        except:
            logger.error(traceback.format_exc())
            result = None
        else:
            self.__database.commit()

        return result

    def close(self):
        self.__database.close()


def create(path:str) -> Database:
    return Database(path)