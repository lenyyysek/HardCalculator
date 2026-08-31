import sys
from math import gcd
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Калькуляторы")
        self.setFixedSize(950, 850)

        tabs = QTabWidget()
        tabs.addTab(PercentOperations(), "Процентные операции")
        tabs.addTab(GcdLcmCalc(), "НОД/НОК")
        tabs.addTab(MatrixCalculator(), "Калькулятор матриц")

        self.setCentralWidget(tabs)


class PercentOperations(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 30, 40, 40)

        title = QLabel("Калькулятор процентов")
        title.setStyleSheet("font-weight: bold; font-size: 18px; color: #32cd32;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(5)

        line1 = QFrame()
        line1.setFrameShape(QFrame.Shape.HLine)
        line1.setStyleSheet("background-color: rgba(0, 0, 0, 0.15); max-height: 2px;")
        layout.addWidget(line1)

        layout.addSpacing(20)

        self.operation_combo = QComboBox()
        self.operation_combo.addItems([
            "Нахождение процента от числа",
            "Сколько процентов составляет число X от числа Y",
            "Прибавление процента к числу",
            "Вычитание процента из числа"
        ])
        self.operation_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #aaa;
                border-radius: 4px;
                padding: 6px;
                font-size: 13px;
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        self.operation_combo.currentIndexChanged.connect(self.update_labels)
        layout.addWidget(self.operation_combo)

        layout.addSpacing(30)

        input_layout = QHBoxLayout()
        input_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        input_layout.setSpacing(15)

        self.label1 = QLabel("Процент:")
        self.label1.setStyleSheet("font-size: 13px;")
        self.input1 = QLineEdit()
        self.input1.setFixedWidth(100)
        self.input1.setFixedHeight(30)
        self.input1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input1.setStyleSheet("""
            QLineEdit {
                border: 1px solid #aaa;
                border-radius: 4px;
                font-size: 13px;
                background-color: white;
            }
        """)

        self.label2 = QLabel("Число:")
        self.label2.setStyleSheet("font-size: 13px;")
        self.input2 = QLineEdit()
        self.input2.setFixedWidth(100)
        self.input2.setFixedHeight(30)
        self.input2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input2.setStyleSheet("""
            QLineEdit {
                border: 1px solid #aaa;
                border-radius: 4px;
                font-size: 13px;
                background-color: white;
            }
        """)

        input_layout.addWidget(self.label1)
        input_layout.addWidget(self.input1)
        input_layout.addWidget(self.label2)
        input_layout.addWidget(self.input2)

        layout.addLayout(input_layout)

        layout.addSpacing(40)

        self.btn = QPushButton("Рассчитать")
        self.btn.setFixedWidth(140)
        self.btn.setFixedHeight(38)
        self.btn.setStyleSheet("""
            QPushButton {
                background-color: #32cd32;
                color: white;
                font-weight: bold;
                font-size: 13px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2d6e55;
            }
        """)
        self.btn.clicked.connect(self.calc)
        layout.addWidget(self.btn, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(30)

        self.result_line = QLabel("")
        self.result_line.setStyleSheet("font-size: 13px; color: black;")
        self.result_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.result_line)

        layout.addSpacing(10)

        self.solution_widget = QWidget()
        self.solution_widget.setStyleSheet("background-color: #f0f0f0; border-radius: 5px;")
        solution_layout = QVBoxLayout(self.solution_widget)
        solution_layout.setContentsMargins(15, 10, 15, 10)

        self.solution_text = QLabel("")
        self.solution_text.setStyleSheet("font-size: 12px; color: #333; background-color: transparent;")
        self.solution_text.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.solution_text.setWordWrap(True)
        solution_layout.addWidget(self.solution_text)

        layout.addWidget(self.solution_widget)

        layout.addStretch()
        self.setLayout(layout)

        self.set_default_values()
        self.update_labels()

    def set_default_values(self):
        op = self.operation_combo.currentIndex()
        if op == 0:
            self.input1.setText("25")
            self.input2.setText("200")
        elif op == 1:
            self.input1.setText("50")
            self.input2.setText("200")
        elif op == 2:
            self.input1.setText("10")
            self.input2.setText("150")
        else:
            self.input1.setText("20")
            self.input2.setText("500")

    def update_labels(self):
        op = self.operation_combo.currentIndex()
        if op == 0:
            self.label1.setText("Сколько составляет")
            self.label2.setText("% от числа")
            self.input1.setPlaceholderText("например, 25")
            self.input2.setPlaceholderText("например, 200")
        elif op == 1:
            self.label1.setText("Число X:")
            self.label2.setText("Число Y:")
            self.input1.setPlaceholderText("например, 50")
            self.input2.setPlaceholderText("например, 200")
        elif op == 2:
            self.label1.setText("Прибавить %")
            self.label2.setText("К числу")
            self.input1.setPlaceholderText("например, 10")
            self.input2.setPlaceholderText("например, 150")
        else:
            self.label1.setText("Из числа")
            self.label2.setText("вычесть %")
            self.input1.setPlaceholderText("например, 500")
            self.input2.setPlaceholderText("например, 20")

        self.set_default_values()
        self.result_line.setText("")
        self.solution_text.setText("")

    def calc(self):
        try:
            op = self.operation_combo.currentIndex()
            val1 = float(self.input1.text())
            val2 = float(self.input2.text())

            if op == 0:
                percent = val1
                number = val2
                result = (percent / 100) * number
                self.result_line.setText(
                    f'<span style="font-size: 13px;">{percent}% от числа {number} = </span>'
                    f'<span style="color: red; font-size: 20px; font-weight: bold;">{result}</span>'
                )
                self.solution_text.setText(
                    f"Решение: {percent}% от {number} = ({percent} ÷ 100) × {number} = {percent / 100} × {number} = {result}"
                )
            elif op == 1:
                x = val1
                y = val2
                if y == 0:
                    raise ValueError("Число Y не может быть нулём")
                result = (x / y) * 100
                self.result_line.setText(
                    f'<span style="font-size: 13px;">Число {x} составляет от числа {y} </span>'
                    f'<span style="color: red; font-size: 20px; font-weight: bold;">{result}%</span>'
                )
                self.solution_text.setText(
                    f"Решение: {x} ÷ {y} × 100% = {x / y} × 100% = {result}%"
                )
            elif op == 2:
                percent = val1
                number = val2
                result = number + (number * percent / 100)
                self.result_line.setText(
                    f'<span style="font-size: 13px;">К числу {number} прибавить {percent}% = </span>'
                    f'<span style="color: red; font-size: 20px; font-weight: bold;">{result}</span>'
                )
                self.solution_text.setText(
                    f"Решение: {number} + ({number} · {percent} ÷ 100) = {number} + {number * percent / 100} = {result}"
                )
            else:
                number = val1
                percent = val2
                result = number - (number * percent / 100)
                self.result_line.setText(
                    f'<span style="font-size: 13px;">Из числа {number} вычесть {percent}% = </span>'
                    f'<span style="color: red; font-size: 20px; font-weight: bold;">{result}</span>'
                )
                self.solution_text.setText(
                    f"Решение: {number} - ({number} · {percent} ÷ 100) = {number} - {number * percent / 100} = {result}"
                )

            self.result_line.setTextFormat(Qt.TextFormat.RichText)

        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите корректные числа!")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", str(e))


