"""
Exercise object for work with JSON file's

"""

import os
import json
import random

TRAIN_FILE = os.path.join('resources', 'exercise', 'exercise.json')


class Exercise():
    """Class generate obj which means to return random exercise from json file"""
    def __init__(self, list):
        self._exercise = list
        self._len = len(self._exercise)

    def __len__(self):
        return self._len

    def __str__(self):
        return 'There are {} exercises'.format(self._len)

    def __repr__(self):
        return 'Exercise({})'.format(self._exercise)

    def __getitem__(self, item):
        return self._exercise[item]

    def __iter__(self):
        return self._exercise.__iter__()

    def to_json(self):
        return self._exercise

    #create obj by path argument which means to be *.json
    @classmethod
    def from_json(cls, path):
        with open(path) as f:
            return cls(json.load(f))

    def random_exercise(self):
        """
            random_exercise(self) -> list

            return exrcise as list with 2 elements where
            list[0] = title
            list[1] = text of exercise
        """

        return random.choice(self._exercise)


if __name__ == '__main__':

    #Filling json file or creating it with default data

    exer1 = ['title1',\
    '''
    Случайное упражнение1
    ''']
    exer2 = ['title2',\
    '''
    Случайное упражнение2
    ''']
    exer3 = ['title3',\
    '''
    Случайное упражнение3
    ''']
    exer4 = ['title4',\
    '''
    Случайное упражнение4
    ''']
    exer5 = ['title5',\
    '''
    Случайное упражнение5
    ''']
    exer6 = ['title6',\
    '''
    Случайное упражнение6
    ''']
    exer7 = ['title7',\
    '''
    Случайное упражнение7
    ''']
    exer8 = ['title8',\
    '''
    Случайное упражнение8
    ''']
    exer9 = ['title9',\
    '''
    Случайное упражнение9
    ''']
    exer10 = ['title10',\
    '''
    Случайное упражнение10
    ''']

    data = [exer1, exer2, exer3, exer4, exer5, exer6, exer7, exer8, exer9, exer10]

    print(data)
    with open(TRAIN_FILE, 'w') as o:
        json.dump(data, o)

    ''' debug
    show_inst = Exercise.from_json(TRAIN_FILE)
    print(show_inst)
    print(show_inst.__repr__())
        debug '''
