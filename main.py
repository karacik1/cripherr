# -*- coding: utf-8 -*-
import tkinter as tk
from importlib.resources import open_text
from random import Random
from time import process_time_ns
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import example

from tksheet import Sheet
import random
from tkinter.messagebox import showwarning
import numpy as np
import math
# что бы массив отображался без срезов

np.set_printoptions(threshold=np.inf, linewidth=np.nan)

class MainApp:
    def __init__(self, root):
        self.root = root

        self.listFrame = tk.Frame(root)
        self.listFrame.pack(side='left', fill='y')

        # создает контейнер а в нем inf frame чтобы добавить scrollbar
        container = ttk.Frame(root)
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.infFrame = ttk.Frame(canvas)

        self.infFrame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window= self.infFrame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)
        container.pack(side='right', fill='both', expand=True)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


        OpeningWindow(self.infFrame)

        list_of_coders = [["Шифр Цезаря"], ["Решетка Кардано"],['Скитала Шифр'],['Шифр Хилла'], ["Информация по проекту"]]
        self.listbox = tk.Listbox(self.listFrame, height=30, width=30)
        for coder in list_of_coders:
            self.listbox.insert(END, coder[0])
        self.listbox.pack(fill='y',side='top')

        self.listbox.bind('<<ListboxSelect>>', self.select_coder)

    def select_coder(self, event):
        selection = event.widget.curselection()
        if not selection:
            return
        index = selection[0]

        # Очистить infFrame перед добавлением нового контента
        for widget in self.infFrame.winfo_children():
            widget.destroy()

        if index == 0:
            CausersCipher(self.infFrame)
        elif index == 1:
            CardanosGrid(self.infFrame)
        elif index == 2:
            SkitalaController(self.infFrame)
        elif index == 3:
            HillController(self.infFrame)
        else:
            OpeningWindow(self.infFrame)

class ListOfCoders(MainApp):
    # общие переменные(словари)
    LIST_OF_LETTER = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м',
                           'n', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы',
                           'ь', 'э', 'ю', 'я']
    def __init__(self, parent):
        self.parent_frame = parent
        test = tk.Label(self.infFrame, text="WORKS!!!!")
        test.grid(row=0, column=1)



    # здесь общие функции
    # def change_filling(self, filling,frame, is_created=True):
    #     if is_created:
    #         self.matrix.destroy()
    #
    #     self.matrix = Sheet(frame,
    #                         data=filling,
    #                         show_header=False,
    #                         show_x_scrollbar=False,
    #                         show_y_scrollbar=False,
    #                         show_row_index=False,
    #                         column_width=25,
    #                         row_width=25,
    #                         width=25 * len(filling[0]),
    #                         height=26 * (len(filling)),
    #                         empty_horizontal=0,
    #                         empty_vertical=0)
    #     self.matrix.hide("y_scrollbar")
        # self.matrix.grid(row=2, column=0, rowspan=3) в скитале

class CausersCipher(ListOfCoders):
    def __init__(self, parent):
        self.infFrame = parent
        # super().__init__(parent)



        ttk.Label(self.infFrame, text="Шифр Цезаря").pack()

        # историческая справка
        history_inf = ttk.Label(self.infFrame, text="Шифр Цезаря, также известный как шифр сдвига или код Цезаря"
                                               " — разновидность шифра подстановки, в котором каждый символ в"
                                               " открытом тексте заменяется символом, находящимся на некотором "
                                               "постоянном числе позиций левее или правее него в алфавите.",
                                wraplength=400)
        history_inf.pack()

        # ввод сдвига текста
        self.shiftNumber = IntVar()

        # нулевое значение для исправление бага
        self.value = 0

        enter_num_of_shift = ttk.Entry(self.infFrame, textvariable=self.shiftNumber)
        enter_num_of_shift.pack()

        button_numb = ttk.Button(self.infFrame, text='Ввести значение сдвига', command=self.save_num)
        button_numb.pack()

        # алфавит для таблицы и создание таблицы
        self.original_alphabet = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П',
                                  'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']
        self.codered_alphabet = self.original_alphabet.copy()
        self.alphabet = ttk.Treeview(self.infFrame, columns=self.original_alphabet, show="", height=2)
        self.alphabet.pack(expand=0)
        self.alphabet.insert("", END, values=self.original_alphabet)
        self.alphabet.insert("", END, values=self.codered_alphabet)

        # коррекция ширины таблицы
        for col in self.original_alphabet:
            self.alphabet.column(col, width=20)

        # создание поля для открытого текста с базовым текстом
        self.open_text = ("Жабы — это земноводные с широким телом, короткими лапами и сухой, бугристой кожей, "
                          "предпочитающие сухие места и ведущие ночной образ жизни, питаясь насекомыми и червями, "
                          "тем самым принося пользу садам и огородам. Они отличаются от лягушек более «грузным» видом, "
                          "передвигаются в основном шагом, а не прыжками, и в период размножения откладывают икру "
                          "длинными шнурами, а не в виде комков, как лягушки, а их кожа выделяет защитный, хоть и не "
                          "опасный для человека, яд.При данном сдвигает зашифрованный текст будет выглядеть:")
        self.label_of_open_text = Text(self.infFrame, height=12, wrap='word')
        self.label_of_open_text.insert(1.1, self.open_text)
        self.label_of_open_text.pack()

        self.translate_text = ttk.Button(self.infFrame, text="Конвертировать", command=self.coder)
        self.translate_text.pack()

        # создание поля для закрытого текста с базовым текстом
        self.closed_text = ""
        self.label_of_closed_text = Text(self.infFrame, height=12)
        self.label_of_closed_text.pack()

    # шифровщик
    def coder(self):
        self.closed_text = ""
        full_original_alphabet = ['А', 'а', 'Б', 'б', 'В', 'в', 'Г', 'г', 'Д', 'д', 'Е', 'е', 'Ё', 'ё', 'Ж', 'ж', 'З',
                                  'з', 'И', 'и', 'Й', 'й', 'К', 'к', 'Л', 'л', 'М', 'м', 'Н', 'н', 'О', 'о', 'П', 'п',
                                  'Р', 'р',  'С', 'с', 'Т', 'т', 'У', 'у', 'Ф', 'ф', 'Х', 'х', 'Ц', 'ц', 'Ч', 'ч', 'Ш',
                                  'ш', 'Щ', 'щ', 'Ъ', 'ъ', 'Ы', 'ы', 'Ь', 'ь', 'Э', 'э', 'Ю', 'ю', 'Я', 'я']
        codered_alphabet = full_original_alphabet[self.value*2:] + full_original_alphabet[:self.value*2]
        self.open_text = self.label_of_open_text.get(1.0, END)
        for i in self.label_of_open_text.get(1.0, END):

            if i in full_original_alphabet:
                self.closed_text += codered_alphabet[full_original_alphabet.index(i)]
            else:
                self.closed_text += i
        self.label_of_closed_text.delete(1.0, END)
        self.label_of_closed_text.insert(1.0, self.closed_text)

    # дешифратор. вероятно нужно отрисовать еще одну кнопку для дешифровки. или рассмотреть возможность с той же
    # кнопкой
    def decoder(self):
        pass

    # обновление данных таблицы ///попробовать сделать через конфигуратор обновление данных
    def draw_shift(self):
        self.alphabet.insert("", END, values=self.codered_alphabet)
        self.alphabet.delete(self.alphabet.get_children()[1])

    # отрисовка таблицы со сдвигом сделать обработку ошибок от букв(обработка событий?)
    def save_num(self):
        self.value = self.shiftNumber.get() % 33
        self.codered_alphabet = self.original_alphabet[self.value:]+self.original_alphabet[:self.value]
        self.draw_shift()

