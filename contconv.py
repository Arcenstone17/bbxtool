'''functions for safety convert object text content'''

from PyQt4.QtGui import QMessageBox

def diff_conv(editBox, change_state):
    '''
        diff_conv(editBox, change_state) -> int

        difficulty always convert to int in case of exception:
         just clear text and return None
    '''

    if change_state:
        try:
            return int(editBox.text())
        except ValueError:
            editBox.clear()
    else:
        try:
            return int(editBox.text())
        except ValueError:
            editBox.clear()


def bpm_conv(editBox, change_state):
    '''
        bpm_conv(editBox, change_state) -> int or str

        depends on mode return either sound type as str or bpm as int
        in case of exception:
        just clear text and return None
    '''

    if change_state:
        # Remove unwanted message boxes?
        '''res = editBox.text()
        res = res.replace(' ', '')
        res = res.casefold()

        if res in ('inward', 'outward', 'free'):
            return res
        else: editBox.clear()'''
        return editBox.text()
    else:
        try:
            return int(editBox.text())
        except ValueError:
            editBox.clear()


def array_conv(editBox, change_state):
    '''
        array_conv(editBox, change_state) -> str

        return Edit text stripped
    '''

    # Some restrict?
    if change_state:
        return editBox.text().strip()
    else:
        return editBox.text().strip()


def sample_conv(editBox):
    '''
        sample_conv(editBox, editBox) -> str

        return Edit text
    '''

    return editBox.text()


def url_conv(editBox):
    '''
        url_conv(editBox, editBox) -> str

        return Edit text
    '''

    return editBox.text()


def name_conv(editBox):
    '''
        name_conv(editBox, editBox) -> str

        return Edit text
    '''

    return editBox.text()

