# -*- coding: utf-8 -*-
import tkinter as tk
from time import process_time_ns
from tkinter import *
from tkinter import ttk
from tksheet import Sheet
import random
from tkinter.messagebox import showwarning

class MainApp:
    def __init__(self, root):
        self.root = root

        self.listFrame = tk.Frame(root)
        self.listFrame.pack(side='left', fill='y')

        self.infFrame = tk.Frame(root)
        self.infFrame.pack(side='right', fill='both', expand=True)

        OpeningWindow(self.infFrame)

        list_of_coders = [["Шифр Цезаря"], ["Решетка Кардано"],['Скитала Шифр'], ["Информация по проекту"]]
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
            TableSkitalaCripher(self.infFrame)
        elif index == 3:
            OpeningWindow(self.infFrame)



class ListOfCoders(MainApp):
    # общие переменные(словари)
    def __init__(self, parent):
        self.infFrame = parent
        test = tk.Label(self.infFrame, text="WORKS!!!!")
        test.grid(row=0, column=1)



    # здесь общие функции
    def change_filling(self, filling,frame, is_created=True):
        if is_created:
            self.matrix.destroy()

        self.matrix = Sheet(frame,
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
        self.key_matrix.change_filling(BASE_FILLING, frame=self.frame)

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
        def change_filling(self, filling, is_created, frame):
            ListOfCoders.change_filling(self, filling, is_created, self.frame)
            # if is_created:
            #     self.matrix.destroy()
            #
            # self.matrix = Sheet(self.frame,
            #                     data=filling,
            #                     show_header=False,
            #                     show_x_scrollbar=False,
            #                     show_y_scrollbar=False,
            #                     show_row_index=False,
            #                     column_width=25,
            #                     row_width=25,
            #                     width=25*len(filling),
            #                     height=26*(len(filling)),
            #                     empty_horizontal=0,
            #                     empty_vertical=0)
            # self.matrix.hide("y_scrollbar")
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

        def change_filling(self, filling, frame, is_created=True):
            super().change_filling(filling, is_created, frame)
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


class TableSkitalaCripher(ListOfCoders):
    def __init__(self, parent):
        self.infFrame = parent

        self.matrix = None
        BASE_SIZE=[2,3]
        BASE_DATA = [["0" for _ in range(BASE_SIZE[1])] for _ in range(BASE_SIZE[0])]
        self.change_filling(BASE_DATA, False)
        ttk.Label(self.infFrame, text="Шифр Цезаря").grid(column=0,row=0, columnspan=2)

        history_inf = ttk.Label(self.infFrame, text="Шифр Цезаря, также известный как шифр сдвига или код Цезаря"
                                                    " — разновидность шифра подстановки, в котором каждый символ в"
                                                    " открытом тексте заменяется символом, находящимся на некотором "
                                                    "постоянном числе позиций левее или правее него в алфавите.",
                                wraplength=400)
        history_inf.grid(column=0,row=1, columnspan=2)

        open_text_widget = Text (self.infFrame, height=10, width=60)
        open_text_widget.grid(column=1,row=2)

        table_size_text_widget = tk.Label(self.infFrame, text="Размер решетки:")
        table_size_text_widget.grid(column=1, row=3)

        size_frame = tk.Frame(self.infFrame)
        size_frame.grid(column=1, row=4)

        row_number = IntVar()
        row_number_widget = tk.Entry(size_frame, textvariable=row_number, width=5)
        row_number_widget.grid(column=0, row=0)

        x_widget = tk.Label(size_frame, text='X')
        x_widget.grid(column=1, row=0)

        column_number = IntVar()
        column_number_widget = tk.Entry(size_frame, textvariable=column_number, width=5)
        column_number_widget.grid(column=2, row=0)

        coder_button = tk.Button(size_frame, text='Кодировать', command=self.coder)
        coder_button.grid(column=3, row=0)

        closed_text_widget = tk.Text(self.infFrame, height=10)
        closed_text_widget.grid(column=0,row=5, columnspan=2)

    # def change_filling(self, filling, is_created=True):
    #     if is_created:
    #         self.matrix.destroy()
    #
    #     self.matrix = Sheet(self.infFrame,
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
    #     self.matrix.grid(row=2, column=0, rowspan=3)

    def coder(self):
        pass

# пустое окно с инф обо мне шифре и тп
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