class CardanosGrid(ListOfCoders):
    def __init__(self, parent):
        self.infFrame = parent
        super().__init__(self.infFrame)

        LIST_OF_MATRIX_SIZES = ['2', '4', '6', '8']

        self.LIST_OF_LETTER = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м',
                               'n', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы',
                               'ь', 'э', 'ю', 'я']
        # историческая справка
        ttk.Label(self.infFrame, text="Решётка Кардано").grid(column=0, row=0)


        self.size_of_key = StringVar(value=LIST_OF_MATRIX_SIZES[0])

        history_inf = ttk.Label(self.infFrame, text="Шифр Цезаря, также известный как шифр сдвига или код Цезаря"
                                               " — разновидность шифра подстановки, в котором каждый символ в"
                                               " открытом тексте заменяется символом, находящимся на некотором "
                                               "постоянном числе позиций левее или правее него в алфавите.",
                                wraplength=400)
        history_inf.grid(column=0, row=1)

        # создание фрейма под создание ключа и ввод текста
        self.frame_for_key_generation = tk.Frame(self.infFrame)
        self.frame_for_key_generation.grid(column=0, row=2)

        self.combobox_of_key_size = ttk.Combobox(self.frame_for_key_generation,
                                                 textvariable=self.size_of_key,
                                                 values=LIST_OF_MATRIX_SIZES)
        self.combobox_of_key_size.bind("<<ComboboxSelected>>", self.selected_size)
        self.combobox_of_key_size.grid(row=1, column=1)

        self.key_matrix = self.KeyMatrix(self.frame_for_key_generation, 0)

        self.open_text = Text(self.frame_for_key_generation, width=100, height=5)
        self.open_text.grid(row=0, column=1,columnspan=2)
        self.open_text.bind("<KeyRelease>", self.check_long_open_text)

        rotate_button = ttk.Button(self.frame_for_key_generation, text="Кодировать", command=self.get_chosen_cells)
        rotate_button.grid(row=1, column=2)

        # фрейм под примеры поворота
        self.frame_of_rotations = tk.Frame(self.infFrame)
        self.frame_of_rotations.grid(column=0, row=3)
        self.rotated_matrix1 = self.RotationMatrix(self.frame_of_rotations, 0)
        self.rotated_matrix2 = self.RotationMatrix(self.frame_of_rotations, 1)
        self.rotated_matrix3 = self.RotationMatrix(self.frame_of_rotations, 2)
        self.rotated_matrix4 = self.RotationMatrix(self.frame_of_rotations, 3)

        # фрейм под выбор режима поворота ключа
        # тут начинается результат
        self.frame_of_result = tk.Frame(self.infFrame)
        self.frame_of_result.grid(column=0, row=4)
        self.matrix_result = self.ResultMatrix(self.frame_of_result, is_pack=True)
        # возможно ширф ришльера или как его там

    def selected_size(self, event):
        self.size_of_key = int(self.combobox_of_key_size.get())


        BASE_FILLING = [[" "] * self.size_of_key] * self.size_of_key
        self.key_matrix.change_filling(BASE_FILLING)

        self.rotated_matrix1.change_filling(BASE_FILLING)
        self.rotated_matrix2.change_filling(BASE_FILLING)
        self.rotated_matrix3.change_filling(BASE_FILLING)
        self.rotated_matrix4.change_filling(BASE_FILLING)

        # передача размера матрицы в класс
        self.matrix_result.size_of_matrix = self.rotated_matrix1.size_of_matrix = self.rotated_matrix2.size_of_matrix =\
            self.rotated_matrix3.size_of_matrix = self.rotated_matrix4.size_of_matrix=self.size_of_key

        self.matrix_result.change_filling(BASE_FILLING)

        # чистит выделенные клеточки при изменении размера матрицы
        self.key_matrix.all_selected_cells = [[99, 99]]

    # смотрит на ввод символов и редактирует открытый текст
    def check_long_open_text(self, event):
        text = self.open_text.get("1.0", "end")[:-1]
        new_text = ""

        for ch in text:
            code = ord(ch)
            if (1040 <= code <= 1103) or code in [1025, 1105]:
                new_text += ch.upper()
            else:
                self.warning_massege_box()

        max_len = (len(self.key_matrix.all_selected_cells) - 1) * 4
        if len(new_text) > max_len:
            new_text = new_text[:max_len]
        self.open_text.delete("1.0", "end")
        self.open_text.insert("1.0", new_text)

    def warning_massege_box(self):
        showwarning(title="Предупреждение", message="Используйте только русские символы")



    # перекидывает список выделенных ячеек в поворотные матрицы список не сортирован НАДО СДЕЛАТЬ ЗАПРЕТ НА ПУСТОЙ МАССИВ ВОЗМОЖНО
    def get_chosen_cells(self):
        # получение длину куска открытого текста
        long_of_text_chank = len(self.key_matrix.all_selected_cells)-1

        # передача открытого текста
        current_open_text = self.open_text.get("1.0", "end")[:-1]

        # если текст короче ключа
        if long_of_text_chank*4 > len(current_open_text):
            current_open_text+=self.generator_expection(long_of_text_chank*4 -len(current_open_text))
        self.rotated_matrix1.open_text = current_open_text[:long_of_text_chank]
        self.rotated_matrix2.open_text = current_open_text[long_of_text_chank:2*long_of_text_chank]
        self.rotated_matrix3.open_text = current_open_text[2*long_of_text_chank:3*long_of_text_chank]
        self.rotated_matrix4.open_text = current_open_text[3*long_of_text_chank:]

        get_current_list_of_cells = self.key_matrix.get_selected_cells()

        cells_massive_for_1rotation = []
        cells_massive_for_2rotation = []
        cells_massive_for_3rotation = []
        cells_massive_for_4rotation = []

        # редакция поворота обратный порядок ниже ибо иначе против часовой стрелки что не надо
        for i in range(1, len(get_current_list_of_cells)):
            cells_massive_for_1rotation.append(get_current_list_of_cells[i][0])
            cells_massive_for_4rotation.append(get_current_list_of_cells[i][1])
            cells_massive_for_3rotation.append(get_current_list_of_cells[i][2])
            cells_massive_for_2rotation.append(get_current_list_of_cells[i][3])

        self.rotated_matrix1.set_selected_cells(cells_massive_for_1rotation)
        self.rotated_matrix2.set_selected_cells(cells_massive_for_2rotation)
        self.rotated_matrix3.set_selected_cells(cells_massive_for_3rotation)
        self.rotated_matrix4.set_selected_cells(cells_massive_for_4rotation)

        self.matrix_result.get_all_rotated(cells_massive_for_1rotation,cells_massive_for_2rotation,cells_massive_for_3rotation,cells_massive_for_4rotation, current_open_text, self.LIST_OF_LETTER)

    def generator_expection(self,long):
        add=""
        for i in range(long):
            add+= random.choice(self.LIST_OF_LETTER)
        return add.upper()


    class MatrixManager:
        def __init__(self, parent_frame, place=None, is_pack=False):
            self.frame = parent_frame
            self.is_pack = is_pack
            self.place = place

            # помогает инициализировать лист кодировщиков что бы достатть нужные элементы

            self.all_selected_cells = [[99, 99]]
            self.matrix = None

            self.BASE_SIZE = 2
            self.BASE_FILLING = [[" "]*self.BASE_SIZE]*self.BASE_SIZE
            self.change_filling(self.BASE_FILLING,False)

            # отрисовка
        def place_matrix(self):
            if not self.is_pack:
                self.matrix.grid(row=0, column=self.place, padx=5, pady=5)
            else:
                self.matrix.pack()

            # изменение данных
        def change_filling(self, filling, is_created=True):
            if is_created:
                self.matrix.destroy()

            self.matrix = Sheet(self.frame,
                                data=filling,
                                show_header=False,
                                show_x_scrollbar=False,
                                show_y_scrollbar=False,
                                show_row_index=False,
                                column_width=25,
                                row_width=25,
                                width=25*len(filling),
                                height=26*(len(filling)),
                                empty_horizontal=0,
                                empty_vertical=0)
            self.matrix.hide("y_scrollbar")
            self.place_matrix()

        # сортировка координат для ключевой и поворотной
        def sort_coor(self, massive, long):
            not_same = True
            copy_of_massive = massive.copy()
            while not_same:
                for i in range(1, long):
                    if copy_of_massive[i][0] < copy_of_massive[i - 1][0]:
                        copy_of_massive[i], copy_of_massive[i - 1] = copy_of_massive[i - 1], copy_of_massive[i]

                    if copy_of_massive[i][0] == copy_of_massive[i - 1][0] and copy_of_massive[i][1] < \
                            copy_of_massive[i - 1][1]:
                        copy_of_massive[i], copy_of_massive[i - 1] = copy_of_massive[i - 1], copy_of_massive[i]
                if copy_of_massive == massive:
                    not_same = False
                else:
                    massive = copy_of_massive.copy()
            return copy_of_massive



    class KeyMatrix(MatrixManager):
        def __init__(self, parent_frame, place=None, is_pack=False):
            super().__init__(parent_frame,place, is_pack)
            self.frame = parent_frame
            self.is_pack = is_pack
            self.place = place

            # возможно больше не нужна
            self.base_list_of_blocked_cells = []

        def change_filling(self, filling, is_created=True):
            super().change_filling(filling, is_created)
            self.matrix.enable_bindings("single_select")
            self.matrix.extra_bindings([("cell_select", self.select_cell)])

        def select_cell(self, event):
            selected_cell=self.matrix.get_selected_cells()
            self.clolour_cell_manager(*selected_cell)

        # управление покрасом клеток
        def clolour_cell_manager(self, selected_cell):
            colour = self.matrix.props(row=selected_cell[0],column=selected_cell[1],key="highlight")

            if colour == {} or colour[0] in ["red", None]:
                self.colour_cells(selected_cell)
            else:
                self.decolour_cells(selected_cell)

        #отменяет покраску и разблокирует запрещенные клеточки
        def decolour_cells(self,selected_cell):
            number_of_group = self.check_selection(selected_cell)[1]
            for coor in self.all_selected_cells[number_of_group]:
                row, col = coor
                self.matrix.highlight_cells(row=row,
                                            column=col,
                                            bg=None,
                                            fg=None)
            self.all_selected_cells.pop(number_of_group)

        #красит и блокирует запрещенные клеточки
        def colour_cells(self, selected_cell):
            row, col = selected_cell

            # получаю список запрещенных клеток и перевод в баз систему исч
            blocked_cells = self.change_coordinate_sistem_to_central(row, col)
            list_of_blocked_cells = self.rotation_coordinates(*blocked_cells)
            self.base_list_of_blocked_cells = self.change_coordinate_sistem_to_base(list_of_blocked_cells)

            # создание массива с выделенными клеточками
            its_exist, number_of_group = self.check_selection(selected_cell)

            if not its_exist: self.all_selected_cells.append(self.base_list_of_blocked_cells)

            elif its_exist and self.all_selected_cells[number_of_group][0]!=selected_cell:
                blocked_cells = self.change_coordinate_sistem_to_central(row, col)
                list_of_blocked_cells = self.rotation_coordinates(*blocked_cells)
                self.base_list_of_blocked_cells = self.change_coordinate_sistem_to_base(list_of_blocked_cells)

                self.all_selected_cells[number_of_group]=self.base_list_of_blocked_cells



            # покраска ячеек
            for coor in self.all_selected_cells[number_of_group]:
                row, col = coor
                if coor == selected_cell:
                    self.matrix.highlight_cells(row=row,
                                                column=col,
                                                bg="light green",
                                                fg="white")
                else:
                    self.matrix.highlight_cells(row=row,
                                                column=col,
                                                bg="red",
                                                fg="white")

            # число для перевода из координты в левой верхной в центр
        def check_selection(self, selected_cell):
            for i in range(len(self.all_selected_cells)):
                if selected_cell in self.all_selected_cells[i]:
                    break
            else: return False, len(self.all_selected_cells)
            return True, i

        # перевод в центральную систему исчисления
        def change_coordinate_sistem_to_central(self, row, col):
            center = self.matrix.get_total_columns()//2
            if row < center:
                X = row - center
            else:
                X = row - (center - 1)

            if col < center:
                Y = -1 * (col - center)
            else:
                Y = -1 * (col - (center - 1))

            return X, Y

        # перевод в базовую систем исчисления
        def change_coordinate_sistem_to_base(self, list_of_blocked_cells):
            center = self.matrix.get_total_columns()//2
            converted_list_blocked_cells = []
            for i in list_of_blocked_cells:
                row, col = i

                if row < 0:
                    X = row + center
                else:
                    X = row + (center - 1)

                if col > 0:
                    Y = -1 * col + center
                else:
                    Y = -1 * col + (center - 1)
                converted_list_blocked_cells.append((X, Y))
            return converted_list_blocked_cells

        # список блокируемых коорд при поворот на 90 град
        # МОЖНО ЕЩЕ СДЕЛАТЬ ЕЩЕ ОТРАЖЕНИЕ
        def rotation_coordinates(self, x, y):
            list_of_extra_coor = [
                ( x, y),
                (y, -x),
                (-x, -y),
                (-y, x),

            ]
            return list_of_extra_coor

        # передает список выбранных клеточек
        def get_selected_cells(self):
            return self.all_selected_cells

    # работа с матрицами поворота
    class RotationMatrix(MatrixManager):
        def __init__(self, parent_frame, place=None, is_pack=False):
            super().__init__(parent_frame, place, is_pack)

            # выставление базового значения матрицы
            self.size_of_matrix = self.BASE_SIZE
            self.open_text = "BASE TEXT"



        # получает массив и сортирует его
        def set_selected_cells(self, selected_sells):
            self.all_selected_cells = selected_sells
            sorted_massive = super().sort_coor( self.all_selected_cells, len(self.all_selected_cells))

            self.coder(sorted_massive, self.size_of_matrix)

        # заполняет открытые окошки матрицы
        def coder(self, massive_selected_cells, long):
            filling = [["" for _ in range(long)] for _ in range(long)]
            counter_of_current_letter = 0
            for i in massive_selected_cells:
                filling[i[0]][i[1]] = self.open_text[counter_of_current_letter]
                counter_of_current_letter += 1
            self.change_filling(filling)

    class ResultMatrix(MatrixManager):
        def __init__(self, parent_frame, place=None, is_pack=False):
            super().__init__(parent_frame, place, is_pack)
            self.size_of_matrix = self.BASE_SIZE

        # обьеденяет все матрицы в одну и заполняет пустоты рандомом
        def get_all_rotated(self,matrix1, matrix2, matrix3, matrix4, text, letters):
            summ_of_matrix = []

            long = len(matrix1)
            filling = [["" for _ in range(self.size_of_matrix)] for _ in range(self.size_of_matrix)]
            matrix1 = self.sort_coor(matrix1, long)
            matrix2 = self.sort_coor(matrix2, long)
            matrix3 = self.sort_coor(matrix3, long)
            matrix4 = self.sort_coor(matrix4, long)

            summ_of_matrix.extend(matrix1)
            summ_of_matrix.extend(matrix2)
            summ_of_matrix.extend(matrix3)
            summ_of_matrix.extend(matrix4)

            number_of_letter = 0
            for coor_of_symbol in summ_of_matrix:
                row, cow = coor_of_symbol
                filling[row][cow] = text[number_of_letter]
                number_of_letter+=1

            for x in range(self.size_of_matrix):
                for y in range(self.size_of_matrix):
                    if filling[x][y] == "":
                        filling[x][y] = random.choice(letters).upper()
            super().change_filling(filling)

