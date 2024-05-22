install:
	python3 -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt

# запуск приложения
run:
	venv/bin/python mainwindow_ui.py

# Запуск тестов с использованием pytest
test:
	venv/bin/pytest

# Удаление виртуального окружения
clean:
	rm -rf venv

# Запуск установки зависимостей и тестов
all: clean install test
