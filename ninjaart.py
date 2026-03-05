#!/usr/bin/env python3

'''
NinjaArt - Network Infrastructure Penetration Testing Tool
Copyright (c) 2020 SECFORCE (Antonio Quina and Leonidas Stavliotis)

    This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

# check for dependencies first (make sure all non-standard dependencies are checked for here)
# TODO: review this.
try:
    from sqlalchemy.orm import scoped_session as scoped_session
except ImportError as e:
    print("[-] Import failed. SQLAlchemy library not found. \nTry installing it with: apt install python3-sqlalchemy")
    print(e)
    exit(1)
    
try:
    from PyQt5 import QtGui, QtCore, QtWidgets
except ImportError as e:
    print("[-] Import failed. PyQt5 library not found. \nTry installing it with: apt install python3-pyqt5")
    print(e)
    exit(1)

import sys
import argparse
from app.logic import Logic
from ui.gui import Ui_MainWindow
from ui.view import View
from controller.controller import Controller

# this class is used to catch events such as arrow key presses or close window (X)
class MyEventFilter(QtCore.QObject):
    
    def eventFilter(self, receiver, event):
        # catch up/down arrow key presses in hoststable
        #if(event.type() == QtCore.QEvent.KeyPress and (receiver == view.ui.HostsTableView or receiver == view.ui.ServiceNamesTableView or receiver == view.ui.ToolsTableView or receiver == view.ui.ToolHostsTableView or receiver == view.ui.ScriptsTableView or receiver == view.ui.ServicesTableView or receiver == view.settingsWidget.toolForHostsTableWidget or receiver == view.settingsWidget.toolForServiceTableWidget or receiver == view.settingsWidget.toolForTerminalTableWidget)):
        if(event.type() == QtCore.QEvent.KeyPress and (receiver == view.ui.HostsTableView or receiver == view.ui.ServiceNamesTableView or receiver == view.ui.ToolsTableView or receiver == view.ui.ToolHostsTableView or receiver == view.ui.ScriptsTableView or receiver == view.ui.ServicesTableView)):
            key = event.key()
            if not receiver.selectionModel().selectedRows():
                return True
            index = receiver.selectionModel().selectedRows()[0].row()
            
            if key == QtCore.Qt.Key_Down: 
                newindex = index + 1
                receiver.selectRow(newindex)
                receiver.clicked.emit(receiver.selectionModel().selectedRows()[0])

            elif key == QtCore.Qt.Key_Up:
                newindex = index - 1
                receiver.selectRow(newindex)
                receiver.clicked.emit(receiver.selectionModel().selectedRows()[0])

            elif QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier and key == QtCore.Qt.Key_C:    
                selected = receiver.selectionModel().currentIndex()
                clipboard = QtWidgets.QApplication.clipboard()
                clipboard.setText(selected.data().toString())

            return True
            
        elif(event.type() == QtCore.QEvent.Close and receiver == MainWindow):
            event.ignore()
            view.appExit()
            return True
            
        else:
            return super(MyEventFilter,self).eventFilter(receiver, event)    # normal event processing

def applyAppearanceSettings(app, mainWindow, settings):
    """Apply theme and font settings to the application"""
    # Define theme color schemes
    themes = {
        'Default': '',
        'Dark': '''
            QMainWindow, QWidget { background-color: #2b2b2b; color: #ffffff; }
            QTableView, QTreeView, QListView { background-color: #1e1e1e; color: #ffffff; alternate-background-color: #2d2d2d; }
            QTabWidget::pane { border: 1px solid #444; }
            QTabBar::tab { background-color: #3c3c3c; color: #ffffff; padding: 8px 16px; }
            QTabBar::tab:selected { background-color: #505050; }
            QPushButton { background-color: #3c3c3c; color: #ffffff; border: 1px solid #555; padding: 5px 15px; }
            QPushButton:hover { background-color: #505050; }
            QLineEdit, QTextEdit, QPlainTextEdit { background-color: #1e1e1e; color: #ffffff; border: 1px solid #555; }
            QComboBox { background-color: #3c3c3c; color: #ffffff; border: 1px solid #555; }
            QMenuBar { background-color: #2b2b2b; color: #ffffff; }
            QMenuBar::item:selected { background-color: #505050; }
            QMenu { background-color: #2b2b2b; color: #ffffff; }
            QMenu::item:selected { background-color: #505050; }
            QCheckBox { color: #ffffff; }
            QLabel { color: #ffffff; }
            QGroupBox { color: #ffffff; border: 1px solid #555; }
        ''',
        'Light': '''
            QMainWindow, QWidget { background-color: #f5f5f5; color: #333333; }
            QTableView, QTreeView, QListView { background-color: #ffffff; color: #333333; alternate-background-color: #f0f0f0; }
            QTabWidget::pane { border: 1px solid #ccc; }
            QTabBar::tab { background-color: #e0e0e0; color: #333333; padding: 8px 16px; }
            QTabBar::tab:selected { background-color: #ffffff; }
            QPushButton { background-color: #e0e0e0; color: #333333; border: 1px solid #ccc; padding: 5px 15px; }
            QPushButton:hover { background-color: #d0d0d0; }
            QLineEdit, QTextEdit, QPlainTextEdit { background-color: #ffffff; color: #333333; border: 1px solid #ccc; }
            QComboBox { background-color: #ffffff; color: #333333; border: 1px solid #ccc; }
        ''',
        'Hacker': '''
            QMainWindow, QWidget { background-color: #0a0a0a; color: #00ff00; }
            QTableView, QTreeView, QListView { background-color: #000000; color: #00ff00; alternate-background-color: #0a0a0a; }
            QTabWidget::pane { border: 1px solid #00ff00; }
            QTabBar::tab { background-color: #0a0a0a; color: #00ff00; padding: 8px 16px; border: 1px solid #00ff00; }
            QTabBar::tab:selected { background-color: #003300; }
            QPushButton { background-color: #0a0a0a; color: #00ff00; border: 1px solid #00ff00; padding: 5px 15px; }
            QPushButton:hover { background-color: #003300; }
            QLineEdit, QTextEdit, QPlainTextEdit { background-color: #000000; color: #00ff00; border: 1px solid #00ff00; }
            QComboBox { background-color: #0a0a0a; color: #00ff00; border: 1px solid #00ff00; }
            QMenuBar { background-color: #0a0a0a; color: #00ff00; }
            QMenu { background-color: #0a0a0a; color: #00ff00; }
            QMenu::item:selected { background-color: #003300; }
            QCheckBox { color: #00ff00; }
            QLabel { color: #00ff00; }
            QGroupBox { color: #00ff00; border: 1px solid #00ff00; }
        ''',
        'Midnight': '''
            QMainWindow, QWidget { background-color: #1a1a2e; color: #eaeaea; }
            QTableView, QTreeView, QListView { background-color: #16213e; color: #eaeaea; alternate-background-color: #1a1a2e; }
            QTabWidget::pane { border: 1px solid #0f3460; }
            QTabBar::tab { background-color: #16213e; color: #eaeaea; padding: 8px 16px; }
            QTabBar::tab:selected { background-color: #0f3460; }
            QPushButton { background-color: #0f3460; color: #eaeaea; border: 1px solid #e94560; padding: 5px 15px; }
            QPushButton:hover { background-color: #e94560; color: #ffffff; }
            QLineEdit, QTextEdit, QPlainTextEdit { background-color: #16213e; color: #eaeaea; border: 1px solid #0f3460; }
            QComboBox { background-color: #16213e; color: #eaeaea; border: 1px solid #0f3460; }
            QMenuBar { background-color: #1a1a2e; color: #eaeaea; }
            QMenu { background-color: #1a1a2e; color: #eaeaea; }
            QMenu::item:selected { background-color: #e94560; }
            QCheckBox { color: #eaeaea; }
            QLabel { color: #eaeaea; }
            QGroupBox { color: #eaeaea; border: 1px solid #0f3460; }
        '''
    }

    # Apply theme
    theme = getattr(settings, 'general_theme', 'Default')
    if theme in themes and themes[theme]:
        mainWindow.setStyleSheet(mainWindow.styleSheet() + themes[theme])

    # Apply font settings
    font_family = getattr(settings, 'general_font_family', 'Default')
    font_size = int(getattr(settings, 'general_font_size', '10'))

    if font_family != 'Default':
        font = QtGui.QFont(font_family, font_size)
        app.setFont(font)
    elif font_size != 10:
        font = app.font()
        font.setPointSize(font_size)
        app.setFont(font)

if __name__ == "__main__":
    # Parse arguments and kick off scans if needed
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", help="Automatically launch a staged nmap against the target IP range")
    parser.add_argument("-f", "--file", help="Import nmap XML file and kick off automated attacks")
    args = parser.parse_args()

    app = QtWidgets.QApplication(sys.argv)
    myFilter = MyEventFilter()                        # to capture events
    app.installEventFilter(myFilter)
    app.setWindowIcon(QtGui.QIcon('./images/icons/logo.png'))

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    # Load base stylesheet
    try:
        qss_file = open('./ui/ninjaart.qss').read()
    except IOError:
        try:
            qss_file = open('./ui/ninjaart.qss').read()
        except IOError as e:
            print("[-] No stylesheet file found. Using default styling.")
            qss_file = ""

    MainWindow.setStyleSheet(qss_file)
    logic = Logic()                                    # Model prep (logic, db and models)
    view = View(ui, MainWindow)                        # View prep (gui)
    controller = Controller(view, logic)            # Controller prep (communication between model and view)

    # Apply theme and font settings
    applyAppearanceSettings(app, MainWindow, controller.settings)

    MainWindow.show()
    
    if args.target:
        print("[+] Target was specified.")
        controller.addHosts(args.target, True, True)

    if args.file:
        print("[+] Nmap XML file was provided.")
        controller.importNmap(args.file)        

    sys.exit(app.exec_())
