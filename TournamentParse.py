#!/usr/bin/python3

'''

TournamentParse.py - Parses .wer and .tournament files (XML files created by
                     Wizards Event Reporter and Konami Tournament Software
                     respectively) and pull out the names and player ID number
                     of each indivdual player, the event date, and the number
                     of participants.

                     Written by: Patrick Coyle

TO DO:

Design the UI
Make this read the files .wer and .tournament files
'''
import sys

import xml.etree.ElementTree as ET

from PyQt5.QtWidgets import (QMessageBox, QMainWindow, QApplication,
                             QVBoxLayout, QPushButton, QAction, QDialog,
                             QLabel, QWidget, QFileDialog)

from PyQt5.QtSql import QSqlDatabase, QSqlQuery

class ParseMain(QMainWindow):

    # Creates and displays the main window. Has methods used for
    # interacting with the tournaments database

    def __init__(self):

        super().__init__()

        # self.ParseWidget = ParseWidget(self)
        # Uncomment once ParseWidget is created

        self.db = QSqlDatabase.addDatabase('QSQLITE')
        # QSQLITE refers to Sqlite3
        self.db.setDatabaseName('tournaments.db')
        # Creates the database if it doesn't exist, or loads the
        # previously created database

        self.initUI()

    def initUI(self):

        ### Menu Bar ###

        menubar = self.menuBar()

        file_menu = menubar.addMenu('&File')

        new_event = QAction('&New Event', self)
        new_event.setShortcut('Ctrl+N')
        new_event.triggered.connect(self.start_new_event)

        browse_files = QAction('&Open Tournament', self)
        browse_files.setShortcut('Ctrl+T')
        browse_files.triggered.connect(self.read_file)

        file_menu.addAction(new_event)
        file_menu.addAction(browse_files)

        ### Window Settings ###

        # self.setCentralWidget(self.ParseWidget)
        # Uncomment once ParseWidget is created

        self.setGeometry(300, 300, 800, 400)

        self.setWindowTitle('Tournament Parse')

        self.show()

    def start_new_event(self):

        '''
        Creates a new table for a new event that players can qualify for,
        and options for that event (such as date, number of points needed
        to qualify)
        '''
    
        pass

    def read_file(self):

        '''
        Uses QFileDialog to let the user select a .tournament or.wer file they wish to parse

        TO DO:
        Have this do more than just print the file name
        '''

        file_name = QFileDialog.getOpenFileName(self,
                                                'Select a .tournament or .wer file',
                                                '',
                                                'Tournament Files (*.Tournament *.wer)')
        print(file_name)
class ParseWidget(QWidget):

    def __init__(self, p_main):

        # main: the reference to the main window so that methods in
        #       ParseWidget can interact with the main window.

        self.p_main = p_main

if __name__ == '__main__':

    app = QApplication(sys.argv)
    parser = ParseMain()
    sys.exit(app.exec_())
