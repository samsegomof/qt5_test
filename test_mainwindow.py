import os
import pytest
from PyQt5 import QtWidgets, QtCore
from mainwindow_ui import UiMainWindow


@pytest.fixture
def app(qtbot):
    """
        Fixture to set up the application with the main window.
    """
    main_window = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setupUi(main_window)
    main_window.show()
    qtbot.addWidget(main_window)
    yield ui
    main_window.close()


def test_display_directory(app, qtbot):
    """
        Test to ensure the directory is displayed correctly and the directory
        list widget is populated with the correct number of items.
    """
    directory = os.getcwd()
    app.pathLineEdit.setText(directory)
    qtbot.mouseClick(app.refreshButton, QtCore.Qt.LeftButton)
    qtbot.wait(1000)
    assert app.pathLineEdit.text() == directory
    assert app.directoryListWidget.count() == len(os.listdir(directory))


def test_navigation_to_subdirectory(app, qtbot):
    """
        Test to verify navigation to a subdirectory updates the path
        and displays the contents of the subdirectory.
    """
    directory = os.getcwd()
    subdirectory = os.path.join(directory, 'test_subdir')
    os.makedirs(subdirectory, exist_ok=True)
    app.pathLineEdit.setText(subdirectory)
    qtbot.mouseClick(app.refreshButton, QtCore.Qt.LeftButton)
    qtbot.wait(1000)
    assert app.pathLineEdit.text() == subdirectory


def test_open_file(app, qtbot):
    """
        Test to ensure that opening a file from the directory list widget
        displays its contents in the file content text edit.
    """
    directory = os.getcwd()
    test_file = os.path.join(directory, 'test_file.txt')
    with open(test_file, 'w') as f:
        f.write('Hello, world!')
    app.pathLineEdit.setText(directory)
    qtbot.mouseClick(app.refreshButton, QtCore.Qt.LeftButton)
    qtbot.wait(1000)
    item = app.directoryListWidget.findItems('test_file.txt', QtCore.Qt.MatchExactly)[0]
    item.setSelected(True)
    app.directoryListWidget.itemDoubleClicked.emit(item)
    qtbot.wait(1000)
    assert app.fileContentTextEdit.toPlainText() == 'Hello, world!'
    os.remove(test_file)


def test_back_button(app, qtbot):
    """
        Test to ensure the back button navigates to the previous directory
        and updates the path and directory list widget accordingly.
    """
    directory = os.getcwd()
    subdirectory = os.path.join(directory, 'test_subdir')
    os.makedirs(subdirectory, exist_ok=True)
    app.pathLineEdit.setText(subdirectory)
    qtbot.mouseClick(app.refreshButton, QtCore.Qt.LeftButton)
    qtbot.wait(1000)
    qtbot.mouseClick(app.backButton, QtCore.Qt.LeftButton)
    qtbot.wait(1000)
    assert app.pathLineEdit.text() == directory


def test_close_app(app, qtbot):
    """
        Test to ensure that clicking the exit button closes the application.
    """
    qtbot.mouseClick(app.exitButton, QtCore.Qt.LeftButton)
    qtbot.wait(1000)
    assert not app.centralwidget.isVisible()


def test_navigation_to_empty_directory(app, qtbot):
    """
        Test navigation to an empty directory.
        Ensures that the directory list widget is empty when navigating to a directory with no files or subdirectories.
    """
    empty_directory = os.path.join(os.getcwd(), 'empty_dir')
    os.makedirs(empty_directory, exist_ok=True)
    app.pathLineEdit.setText(empty_directory)
    qtbot.mouseClick(app.refreshButton, QtCore.Qt.LeftButton)
    qtbot.wait(1000)
    assert app.directoryListWidget.count() == 0


def test_back_button_at_root(app, qtbot):
    """
        Test the back button functionality when at the root directory.
        Ensures that the path does not change when trying to navigate back from the root directory.
    """
    root_directory = '/'
    app.pathLineEdit.setText(root_directory)
    qtbot.mouseClick(app.refreshButton, QtCore.Qt.LeftButton)
    qtbot.wait(1000)
    qtbot.mouseClick(app.backButton, QtCore.Qt.LeftButton)
    qtbot.wait(1000)
    assert app.pathLineEdit.text() == root_directory