class SkitalaView:
    def __init__(self, parent):
        self.infFrame = parent

        self._DEFAULT_ROW = 3
        self._DEFAULT_COLUMN = 3
        self._DEFAULT_DATA = [[""]*self._DEFAULT_COLUMN for _ in range(self._DEFAULT_ROW)]

        # Виджеты
        self.matrix = None
        self.open_text_widget = None
        self.closed_text_widget = None
        self.row_number = None
        self.column_number = None

        # Callback-функции
        self.on_encrypt = None
        self.on_decrypt = None

        self.create_widgets()

    def create_widgets(self) -> None:
            self.create_header()
            self.create_text_widgets()
            self.create_controls()

            # создает базовую матрицу
            self.change_filling(self._DEFAULT_DATA)


    def create_header(self) -> None:
        ttk.Label(self.infFrame, text="Шифр Цезаря").grid(column=0, row=0, columnspan=2)

        history_inf = ttk.Label(self.infFrame, text="Шифр Цезаря, также известный как шифр сдвига или код Цезаря"
                                                    " — разновидность шифра подстановки, в котором каждый символ в"
                                                    " открытом тексте заменяется символом, находящимся на некотором "
                                                    "постоянном числе позиций левее или правее него в алфавите.",
                                wraplength=400)
        history_inf.grid(column=0, row=1, columnspan=2)

    def create_controls(self) -> None:
        table_size_text_widget = tk.Label(self.infFrame, text="Размер решетки:")
        table_size_text_widget.grid(column=1, row=3)

        size_frame = tk.Frame(self.infFrame)
        size_frame.grid(column=1, row=4)

        self.row_number = IntVar(value=self._DEFAULT_ROW)
        row_number_widget = tk.Entry(size_frame, textvariable=self.row_number, width=5)
        row_number_widget.grid(column=0, row=0)

        x_widget = tk.Label(size_frame, text='X')
        x_widget.grid(column=1, row=0)

        self.column_number = IntVar(value=self._DEFAULT_COLUMN)
        column_number_widget = tk.Entry(size_frame, textvariable=self.column_number, width=5)
        column_number_widget.grid(column=2, row=0)

        coder_button = tk.Button(size_frame, text='Кодировать', command=self._on_encrypt)
        coder_button.grid(column=3, row=0)

        decoder_button = tk.Button(size_frame, text='Декодировать', command=self._on_decrypt)
        decoder_button.grid(column=4, row=0)

    def create_text_widgets(self) -> None:
        # открытый текст
        self.open_text_widget = Text(self.infFrame, height=10, width=60)
        # self.open_text_widget.bind("<KeyRelease>", self.enter_text)
        self.open_text_widget.grid(column=1, row=2)

        # закрытый текст
        self.closed_text_widget = tk.Text(self.infFrame, height=10)
        # self.closed_text_widget.bind("<KeyRelease>", self.enter_text)
        self.closed_text_widget.grid(column=0, row=5, columnspan=2)

    def get_open_text(self) -> str:
        return self.open_text_widget.get('1.0', 'end-1c')

    def set_open_text(self, new_open_text: str) -> None:
        self.open_text_widget.delete('1.0', 'end-1c')
        self.open_text_widget.insert('1.0', new_open_text)

    def get_closed_text(self) -> str:
        return self.closed_text_widget.get('1.0', 'end-1c')

    def set_closed_text(self, new_open_text: str) -> None:
        self.closed_text_widget.delete('1.0', 'end-1c')
        self.closed_text_widget.insert('1.0', new_open_text)

    def change_filling(self, filling: list[list[str]]) -> None:
        """ Отрисовывает матрицу """
        if self.matrix is not None:
            self.matrix.destroy()

        self.matrix = Sheet(self.infFrame,
                            data=filling,
                            show_header=False,
                            show_x_scrollbar=False,
                            show_y_scrollbar=False,
                            show_row_index=False,
                            column_width=25,
                            row_width=25,
                            width=25 * len(filling[0]),
                            height=26 * (len(filling)),
                            empty_horizontal=0,
                            empty_vertical=0)
        self.matrix.hide("y_scrollbar")
        self.matrix.grid(column=0, row=2)

    def _on_encrypt(self):
        if self.on_encrypt:
            self.on_encrypt()

    def _on_decrypt(self):
        if self.on_decrypt:
            self.on_decrypt()

    def get_matrix_size(self) -> (int, int):
        return self.column_number.get(), self.row_number.get()

