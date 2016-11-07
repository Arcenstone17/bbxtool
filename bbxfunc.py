"""
dynamic functions for form elements actions
"""

import os
import bbdb
import bbxgui
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox


def _cb_output(comboBox, query_result, query, change_state):
    """
        _cb_output(comboBox, query_result, query, change_state)

        Write in object text:
            ComboBox: all of query_result explanation depends on change_state
            query: deep copy of query_result
    """
    comboBox.clear()
    query.clear()
    # For some reason copy.deepcopy wont work ?
    # deepcopy cant copy rowproxy correct ?
    # query = copy.deepcopy(query_result)

    # Check query_result as rowProxy or tuple or list, on emptyness
    try:
        query_result[0]
    except:
        comboBox.addItem(' No result for your query :( ')
        return False
    if change_state:

        for i in range(len(query_result)):
            query.append(query_result[i])
            comboBox.addItem('{} - {}'.format(query_result[i].literal, query_result[i].name))

    else:
        for i in range(len(query_result)):
            comboBox.addItem(query_result[i].beat_text)


def is_data_correct(liter=None, name=None, diff=None, sample=None, type_=None, url=None, beat=None, bpm=None):
    """
            is_data_correct(liter=None, name=None, diff=None,
            sample=None, type_=None, url=None, beat=None, bpm=None) -> bool

            return true if all input data is correct for db column and custom restrictions
            otherwise raise ValueError
    """

    if liter:
        if not liter.isalpha():
            raise ValueError('Beat literal must contain only letters')

    if name:
        if len(name) > 255:
            raise ValueError('Too long sound definition try make it shortly')

    if diff or diff == 0:           # seems there is more logical way to do it ?
        if diff < 0 or diff > 100:
            raise ValueError('Difficulty must be beetwin 0 and 100')

    if sample:
        pass

    if type_:
        if type_.casefold() not in ('inward', 'outward', 'free'):
            raise ValueError('Type must be either inward or outward or free')

    if url:
        pass

    if beat:
        if len(beat) > 1000:
            raise ValueError('wow too long beat')

    if bpm is not None:
        if bpm < 30 or bpm > 220:
            raise ValueError('BPM must be beetwin 30 and 220')

    return True


def search_action(comboBox, query, change_state, array=None, bpm=None, diff=None):
    '''
        search_action(comboBox, query, change_state, array=None, bpm=None, diff=None)

        layer beetwin editBoxes and DB which check values on correct and call _cb_output()
    '''

    # message boxes in case of data out of borders (TypeError boxes mainly for debug)
    if change_state:
        try:
            is_data_correct(liter=array, type_=bpm, diff=diff)
        except ValueError as f:
            _alarm(str(f))
            return False
        except TypeError:
            _alarm('some type is incorrect')
            return False

        _cb_output(comboBox, bbdb.show_table_sounds(liter=array, diff=diff, type_=bpm), query, change_state)

    else:
        try:
            is_data_correct(beat=array, bpm=bpm, diff=diff)
        except ValueError as f:
            _alarm(str(f))
            return False
        except TypeError:
            _alarm('some type is incorrect')
            return False

        _cb_output(comboBox, bbdb.show_table_beats(beat=array, diff=diff, bpm=bpm), query, change_state)


def metro_func(metroLabel, soundObj, metro_state):
    """
        metro_func(Label, Dial, metro_state)

        switch element visibility depend on metro_state
    """

    metroLabel.setVisible(metro_state)
    soundObj.setVisible(metro_state)


def change_func(changeAction, diffLabel, bpmLabel, arrayLabel, searchLabel, change_state):
    """
            change_func(QAction, Label, Label, Label, Label, change_state)

            switch element texts and icon depend on change_state
    """

    if change_state:
        diffLabel.setText('difficulty')
        bpmLabel.setText('type')
        arrayLabel.setText('literal')
        searchLabel.setText(' Search \n Sound')
        changeAction.setIcon(QtGui.QIcon(bbxgui.CHANGE_ICON_B))

    else:
        diffLabel.setText('difficulty')
        bpmLabel.setText('bpm')
        arrayLabel.setText('used sounds')
        searchLabel.setText(' Search \n Beat')
        changeAction.setIcon(QtGui.QIcon(bbxgui.CHANGE_ICON_A))


def dial_func(metroLabel, value):
    """
        dial_func(Label, value)

        set label text in value
    """

    metroLabel.setText('{} BPM'.format(str(value)))


def url_func(urlEdit, urlButton, url_state):
    """
        url_func(Edit, Button, url_state)

        switch element visibility depend on url_state
    """

    urlButton.setVisible(url_state)
    urlEdit.setVisible(url_state)


def write_beat_to_db(array=None, bpm=None, diff=None):
    """
        write_beat_to_db(array=None, bpm=None, diff=None)

        run alarm message if any input data incorrect otherwise write data into beats table
    """

    if not array:
        _alarm('Beat cant be empty')
        return False
    try:
        is_data_correct(beat=array, bpm=bpm, diff=diff)
    except ValueError as f:
        _alarm(str(f))
        return False
    except TypeError:
        _alarm('some type is incorrect')
        return False

    bbdb.add_item_to_beats(array, diff=diff, bpm=bpm)


def write_sound_to_db(array=None, type_=None, diff=None, sample=None, url=None, name=None):
    """
        write_sound_to_db(array=None, type_=None, diff=None, sample=None, url=None, name=None)

        run alarm message if any input data incorrect otherwise write data into sounds table
    """

    if not array:
        _alarm('literal cant be empty')
        return False
    if not name:
        _alarm('Put some discribe for sound')
        return False

    try:
        is_data_correct(liter=array, name=name, diff=diff, sample=sample, type_=type_, url=url)
    except ValueError as f:
        _alarm(str(f))
        return False
    except TypeError:
        _alarm('some type is incorrect')
        return False

    bbdb.add_item_to_sounds(array, name, diff=diff, sample=sample, type_=type_, url=url)


def _alarm(mess):
    """
        _alarm(message)

        create and execute alarm message with message text
    """

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("Input data is incorrect")
    msg.setInformativeText(mess)
    msg.setWindowTitle('incorrect data')
    msg.exec()


def create_sub_window(change_state, parent):
    """
        create_sub_window(change_state, parent)

        create sub window for current parent, type of window depends on change_state
    """

    if change_state:
        bbxgui.SoundsSubWindow(parent)
    else:
        bbxgui.BeatsSubWindow(parent)


def rb_change(comboBox, displayLabel, query, urlEdit):
    """
        rb_change(comboBox, Label, query, Edit)

        change Label text to current comboBox text also
        change Edit text into .lesson_url RowProxy field in query
    """

    displayLabel.setText(comboBox.currentText())
    url_list = []
    for i in range(len(query)):
        url_list.append(query[i].lesson_url)

    if query:
        current_url = url_list[comboBox.currentIndex()]
        if current_url:
            urlEdit.setText(url_list[comboBox.currentIndex()])
        else:
            urlEdit.setText('no lesson for this :(')
    else:
        urlEdit.setText('no lesson for this :(')


def url_open(url):
    """
        url_open(url)

        open ulr wiht current os tool
    """

    # bad bad bad opening find some way to make it better ?
    if url.startswith('http'):
        os.system("start {}".format(url))
    else:
     # also need to fix ?
        _alarm('bad url')


def exer_func(parent, exer):
    """
        exer_func(parent, exer)

        create sub window for current parent with current exer parameters:
        Window title: exer[0]
        Window content: exer[1]
    """

    bbxgui.ExerciseSubWindow(parent, exer)


if __name__ == '__main__':
    print('hi there')