# TALOS TERMINAL

[![Python 3.6](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380//)
[![License: GPL](https://img.shields.io/badge/License-GPL-yellow.svg)](https://opensource.org/licenses/GPL-3.0)
[![PyPI version](https://badge.fury.io/py/rich.svg)](https://badge.fury.io/py/rich)

<!---![Logo](https://github.com/straniks/Talos_Ver_0.1/blob/main/images/talos.png)-->


Данный терминал разрабатывается на Python для анализа и торговли на крипто биржах для ОС Linux.

Код терминала базируется на REST API BINANCE [Binance Futures public API](https://binance-docs.github.io/apidocs/futures/en/)

- Используемые APIs из Binance:
	- USDT-M Futures `/fapi/*`

---

### Установка и использование

На момент разработки, терминал не требует какой либо индивидуальной установки. Достаточно склонировать репазиторий и запустить 
```bash
./main.py
```

---

### Требования для работы кода

Для успешного выполнения кода, требует наличией следующих Python библиотек

- [Binance futures connector](https://github.com/binance/binance-futures-connector-python) lightweight library that works as a connector to [Binance Futures public API](https://binance-docs.github.io/apidocs/futures/en/)
- [Rich](https://github.com/Textualize/rich) library for text and beautiful formatting in the terminal
- [Colorama](https://github.com/tartley/colorama) library for producing colored terminal text and cursor positioning
- [PrettyTable](https://github.com/jazzband/prettytable) library for easily displaying tabular data in a visually appealing ASCII table format
- [Art](https://github.com/sepandhaghighi/art) library for text converting to ASCII art fancy
- [Matplotlib](https://github.com/matplotlib/matplotlib) library for creating static, animated, and interactive visualizations

### Установка библиотек через PIP

```bash
pip install binance-futures-connector
pip install rich
pip install colorama
pip install prettytable
pip install art
pip install matplotlib
```
---

### Текущие возможности
- На текущем этапе разработки, терминал выполняет следующие функции:
	- Подключение к бирже;
	- Создание дампа тикеров;
	- Сбор информации по тикеру, таймфрейму;
	- Запись собранной информации в текстовый файл;
	- Генерация графиков на основе собранных данных с последующим сохранением;

### План лист
- Планируется добавить GUI
- Вывод Live Chart инструмента
- Вывод графиков на основе собранных данных в виджет GUI
- Добавление формул для пересчета данных
- Сохранение собранных данных в exel таблицу с автоматическим добавлением формул для пересчета
- Добавление панели для торговли
- Разделения потокв(Получения данных с одной биржи, а торговля на другой)
- Создание бинарных файлов, для упрощения установки и работы терминала

---

![Features](https://github.com/straniks/Talos_Ver_0.1/blob/main/images/main.svg)

---

## License
GNU General Public License (GPL-3.0)