class SkitalaModel:
    def __init__(self):
        pass
    # шифрует
    def encrypt(self, text: str, rows: int, columns: int) -> list[list[str]]:
        """ принимает текст размеры матрицы и делает зашифрованный массив"""
        current_letter = 0
        default_data = [["0" for _ in range(columns)] for _ in range(rows)]

        for column in range(columns):
            for row in range(rows):
                if current_letter< len(text):
                    default_data[row][column] = text[current_letter]
                    current_letter+=1
                else:
                    default_data[row][column] = random.choice(ListOfCoders.LIST_OF_LETTER)

        return default_data

    def from_matrix_to_string_by_rows(self, table: list[list[str]]) -> str:
        """переводит из массива в текст для шифрования"""
        closed_text = []
        for row in range(len(table)):
            for column in range(len(table[0])):
                closed_text.append(table[row][column])
        return "".join(closed_text)

    # дешифрует текст
    def decrypt(self, text: str , rows: int, columns: int) -> list[list[str]]:
        """ принимает текст размеры матрицы и делает расшифрованный массив"""
        default_data = [["0" for _ in range(columns)] for _ in range(rows)]
        current_letter = 0
        for row in range(rows):
            for column in range(columns):
                default_data[row][column] = text[current_letter]
                current_letter+=1
        return default_data

    def from_matrix_to_string_by_columns(self, table: list[list[str]]) -> str:
        """переводит из массива в строчку для дешифровки"""
        open_text = []
        for column in range(len(table[0])):
            for row in range(len(table)):
                open_text.append(table[row][column])
        return "".join(open_text)

    def _debug_print_matrix(self, filling: list[list[str]]) -> None:
        """печатает в консоле в форме таблицы для отладки"""
        for row in filling:
            print(row)