class GcdLcmCalc(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(40, 30, 40, 40)

        title = QLabel("Калькулятор для нахождения НОД и НОК чисел")
        title.setStyleSheet("font-weight: bold; font-size: 15px; color: #32cd32;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(5)

        line1 = QFrame()
        line1.setFrameShape(QFrame.Shape.HLine)
        line1.setStyleSheet("background-color: rgba(0, 0, 0, 0.15); max-height: 2px;")
        layout.addWidget(line1)

        layout.addSpacing(15)

        label_choice = QLabel("Выберите количество чисел, для которых требуется найти НОД и НОК:")
        label_choice.setStyleSheet("font-size: 12px; color: black; font-weight: bold;")
        label_choice.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label_choice)

        layout.addSpacing(5)

        self.radio_2 = QRadioButton("2 числа")
        self.radio_3 = QRadioButton("3 числа")
        self.radio_4 = QRadioButton("4 числа")
        self.radio_3.setChecked(True)

        for rb in [self.radio_2, self.radio_3, self.radio_4]:
            rb.setStyleSheet("""
                font-size: 12px;
                color: #1E90FF;
                font-weight: bold;
                border-bottom: 2px dotted #1E90FF;
                padding-bottom: 3px;
                margin: 5px;
            """)

        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.radio_2)
        radio_layout.addWidget(self.radio_3)
        radio_layout.addWidget(self.radio_4)
        radio_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        radio_layout.setSpacing(25)
        layout.addLayout(radio_layout)

        self.radio_2.toggled.connect(self.update_inputs)
        self.radio_3.toggled.connect(self.update_inputs)
        self.radio_4.toggled.connect(self.update_inputs)

        layout.addSpacing(20)

        self.inputs_layout = QHBoxLayout()
        self.inputs_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.inputs_layout.setSpacing(20)
        self.inputs = []
        self.input_widgets = []
        layout.addLayout(self.inputs_layout)

        layout.addSpacing(20)

        self.btn = QPushButton("Вычислить")
        self.btn.setFixedWidth(130)
        self.btn.setFixedHeight(35)
        self.btn.setStyleSheet("""
            QPushButton {
                background-color: #32cd32;
                color: white;
                font-weight: bold;
                font-size: 12px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2d6e55;
            }
        """)
        self.btn.clicked.connect(self.calc)
        layout.addWidget(self.btn, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(20)

        line2 = QFrame()
        line2.setFrameShape(QFrame.Shape.HLine)
        line2.setStyleSheet("background-color: rgba(0, 0, 0, 0.15); max-height: 2px;")
        layout.addWidget(line2)

        layout.addSpacing(15)

        self.result_label = QLabel("Ответ:")
        self.result_label.setStyleSheet("font-weight: bold; font-size: 13px; color: black;")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.result_label)

        layout.addSpacing(5)

        self.result = QLabel("")
        self.result.setStyleSheet("font-weight: bold; font-size: 12px; color: black;")
        self.result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result.setWordWrap(True)
        layout.addWidget(self.result)

        layout.addStretch()
        self.setLayout(layout)
        self.update_inputs()

    def update_inputs(self):
        for i in reversed(range(self.inputs_layout.count())):
            widget = self.inputs_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        for container in self.input_widgets:
            container.deleteLater()
        self.input_widgets.clear()
        self.inputs.clear()

        if self.radio_2.isChecked():
            count = 2
        elif self.radio_3.isChecked():
            count = 3
        else:
            count = 4

        default_values = [45, 15, 40, 20]

        for i in range(count):
            container = QWidget()
            container_layout = QVBoxLayout(container)
            container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            container_layout.setSpacing(8)

            label = QLabel(f"Число {i + 1}")
            label.setStyleSheet("font-weight: bold; font-size: 11px; color: #333;")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            spin = QSpinBox()
            spin.setRange(1, 99999)
            spin.setValue(default_values[i])
            spin.setFixedWidth(100)
            spin.setFixedHeight(35)
            spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
            spin.setStyleSheet("""
                QSpinBox {
                    border: 1px solid #aaa;
                    border-radius: 4px;
                    font-size: 13px;
                    background-color: white;
                }
                QSpinBox::up-button, QSpinBox::down-button {
                    width: 20px;
                }
            """)

            container_layout.addWidget(label)
            container_layout.addWidget(spin)

            self.inputs.append(spin)
            self.input_widgets.append(container)
            self.inputs_layout.addWidget(container)

    def get_numbers(self):
        return [spin.value() for spin in self.inputs]

    def calc(self):
        nums = self.get_numbers()

        g = nums[0]
        for n in nums[1:]:
            g = gcd(g, n)

        l = nums[0]
        for n in nums[1:]:
            l = l * n // gcd(l, n)

        nums_str = "; ".join(map(str, nums))

        self.result.setText(
            f"Наибольший общий делитель НОД (<span style='color: #1E90FF; font-weight: bold;'>{nums_str}</span>) = {g}<br><br>"
            f"Наименьшее общее кратное НОК (<span style='color: #1E90FF; font-weight: bold;'>{nums_str}</span>) = {l}"
        )
        self.result.setTextFormat(Qt.TextFormat.RichText)