class SkitalaController:
    def __init__(self, parent_frame):
        # подключаем шифровщик и отображение
        self.model = SkitalaModel()
        self.view = SkitalaView(parent_frame)

        # Привязываем события
        self.view.on_encrypt = self._handle_encrypt
        self.view.on_decrypt = self._handle_decrypt

        # Вставляем начальные данные
        self._initialize()

    def _initialize(self) -> None:
        """Инициализация начального состояния."""
        self.view.set_open_text("ПРИМЕРТЕКСТА")

    def _handle_encrypt(self) -> None:
        """ забирает вводимые данные и передает в шифрование, а потом возвращает """
        open_text = self.view.get_open_text()
        row, columns = self.view.get_matrix_size()

        matrix = self.model.encrypt(open_text, row, columns)
        new_closed_text = self.model.from_matrix_to_string_by_rows(matrix)

        self.view.set_closed_text(new_closed_text)
        self.view.change_filling(matrix)

    def _handle_decrypt(self) -> None:
        """ забирает вводимые данные и передает в дешифрование, а потом возвращает """
        closed_text = self.view.get_closed_text()
        row, columns = self.view.get_matrix_size()

        matrix = self.model.decrypt(closed_text, row, columns)
        new_open_text = self.model.from_matrix_to_string_by_columns(matrix)

        self.view.set_open_text(new_open_text)
        self.view.change_filling(matrix)

class HillModel:
    def __init__(self):
        self._EMPTY_CHAR = "|"
        self.alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ" + self._EMPTY_CHAR
        self._alphabet_size = len(self.alphabet)
        self._MIN_GENERATED_NUMBER = 0
        self._MAX_GENERATED_NUMBER = 10

        self.text_long = None
        self.key_long = None
        self.closed_text_long = None
        self.num_of_added_symbols = None

    def get_alphabet(self):
        return self.alphabet

    def test_input(self):
        """проверяет введенные данные на корректность"""
        pass


    def coder(self, text: str):
        """Переводит последовательность букв в последовательность
        чисел, где число - это порядковый номер буквы результат - горизонтальный массив список"""
        codered_text = []
        for symbol in text:
            codered_text.append(int(self.alphabet.index(symbol)))
        return np.array(codered_text)

    def decoder(self, massive: list[int]) -> str:
        """переводит последовательность чисел обратно в текст, где числа - порядковый номер буквы"""
        decodered_text = []
        for sym in range(self.text_long):
            decodered_text.append(self.alphabet[int(massive[sym])])
        return "".join(decodered_text)

    def generate_key(self, matrix_size: int):
        """генерирует ключ для шифрования: создает матрицу с рандомными числами, вычисляет детерминант и
        проверяет целообратима ли"""
        while True:
            matrix = np.random.randint(self._MIN_GENERATED_NUMBER,
                                       self._MAX_GENERATED_NUMBER,
                                       size=(matrix_size, matrix_size))  # Случайные числа от -10 до 10
            if self.is_correct_matrix(matrix):
                    return matrix

    def is_correct_matrix(self, matrix) -> bool:
        """Проверяет корректность вводимого ключа на обратимость"""
        determinant = int(np.round(np.linalg.det(matrix)))
        if determinant == 1 or determinant == -1:  # Проверяем условие целочисленной обратимости
            if math.gcd(determinant % self._alphabet_size, self._alphabet_size) == 1:  # Проверяем обратимость по модулю
                return True
        return False

    # вероятно не надо контроллер сам вызовет проверку
    def personal_key(self, codered_text: list[int]):
        """ПРОВЕРЯЕМ КЛЮЧ ОТ ПОЛЬЗОВАТЕЛЯ"""
        matrix = np.array(codered_text)
        print("Ваша ключевая матрица:", "\n", matrix)

    # умножает текст на ключ
    def multiplyer(self, text: str, key: list[list[int]], number_of_text_parts: int):
        """Умножает ключ на текст:
        берет по строчно, одна строка - один кусочек текста он его переворачивает в вертикаль
        для умножения. после все кусочки собирает вместе"""

        new_text_matrix = np.zeros((1, self.key_long))[0]

        for num_of_part in range(number_of_text_parts):
            chunk = text[num_of_part]
            vertical_chunk = chunk.reshape((self.key_long, 1))
            multiplied_chunk = np.dot(key, vertical_chunk).ravel()
            new_text_matrix = np.hstack((new_text_matrix, multiplied_chunk))


        new_text_matrix = new_text_matrix[len(key):]
        return new_text_matrix
    def modul_of_codered_text(self, codered_text) -> list[int]:
        """берет по модулю алфавита каждое полученное число, что бы перевести в буквы"""
        new_codered_text = []
        for i in range(self.text_long):
            number = int(codered_text[i])
            if number<0:
                number*=(-1)

            new_codered_text.append(number% self._alphabet_size)
        return new_codered_text

    def mod(self, matrix):
        """берет всю матрицу по модулю алфавита что бы потом перевести в буквенное значение"""
        for i in range(matrix.shape[0]):
            for y in range(matrix.shape[1]):
                if matrix[i][y] < 0:
                    matrix[i][y] = 0 - (((-1) * round(matrix[i][y])) % self._alphabet_size)
                else:
                    matrix[i][y] = round(matrix[i][y]) % self._alphabet_size
        return matrix

    def encrypher(self, text: str, key: list[list[int]]):
        """поулчает значения, кодирует текст, умножает по чанкам, модуль, декодирует """

        self.text_long = len(text)
        self.key_long = len(key)
        self.num_of_added_symbols = None


    # вероятно в проверку текста ввести
        if self.text_long % self.key_long != 0:
            num_of_added_symbols = self.key_long - (self.text_long % self.key_long)
            text += self._EMPTY_CHAR * num_of_added_symbols
            self.text_long = len(text)

        matrix_of_codered_text = self.coder(text)
        codered_open_text = np.array(matrix_of_codered_text).ravel().tolist()

        number_of_text_parts=(self.text_long//self.key_long)
        matrix_of_codered_text.shape = (number_of_text_parts, self.key_long)

        closed_text=self.multiplyer(matrix_of_codered_text, key, number_of_text_parts)
        example_of_closed_text =[np.array(closed_text).ravel().tolist()]

        closed_text_moduled = self.modul_of_codered_text(closed_text)
        example_of_closed_text.append(np.array(closed_text_moduled).ravel().tolist())
        result = self.decoder(closed_text_moduled)
        return result, example_of_closed_text, self.alphabet, " ".join([str(i) for i in codered_open_text]), self.key_long

    def decrypher(self, closed_text: str, key: list[list[int]]) -> str:
        self.text_long = len(closed_text)
        self.key_long = len(key)

        number_of_parts = self.text_long // self.key_long

        codered_closed_text = self.coder(closed_text)
        codered_closed_text.shape = (number_of_parts, self.key_long)

        inverse_matrix = np.linalg.inv(key)
        decryphered_text = self.multiplyer(codered_closed_text, inverse_matrix, number_of_parts)

        decryphered_text.shape = (number_of_parts, self.key_long)
        decryphered_text = self.mod(decryphered_text).ravel()

        decodered_text = self.decoder(decryphered_text)
        added_part_long = decodered_text.count(self._EMPTY_CHAR)

        if added_part_long != 0:
            return decodered_text[:(-1 * added_part_long)]
        else:
            return decodered_text

    def create_data_for_how_to_multiple(self, key, codered_open_text, answer, key_long):
        """подготавливает данные для таблицы 'как умножать'"""
        before_module, moduled_answer = answer
        before_module = before_module[:key_long]
        moduled_answer = moduled_answer[:key_long]
        how_to_multiple = []
        first_piece_of_text = codered_open_text.split()[:self.key_long]
        for row in range(len(key)):
            create_new_row = []
            for column in range(key_long):
                create_new_row.append(f"{key[row][column]} * {first_piece_of_text[column]}")
            new_row = str( f'{"+".join(create_new_row)} = {round(before_module[row])}; {round(before_module[row])}mod(33) = {moduled_answer[row]}')
            how_to_multiple.append([new_row])
        return how_to_multiple

class HillView:
    def __init__(self, parent):
        self.parent = parent
        self._AVAILABLE_MATRIX_SIZES = ['2', '3', '4']
        self._EMPTY_KEY_CHAR = 0

        self.decrypt = None
        self.encrypt = None
        self.clean_matrix = None
        self.generate_matrix = None
        # переменные
        self.key_frame = None
        self.matrix_frame = None
        self.study_inf_frame = None
        self.crypher_frame = None
        self.matrix_size = None
        self.result_text = None
        self.text = None
        self.error_text = None

        self.draw_widgets()

    def draw_widgets(self):
        self.create_frames()
        self.create_result_frame()
        self.create_key_frame()

    def create_frames(self):

        self.crypher_frame = ttk.Frame(self.parent)
        self.crypher_frame.pack()

        self.key_frame = ttk.Frame(self.crypher_frame, borderwidth=1, relief="solid", width=200, height=150, padding=(8, 10))
        self.key_frame.grid(row=0, column=0, sticky="nsew")

        self.matrix_frame = ttk.Frame(self.key_frame, borderwidth=1, relief="solid", width=200, height=150, padding=(8, 10))
        self.matrix_frame.grid(row=4, column=0, rowspan=2)

        self.result_frame = ttk.Frame(self.crypher_frame, borderwidth=1, relief="solid", width=200, height=150, padding=(8, 10))
        self.result_frame.grid(row=0, column=1, sticky="nsew")

        self.study_inf_frame = ttk.Frame(self.parent, width=200, height=150, padding=(8, 10))
        self.study_inf_frame.pack()

    def create_key_frame(self):
        key_main_label = ttk.Label(self.key_frame, text="Твой ключ:")
        key_main_label.grid(row=0, column=0, columnspan=3)

        matrix_size_label_widget = ttk.Label(self.key_frame, text="Выбери размер матрицы")
        matrix_size_label_widget.grid(row=2, column=0, rowspan=2)


        self.matrix_size = StringVar(value=self._AVAILABLE_MATRIX_SIZES[0])
        matrix_size_widget = ttk.Combobox(self.key_frame, textvariable=self.matrix_size, values=self._AVAILABLE_MATRIX_SIZES, state="readonly")
        matrix_size_widget.grid(row=2, column=1)
        matrix_size_widget.bind("<<ComboboxSelected>>", self.event_chose_matrix_size)

        # создает базовую матрицу
        self.change_matrix_size(int(self.matrix_size.get()))


        clean_matrix_button = ttk.Button(self.key_frame, text="Очистить", command=self._clean_matrix)
        clean_matrix_button.grid(row=4, column=1)

        generate_matrix_button = ttk.Button(self.key_frame, text="Сгенерировать матрицу", command=self._generate_matrix)
        generate_matrix_button.grid(row=5, column=1)

        self.error_text = StringVar()
        error_widget = ttk.Label(self.key_frame, textvariable=self.error_text, foreground="red")
        error_widget.grid(row=6, column=0, columnspan=2)

    def change_matrix_size(self, size: int) -> None:
        matrix = self.matrix_frame.winfo_children()
        for i in matrix:
            i.destroy()

        for row in range(size):
            for column in range(size):
                ttk.Entry(self.matrix_frame, validate="key", width=5).grid(row=row, column=column)

    def create_result_frame(self):
        text_label = Label(self.result_frame, text="Enter the text to encrypt")
        text_label.grid(row=1, column=0)

        self.text = Text(self.result_frame, width=50, height=6)
        self.text.grid(row=2, columnspan=2)

        encrypt_button = ttk.Button(self.result_frame, text="Зашифровать", command=self._encrypt)
        encrypt_button.grid(row=5, column=0)
        decrypt_button = ttk.Button(self.result_frame, text="Расшифровать", command=self._decrypt)
        decrypt_button.grid(row=5, column=1)

        self.result_text = Text(self.result_frame, width=50, height=6)
        self.result_text.grid(row=6, columnspan=2)

    def create_table(self,frame, data, row, column, width=25):
        table = Sheet(frame,
                               data=data,
                               show_header=False,
                               show_x_scrollbar=False,
                               show_y_scrollbar=False,
                               show_row_index=False,
                               column_width=width,
                               row_width=25,
                               width=width * column,
                               height=26 * row,
                               empty_horizontal=0,
                               empty_vertical=0
                               )
        return table


    def create_study_inf_frame_encrypt(self,
                                       key_long,
                                       alphabet,
                                       open_text,
                                       codered_open_text,
                                       key,
                                       how_to_multiple,
                                       codered_closed_text,
                                       closed_text
                                       ):
        formula_codered_txt = [['c₁'], ['c₂'], ['c₃']]

        formula_key = [i.split() for i in"k₁₁ k₁₂ k₁₃\nk₂₁ k₂₂ k₂₃\nk₃₁ k₃₂ k₃₃".split("\n")]
        formula_result = [['p₁'], ['p₂'], ['p₃']]
        how_to_multiple_txt = [[i] for i in "c₁ = k₁₁·p₁ + k₁₂·p₂ + k₁₃·p₃\nc₂ = k₂₁·p₁ + k₂₂·p₂ + k₂₃·p₃\nc₃ = k₃₁·p₁ + k₃₂·p₂ + k₃₃·p₃".split("\n")]

        how_to_code_text_widget = Label(self.study_inf_frame,text="Для кирилицы каждой букве сопоставляется число, "
                                             "например, A – 0, Б – 1, В – 2, …, Я – 32. В общем случае "
                                             "соответствия “буква – число” можно выбрать произвольно.")
        how_to_code_text_widget.pack()

        alphabet_table = self.create_table(self.study_inf_frame, [list(alphabet)]+[[i for i in range(len(alphabet))]], 2, 33)
        alphabet_table.pack()

        text1 = ttk.Label(self.study_inf_frame, text="Открытый текст представляет собой n-мерный вектор. Ключ – "
                                                  "квадратная матрица размера n x n. Для получения шифротекста ключ "
                                                  "умножается на открытый текст по модулю выбранной числовой схемы,"
                                                  " в данном случае - 32, или 33 с допольнительным символом."
                                                  "Пусть \"p₁ p₂ p₃\" – открытый текст, ключ – матрица размера 3 x 3 и "
                                                  "шифротекст – вектор размерности – 3, \"с₁ с₂ с₃\" соответственно. "
                                                  "В матричном виде эта система описывается так:", wraplength=800)
        text1.pack()

        self.coder_frame = ttk.Frame(self.study_inf_frame)
        self.coder_frame.pack()

        open_text_widget = tk.Label(self.coder_frame, text=open_text)
        open_text_widget.grid(row=0, column=0)

        arrow = tk.Label(self.coder_frame, text=chr(11116))
        arrow.grid(row=0, column=1)

        codered_open_text_widget = tk.Label(self.coder_frame, text=codered_open_text)
        codered_open_text_widget.grid(row=0, column=2)

        text2 = tk.Label(self.study_inf_frame, text="Далее шифрование идет по чанкам. Текст разбивается на чанки длинной, равной длине ключа. Если текст не делится ровно, то используются добавочные символы. Например добавочным символом будет '|', тогда его номер будет 33.", wraplength=800)
        text2.pack()

        self.multipler_frame = ttk.Frame(self.study_inf_frame)
        self.multipler_frame.pack()

        self.formula_multipler_frame = ttk.Frame(self.multipler_frame)
        self.formula_multipler_frame.grid(row=0, column=0)

        self.example_multipler_frame = ttk.Frame(self.multipler_frame)
        self.example_multipler_frame.grid(row=0, column=1)

        codered_closed_text_vertical_formula = self.create_table(self.formula_multipler_frame, formula_codered_txt, len(formula_codered_txt), 1)
        codered_closed_text_vertical_formula.grid(row=0, column=2)

        multipler_sighn = ttk.Label(self.formula_multipler_frame, text="X")
        multipler_sighn.grid(row=0, column=1)

        key_table = self.create_table(self.formula_multipler_frame, formula_key, key_long, key_long)
        key_table.grid(row=0, column=0)
        equal_sighn = ttk.Label(self.formula_multipler_frame, text="=")
        equal_sighn.grid(row=0, column=3)


        codered_closed_text_vertical = self.create_table(self.formula_multipler_frame,
                                             formula_result, len(formula_result), 1)
        codered_closed_text_vertical.grid(row=0, column=4)




        vertical_codered_text_data = [[i] for i in codered_open_text.split()[:key_long]]

        codered_closed_text_vertical = self.create_table(self.example_multipler_frame, vertical_codered_text_data, len(vertical_codered_text_data), 1)
        codered_closed_text_vertical.grid(row=0, column=2)

        multipler_sighn = ttk.Label(self.example_multipler_frame, text="X")
        multipler_sighn.grid(row=0, column=1)

        key_table = self.create_table(self.example_multipler_frame,
                                             key,key_long, key_long)
        key_table.grid(row=0, column=0)

        equal_sighn = ttk.Label(self.example_multipler_frame, text="=")
        equal_sighn.grid(row=0, column=3)

        vertical_closed_text_data =[[i] for i in codered_closed_text.split()[:key_long]]

        codered_closed_text_vertical = self.create_table(self.example_multipler_frame,
                                             vertical_closed_text_data,len(vertical_closed_text_data), 1)

        codered_closed_text_vertical.grid(row=0, column=4)

        text3 = ttk.Label(self.study_inf_frame, text="Или в качестве системы уравнений:")
        text3.pack()

        frame_how_to_multiple = ttk.Frame(self.study_inf_frame)
        frame_how_to_multiple.pack()

        example_how_to_multiple_table = self.create_table(frame_how_to_multiple,how_to_multiple_txt, 3, 1, 200)
        example_how_to_multiple_table.grid(row=0, column=0)

        how_to_multiple_table = self.create_table(frame_how_to_multiple,
                          how_to_multiple,key_long, 1, 400)
        how_to_multiple_table.grid(row=0, column=1)

        text4 = ttk.Label(self.study_inf_frame,text="Из уравнений видно, что каждый символ открытого текста участвует "
                                                    "в шифровании шифротекста. Именно поэтому шифр Хилла принадлежит "
                                                    "к категории блочных шифров.\nТеперь декодирует результат, "
                                                    "переведя по таблице обратно для получения результата.", wraplength=800)
        text4.pack()

        self.decoder_frame = ttk.Frame(self.study_inf_frame)
        self.decoder_frame.pack()

        codered_closed_text_widget = tk.Label(self.decoder_frame, text=closed_text)
        codered_closed_text_widget.grid(row=0, column=2)

        arrow = tk.Label(self.decoder_frame, text=chr(11116))
        arrow.grid(row=0, column=1)

        closed_text_widget = tk.Label(self.decoder_frame, text=codered_closed_text)
        closed_text_widget.grid(row=0, column=0)

    def event_chose_matrix_size(self, event) -> None:
        """Отрисовывает матрицу правильного размера"""
        self.change_matrix_size(int(self.matrix_size.get()))

    def get_matrix_data(self) -> list[list[int]]:
        key_size = int(self.matrix_size.get())
        key = [[self._EMPTY_KEY_CHAR] * key_size for _ in range(key_size)]

        list_of_data = iter(self.matrix_frame.winfo_children())
        for row in range(key_size):
            for column in range(key_size):
                key[row][column] = int(next(list_of_data).get())
        return key

    def set_matrix_data(self, data: list[int]) -> None:
        """Очищает матрицу и вставляет новые значения"""
        for child in self.matrix_frame.winfo_children():
            child.delete(0, END)

        data_iter = iter(data)
        for cell in self.matrix_frame.winfo_children():
            cell.insert(0, next(data_iter))

    def get_key_size(self) -> int:
        return int(self.matrix_size.get())

    def get_text(self) -> str:
        return self.text.get("1.0", 'end-1c').upper()

    def set_result_text(self, text: str) -> None:
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", text)

    def error_wrong_symbol_in_text(self):
        self.error_text.set("В тексте могут использоваться только\n"
                            "заглавные буквы кирилицы без доп знаков и чисел.\nПопробуйте снова")

    def error_letter_in_key(self):
        self.error_text.set("В качестве ключа могут\nиспользоваться только целые числа")

    def delete_error(self):
        self.error_text.set("")

    def _encrypt(self):
        if self.encrypt:
            self.encrypt()

    def _decrypt(self):
        if self.decrypt:
            self.decrypt()

    def _clean_matrix(self):
        if self.clean_matrix:
            self.clean_matrix()

    def _generate_matrix(self):
        if self.generate_matrix:
            self.generate_matrix()


class HillController:
    def __init__(self, parent_frame):
        self.view = HillView(parent_frame)
        self.model = HillModel()

        # связываем функции
        self.view.decrypt = self._handle_decrypt
        self.view.encrypt = self._handle_encrypt
        self.view.clean_matrix = self._handle_clean_matrix
        self.view.generate_matrix = self._handle_generate_matrix

    def _handle_encrypt(self):
        key = self.view.get_matrix_data()
        open_text = self.view.get_text()

        if self.is_correct_data(open_text, key):
            closed_text, codered_closed_text,alphabet, codered_open_text, key_long = self.model.encrypher(open_text, key)
            how_to_multiple_table = self.model.create_data_for_how_to_multiple(key, codered_open_text, codered_closed_text, key_long)
            self.view.set_result_text(closed_text)

            for child in self.view.study_inf_frame.winfo_children():
                child.destroy()
            self.view.create_study_inf_frame_encrypt(key_long, alphabet, open_text, codered_open_text, key,how_to_multiple_table, " ".join([str(i) for i in codered_closed_text[1]]), closed_text)


    def _handle_decrypt(self):
        key = self.view.get_matrix_data()
        closed_text = self.view.get_text()

        if self.is_correct_data(closed_text,key):
            open_text = self.model.decrypher(closed_text, key)
            self.view.set_result_text(open_text)


    def _handle_clean_matrix(self):
        self.view.change_matrix_size(int(self.view.matrix_size.get()))

    def _handle_generate_matrix(self):
        generated_matrix = self.model.generate_key(int(self.view.matrix_size.get()))
        float_matrix_for_view = generated_matrix.ravel().tolist()
        self.view.set_matrix_data(float_matrix_for_view)

    def is_correct_data(self, text: str, key: list[list[int]]) -> bool:

        if self.is_text_correct(text) and self.is_key_correct(key):
            return True
        return False

    def is_text_correct(self, text: str) -> bool:
        alphabet = self.model.get_alphabet()

        for letter in text:
            if letter not in alphabet:
                self.view.error_wrong_symbol_in_text()
                return False
        self.view.delete_error()
        return True

    def is_key_correct(self, key: list[list[int]]) -> bool:
        return True
        """проверяет есть ли в ключе буквы но не проверяет целые ли числа но в целом не нужен
        ибо при сборе данных ошибка сама выдается"""
        flat_key = np.array(key).ravel().tolist()
        flat_key ="".join(flat_key)

        return flat_key.isdigit()

# class HillTestView:
#     def __init__(self, parent_frame):
#         self.view = HillView(parent_frame)
#
#         alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
#         open_text = "открытый текст"
#         codered_open_text = "1 2 3 4 13"
#         # vertical_codered_text = codered_open_text.split(" ")
#         key = [[i for i in range(3)] for _ in range(3)]
#         how_to_multiple = ["1","2","3"]
#         codered_closed_text = "13 4 3 2 1"
#         closed_text = "закрытый текст"
#         self.view.create_study_inf_frame_encrypt(alphabet,
#                                                  open_text,
#                                                  codered_open_text,
#                                                  key,
#                                                  how_to_multiple,
#                                                  codered_closed_text,
#                                                  closed_text)



# пустое окно с инф обо мне шифре и тп НАДО ПОМЕНЯТЬ РОДИТЕЛЯ ИБО ЗАЧЕМ
class OpeningWindow(ListOfCoders):
    def __init__(self, parent):
        self.infFrame = parent

        opening_window = tk.Label(self.infFrame, text="СУПЕР ТЕКСТ О ПОДДЕРЖКЕ И СИЛЕ", width=400, height=400)
        opening_window.pack()


if __name__ == "__main__":
    root = tk.Tk()

    # берет размеры экрана
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Устанавливаем размеры окна
    root.geometry(f"{screen_width}x{screen_height}")
    app = MainApp(root)
    root.mainloop()