class MatrixCalculator(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(40, 30, 40, 40)

        title = QLabel("Калькулятор матриц")
        title.setStyleSheet("font-weight: bold; font-size: 18px; color: #32cd32;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(5)

        line1 = QFrame()
        line1.setFrameShape(QFrame.Shape.HLine)
        line1.setStyleSheet("background-color: rgba(0, 0, 0, 0.15); max-height: 2px;")
        layout.addWidget(line1)

        layout.addSpacing(20)

        # Верхняя часть: Матрица A, операция, Матрица B
        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_layout.setSpacing(20)

        # Матрица A
        a_container = QWidget()
        a_container_layout = QVBoxLayout(a_container)
        a_container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        a_label = QLabel("Матрица A")
        a_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #333;")
        a_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        a_container_layout.addWidget(a_label)

        self.a_size_label = QLabel("(3×3)")
        self.a_size_label.setStyleSheet("font-size: 11px; color: #666;")
        self.a_size_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        a_container_layout.addWidget(self.a_size_label)

        self.a_grid_widget = QWidget()
        self.a_grid_layout = QGridLayout(self.a_grid_widget)
        self.a_grid_layout.setSpacing(5)
        a_container_layout.addWidget(self.a_grid_widget)
        self.a_cells = []
        top_layout.addWidget(a_container)

        # ComboBox с операцией
        op_container = QWidget()
        op_layout = QVBoxLayout(op_container)
        op_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.operation_combo = QComboBox()
        self.operation_combo.addItems(["+", "−", "×"])
        self.operation_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #aaa;
                border-radius: 4px;
                padding: 8px;
                font-size: 20px;
                font-weight: bold;
                background-color: white;
                min-width: 70px;
            }
        """)
        op_layout.addWidget(self.operation_combo)
        top_layout.addWidget(op_container)

        # Матрица B
        b_container = QWidget()
        b_container_layout = QVBoxLayout(b_container)
        b_container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        b_label = QLabel("Матрица B")
        b_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #333;")
        b_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        b_container_layout.addWidget(b_label)

        self.b_size_label = QLabel("(3×3)")
        self.b_size_label.setStyleSheet("font-size: 11px; color: #666;")
        self.b_size_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        b_container_layout.addWidget(self.b_size_label)

        self.b_grid_widget = QWidget()
        self.b_grid_layout = QGridLayout(self.b_grid_widget)
        self.b_grid_layout.setSpacing(5)
        b_container_layout.addWidget(self.b_grid_widget)
        self.b_cells = []
        top_layout.addWidget(b_container)

        layout.addLayout(top_layout)

        layout.addSpacing(20)

        # Блок выбора размера матриц
        size_layout = QHBoxLayout()
        size_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        size_layout.setSpacing(40)

        # Размер матрицы A
        a_size_group = QGroupBox("Размер Матрицы A")
        a_size_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #aaa;
                border-radius: 5px;
                margin-top: 10px;
                font-size: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        a_size_inner = QVBoxLayout()
        a_size_inner.setSpacing(8)

        rows_layout_a = QHBoxLayout()
        rows_layout_a.addWidget(QLabel("кол-во строк:"))
        self.a_rows_combo = QComboBox()
        self.a_rows_combo.addItems([str(i) for i in range(1, 6)])
        self.a_rows_combo.setCurrentText("3")
        self.a_rows_combo.setFixedWidth(60)
        self.a_rows_combo.currentTextChanged.connect(self.update_matrix_a_size)
        rows_layout_a.addWidget(self.a_rows_combo)
        a_size_inner.addLayout(rows_layout_a)

        cols_layout_a = QHBoxLayout()
        cols_layout_a.addWidget(QLabel("кол-во столбцов:"))
        self.a_cols_combo = QComboBox()
        self.a_cols_combo.addItems([str(i) for i in range(1, 6)])
        self.a_cols_combo.setCurrentText("3")
        self.a_cols_combo.setFixedWidth(60)
        self.a_cols_combo.currentTextChanged.connect(self.update_matrix_a_size)
        cols_layout_a.addWidget(self.a_cols_combo)
        a_size_inner.addLayout(cols_layout_a)

        a_size_group.setLayout(a_size_inner)
        size_layout.addWidget(a_size_group)

        # Размер матрицы B
        b_size_group = QGroupBox("Размер Матрицы B")
        b_size_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #aaa;
                border-radius: 5px;
                margin-top: 10px;
                font-size: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        b_size_inner = QVBoxLayout()
        b_size_inner.setSpacing(8)

        rows_layout_b = QHBoxLayout()
        rows_layout_b.addWidget(QLabel("кол-во строк:"))
        self.b_rows_combo = QComboBox()
        self.b_rows_combo.addItems([str(i) for i in range(1, 6)])
        self.b_rows_combo.setCurrentText("3")
        self.b_rows_combo.setFixedWidth(60)
        self.b_rows_combo.currentTextChanged.connect(self.update_matrix_b_size)
        rows_layout_b.addWidget(self.b_rows_combo)
        b_size_inner.addLayout(rows_layout_b)

        cols_layout_b = QHBoxLayout()
        cols_layout_b.addWidget(QLabel("кол-во столбцов:"))
        self.b_cols_combo = QComboBox()
        self.b_cols_combo.addItems([str(i) for i in range(1, 6)])
        self.b_cols_combo.setCurrentText("3")
        self.b_cols_combo.setFixedWidth(60)
        self.b_cols_combo.currentTextChanged.connect(self.update_matrix_b_size)
        cols_layout_b.addWidget(self.b_cols_combo)
        b_size_inner.addLayout(cols_layout_b)

        b_size_group.setLayout(b_size_inner)
        size_layout.addWidget(b_size_group)

        layout.addLayout(size_layout)

        layout.addSpacing(20)

        self.btn = QPushButton("Рассчитать")
        self.btn.setFixedWidth(140)
        self.btn.setFixedHeight(38)
        self.btn.setStyleSheet("""
            QPushButton {
                background-color: #32cd32;
                color: white;
                font-weight: bold;
                font-size: 13px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2d6e55;
            }
        """)
        self.btn.clicked.connect(self.calc)
        layout.addWidget(self.btn, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(20)

        line2 = QFrame()
        line2.setFrameShape(QFrame.Shape.HLine)
        line2.setStyleSheet("background-color: rgba(0, 0, 0, 0.15); max-height: 2px;")
        layout.addWidget(line2)

        layout.addSpacing(15)

        # Результат
        result_header_layout = QHBoxLayout()
        result_header_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.result_title = QLabel("Результат:")
        self.result_title.setStyleSheet("font-weight: bold; font-size: 14px; color: red;")
        result_header_layout.addWidget(self.result_title)

        self.operation_text = QLabel("")
        self.operation_text.setStyleSheet("font-size: 12px; color: black;")
        result_header_layout.addWidget(self.operation_text)

        result_header_layout.addStretch()
        layout.addLayout(result_header_layout)

        layout.addSpacing(10)

        self.result_widget = QWidget()
        self.result_widget.setStyleSheet("background-color: #f0f0f0; border-radius: 5px;")
        result_layout = QVBoxLayout(self.result_widget)
        result_layout.setContentsMargins(15, 10, 15, 10)

        self.result_matrix_title = QLabel("")
        self.result_matrix_title.setStyleSheet(
            "font-weight: bold; font-size: 13px; color: #333; background-color: transparent;")
        self.result_matrix_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        result_layout.addWidget(self.result_matrix_title)

        # Контейнер для матрицы со скобками
        matrix_container = QHBoxLayout()
        matrix_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        matrix_container.setSpacing(5)

        # Левая скобка
        self.left_bracket = QLabel("[")
        self.left_bracket.setStyleSheet("font-size: 64px; font-family: monospace;")
        self.left_bracket.setAlignment(Qt.AlignmentFlag.AlignCenter)
        matrix_container.addWidget(self.left_bracket)

        # Сама матрица
        self.result_matrix_label = QLabel("")
        self.result_matrix_label.setStyleSheet(
            "font-size: 13px; color: #333; background-color: transparent; font-family: monospace;")
        self.result_matrix_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        matrix_container.addWidget(self.result_matrix_label)

        # Правая скобка
        self.right_bracket = QLabel("]")
        self.right_bracket.setStyleSheet("font-size: 64px; font-family: monospace;")
        self.right_bracket.setAlignment(Qt.AlignmentFlag.AlignCenter)
        matrix_container.addWidget(self.right_bracket)

        result_layout.addLayout(matrix_container)

        layout.addWidget(self.result_widget)

        layout.addStretch()
        self.setLayout(layout)

        self.update_matrix_a_size()
        self.update_matrix_b_size()

    def update_matrix_a_size(self):
        for i in reversed(range(self.a_grid_layout.count())):
            self.a_grid_layout.itemAt(i).widget().deleteLater()
        self.a_cells.clear()

        rows = int(self.a_rows_combo.currentText())
        cols = int(self.a_cols_combo.currentText())

        self.a_size_label.setText(f"({rows}×{cols})")

        default_a = [[0, 5, 0], [3, 9, -1], [0, 8, 0]]

        for i in range(rows):
            row_cells = []
            for j in range(cols):
                cell = QLineEdit()
                cell.setFixedWidth(60)
                cell.setFixedHeight(30)
                cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                cell.setStyleSheet("""
                    QLineEdit {
                        border: 1px solid #aaa;
                        border-radius: 4px;
                        font-size: 12px;
                        background-color: white;
                    }
                """)
                if i < len(default_a) and j < len(default_a[i]):
                    cell.setText(str(default_a[i][j]))
                else:
                    cell.setText("0")
                self.a_grid_layout.addWidget(cell, i, j)
                row_cells.append(cell)
            self.a_cells.append(row_cells)

    def update_matrix_b_size(self):
        for i in reversed(range(self.b_grid_layout.count())):
            self.b_grid_layout.itemAt(i).widget().deleteLater()
        self.b_cells.clear()

        rows = int(self.b_rows_combo.currentText())
        cols = int(self.b_cols_combo.currentText())

        self.b_size_label.setText(f"({rows}×{cols})")

        default_b = [[8, 0, 24], [0, 12, 0], [1, 0, 4]]

        for i in range(rows):
            row_cells = []
            for j in range(cols):
                cell = QLineEdit()
                cell.setFixedWidth(60)
                cell.setFixedHeight(30)
                cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                cell.setStyleSheet("""
                    QLineEdit {
                        border: 1px solid #aaa;
                        border-radius: 4px;
                        font-size: 12px;
                        background-color: white;
                    }
                """)
                if i < len(default_b) and j < len(default_b[i]):
                    cell.setText(str(default_b[i][j]))
                else:
                    cell.setText("0")
                self.b_grid_layout.addWidget(cell, i, j)
                row_cells.append(cell)
            self.b_cells.append(row_cells)

    def get_matrix(self, cells):
        matrix = []
        for i in range(len(cells)):
            row = []
            for j in range(len(cells[i])):
                try:
                    val = float(cells[i][j].text())
                    row.append(val)
                except ValueError:
                    row.append(0.0)
            matrix.append(row)
        return matrix

    def format_matrix_text(self, matrix):
        """Форматирует матрицу в виде текста с выравниванием"""
        if not matrix:
            return "Пустая матрица"

        rows = len(matrix)
        cols = len(matrix[0]) if rows > 0 else 0

        str_matrix = []
        max_width = 0
        for i in range(rows):
            row = []
            for j in range(cols):
                val = matrix[i][j]
                if val == int(val):
                    s = str(int(val))
                else:
                    s = f"{val:.4g}"
                row.append(s)
                max_width = max(max_width, len(s))
            str_matrix.append(row)

        lines = []
        for i in range(rows):
            row_str = "  ".join(s.rjust(max_width) for s in str_matrix[i])
            lines.append(row_str)

        return "\n".join(lines)

    def calc(self):
        try:
            matrix_a = self.get_matrix(self.a_cells)
            matrix_b = self.get_matrix(self.b_cells)

            if not matrix_a or not matrix_b:
                self.result_matrix_label.setText("Ошибка: Заполните матрицы!")
                return

            rows_a, cols_a = len(matrix_a), len(matrix_a[0])
            rows_b, cols_b = len(matrix_b), len(matrix_b[0])

            operation = self.operation_combo.currentText()
            result_matrix = None
            op_symbol = operation

            if operation == "+":
                if rows_a != rows_b or cols_a != cols_b:
                    self.result_matrix_label.setText(
                        f"Ошибка: Для сложения размеры матриц должны совпадать!\n"
                        f"Матрица A: {rows_a}×{cols_a}, Матрица B: {rows_b}×{cols_b}"
                    )
                    return
                result_matrix = [[matrix_a[i][j] + matrix_b[i][j] for j in range(cols_a)] for i in range(rows_a)]

            elif operation == "−":
                if rows_a != rows_b or cols_a != cols_b:
                    self.result_matrix_label.setText(
                        f"Ошибка: Для вычитания размеры матриц должны совпадать!\n"
                        f"Матрица A: {rows_a}×{cols_a}, Матрица B: {rows_b}×{cols_b}"
                    )
                    return
                result_matrix = [[matrix_a[i][j] - matrix_b[i][j] for j in range(cols_a)] for i in range(rows_a)]

            elif operation == "×":
                if cols_a != rows_b:
                    self.result_matrix_label.setText(
                        f"Ошибка: Для умножения число столбцов A должно равняться числу строк B!\n"
                        f"Матрица A: {rows_a}×{cols_a}, Матрица B: {rows_b}×{cols_b}"
                    )
                    return
                result_matrix = [[0 for _ in range(cols_b)] for _ in range(rows_a)]
                for i in range(rows_a):
                    for j in range(cols_b):
                        for k in range(cols_a):
                            result_matrix[i][j] += matrix_a[i][k] * matrix_b[k][j]

            if result_matrix:
                rows_res = len(result_matrix)
                cols_res = len(result_matrix[0])
                self.operation_text.setText(f"  Матрица A {op_symbol} Матрица B = Матрица C")
                self.result_matrix_title.setText(f"Матрица C ({rows_res}×{cols_res})")
                self.result_matrix_label.setText(self.format_matrix_text(result_matrix))
            else:
                self.result_matrix_label.setText("Ошибка при вычислении!")

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())