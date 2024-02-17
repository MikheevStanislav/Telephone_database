from typing import Any
import os

# Для начала создадим класс, который хранит из имен номера. Это будет Древо поиска(префиксное дерево), т.к пользователь может не знать
# имени искомого человека целиком. Если мы реализуем хранение пары имя -> номер то временная сложность при удобном
# для пользователя способе(к примеру есть имена Артем, Анатолий, Борис, пользователь воодит А, программа выдает
# Артема и Анатолия) ьудет O(N), а у дерева O(logN) P.S именно ради этой фичи нужен этот класс. Т.к. для пары телефон
# -> такая фича не нужна, мы можем использовать простую хэштаблицу.

class SearchTreeNode:
    """
        Конструктор для создания узла дерева поиска.

        :param name: Имя конкретной ноды (строка).
        :param parent: Родительская нода (SearchTreeNode).
        :param person: Объект класса person, к которому принадлежит эта нода.
    """
    def __init__(self, name=None, parent=None, person=None):
        self.name = name  # Имя конкретной ноды
        self.parent = parent #отец ноды
        self.child = {}  # Хэштаблица всех сыновей ноды
        self.person = person #объект класса person к которой эта нода принадлежит
        self.indexes = set() #индексы person с таким именем\фамилией\отчеством\именем организации


class NameSearchTree:
    def __init__(self):
        """
                Конструктор для создания древа поиска имен.
        """
        self.root = SearchTreeNode("")  # создаем корень. Корень не будет иметь имени

    # метод добавления данных в древо

    def insert(self, name, index) -> SearchTreeNode:
        """
        Метод для добавления данных в древо.

        :param name: Имя для добавления в древо (строка).
        :param index: Индекс связанный с именем (число).
        :return: Возвращает новый узел древа (SearchTreeNode).
        """
        current = self.root  # Начинаем с корня
        for i in range(len(name)):  # Проходим по каждой букве в имени
            ch = name[i]
            if ch not in current.child:  # Если такой буквы нет, создаем новую ноду
                current.child[ch] = SearchTreeNode(str(current.name) + str(ch), current)
            current = current.child[ch]
            if i == len(name) - 1:  # Если это последняя буква, добавляем индекс
                current.indexes.add(index)
        return current

    def _find_leaf(self, node) -> []:
        """
        Вспомогательный метод для поиска всех листьев конкретной вершины. Используется для поиска по древу.

        :param node: Нода, с которой начинается поиск (SearchTreeNode).
        :return: Список листьев (list).
        """
        if node is None:
            return []
        if len(node.child) == 0:
            return [node]
        else:
            leaf_nodes = []
            for ch in node.child:
                leaf_nodes.extend(self._find_leaf(node.child[ch]))
            return leaf_nodes

    def search(self, name: str) -> []:
        """
        Возвращает все подходящие под описание объекты
        :param name: имя искомой строки в префиксном древе
        :return: массив строк префикс которых совпадает с name
        """
        current = self.root
        for i in range(len(name)):
            ch = name[i]
            if ch not in current.child:
                return None
            current = current.child[ch]
            if i == len(name) - 1:
                if (current.child is not None):
                    return (self._find_leaf(current))
                else:
                    return [current]

    def delete(self, node: SearchTreeNode) -> bool:
        """
        метод удаления ноды. Если нода не имеет братьев, ее отца также нужно удалить
        :param node: узел который нужно удалить
        :return:
        """
        name = node.name
        ans = self.search(name)
        if ans is None or len(ans) == 0:
            print("Не найдено таких записей")
            return
        if (len(ans) == 1):
            while ans[0].parent is not None and len(ans[0].parent.child) == 1 and ans[0] != self.root:
                del ans[0].parent.child[ans[0].name[-1]]
                ans[0] = ans[0].parent
        else:
            print("Выберите какой номер вы хотите удалить(счет от 1):")
            for i, x in enumerate(ans):
                print(str(int(i + 1)) + " " + x.name + " " + str(x.number))
            index = int(input()) - 1
            del ans[index].parent.child[ans[index].name[-1]]


class Person:
    """
    класс человека, который вводит биекцию между комбинацией ФИО и 2 номерами телефона
    """
    def __init__(self, name: SearchTreeNode, family_name: SearchTreeNode, fathers_name: SearchTreeNode,
                 organisation_name: SearchTreeNode, work_number: str, personal_number: str, index: int):
        """
        инициализация
        :param name: имя человека
        :param family_name: фамилия человека
        :param fathers_name: отчество
        :param organisation_name: название организации
        :param work_number: рабочий телефон
        :param personal_number: личный телефон
        :param index: индекс в массиве внутри table
        """
        self.name = name
        self.family_name = family_name
        self.fathers_name = fathers_name
        self.organisation_name = organisation_name
        self.work_number = work_number
        self.personal_number = personal_number
        self.index = index


class Table:
    """
    класс таблицы. Хранит путь до объекта, массив людей, а также хэшмапы из номеров телефонов в людей
    """
    #при инициализации открывает путь до файла и считывает всю информацию из него в префиксные деервья и хэшмапы(для имени, фамилии, отчества свои префиксные деревья)
    def __init__(self, pathfile):
        """
        инициализация таблицы
        :param pathfile: путь до файла с базой
        """
        self.pathfile = pathfile
        self.persons_array = [] #массив объектов person
        self.names_tree = NameSearchTree() #префиксное древо для имени
        self.family_names_tree = NameSearchTree()#для фамилии
        self.fathers_names_tree = NameSearchTree()#для отчества
        self.organisation_names_tree = NameSearchTree()#для названия организации
        self.personal_number_to_person = {}#хэшмапа для личного номера
        self.work_number_to_person = {}#для рабочего
        with open(self.pathfile + '.txt', 'r', encoding='utf-8') as file: # загрузка информации из файла
            i = 0
            for line in file:
                if line == "\n":
                    continue
                name, family_name, fathers_name, organisation_name, work_number, personal_number = line.split(',')
                new_person = Person(self.names_tree.insert(name, i), self.family_names_tree.insert(family_name, i),
                                    self.fathers_names_tree.insert(fathers_name, i),
                                    self.organisation_names_tree.insert(organisation_name, i),
                                    work_number, personal_number, i)
                self.persons_array.append(new_person)
                self.personal_number_to_person[personal_number.strip()] = self.persons_array[-1]
                self.work_number_to_person[work_number] = self.persons_array[-1]
                i += 1


    def insert_data(self, name: str, family_name: str, fathers_name: str, organisation_name: str, work_number: str,
                    personal_number: str) -> Person:
        """
        функция вставки данных
        :param name: имя
        :param family_name: фамилия
        :param fathers_name: отчество
        :param organisation_name: название организации
        :param work_number: номер телефона для работы
        :param personal_number: личный номер теелфона
        :return:
        """
        i = len(self.persons_array)
        new_person = Person(self.names_tree.insert(name, i), self.family_names_tree.insert(family_name, i),
                            self.fathers_names_tree.insert(fathers_name, i),
                            self.organisation_names_tree.insert(organisation_name, i),
                            work_number, personal_number, i)
        if self.search(name, family_name, fathers_name, organisation_name) is not None and len(self.search(name,
                                                                                                           family_name,
                                                                                                           fathers_name,
                                                                                                           organisation_name)) != 0:
            print("Этот объект уже есть")
            return None
        self.persons_array.append(new_person)
        self.personal_number_to_person[personal_number] = self.persons_array[-1]
        self.work_number_to_person[work_number] = self.persons_array[-1]
        with open(self.pathfile + '.txt', 'a', encoding='utf-8') as file:
            file.write(
                name + ',' + family_name + ',' + fathers_name + ',' + organisation_name + ',' + work_number + ',' + personal_number + '\n')
            print("Данные успешно загружены")
            file.close()
        return new_person


    def read_data(self, index: int) -> None:
        """
        функция прочтения данных из person в массиве persons_array
        :param index: индекс person(который выводим на экран) в массиве person_array
        :return:
        """
        print(str(index) + ":" + self.persons_array[index].family_name.name + " " + self.persons_array[
            index].name.name + " " +
              self.persons_array[index].fathers_name.name + ", " + self.persons_array[
                  index].organisation_name.name + "     Рабочий номер:" +
              self.persons_array[index].work_number + "      Домашний номер:" + self.persons_array[
                  index].personal_number)


    def read_all_data(self) -> None:
        """
        использование предыдущего метода на все элементы массива persons_array
        :return:
        """
        for i in range(len(self.persons_array)):
            self.read_data(i)


    def search_number(self, string: str) -> Person:
        """
        поиск person по хэшапам номеров
        :param string: номер телефона
        :return:
        """
        if string in self.personal_number_to_person:
            return self.personal_number_to_person[string]
        if string in self.work_number_to_person:
            return self.work_number_to_person[string]
        else:
            print("Такого номера не найдено в базе данных")
            return None

    #поиск по префиксным деревьям
    def _search_name(self, string: str, mas=None) -> []:
        """
        поиск по префиксному дереву имен
        :param string: имя
        :param mas: в случае если этот поиск не первый(то есть мы отобрали всех с некотрой фамилией\отчеством\названием организации и хотим из них отлбрать всех с некотрым префиксом имени)
        :return:
        """
        ans = []
        if string is None:
            return mas
        if self.names_tree.search(string) is None:
            return
        for x in self.names_tree.search(string):
            for i in x.indexes:
                if mas is None:
                    ans.append(i)
                else:
                    if i in mas:
                        ans.append(i)
        return ans

    def _search_family(self, string, mas=None) -> []:
        """
        поиск по префиксному дереву фамилий
        :param string: фамилия
        :param mas:  случае если этот поиск не первый(то есть мы отобрали всех с некотрой именем\отчеством\названием организации и хотим из них отлбрать всех с некотрым префиксом фамилии
        :return:
        """
        ans = []
        if string is None:
            return mas
        if self.family_names_tree.search(string) is None:
            return
        for x in self.family_names_tree.search(string):
            for i in x.indexes:
                if mas is None:
                    ans.append(i)
                else:
                    if i in mas:
                        ans.append(i)
        return ans

    def _search_father_name(self, string, mas=None) -> []:
        """
        аналогично по отчеству
        :param string:
        :param mas:
        :return:
        """
        ans = []
        if string is None:
            return mas
        if self.fathers_names_tree.search(string) is None:
            return
        for x in self.fathers_names_tree.search(string):
            for i in x.indexes:
                if mas is None:
                    ans.append(i)
                else:
                    if i in mas:
                        ans.append(i)
        return ans

    def _search_organisation_name(self, string, mas=None) -> []:
        """
        и по имени организации
        :param string:
        :param mas:
        :return:
        """
        ans = []
        if string is None:
            return mas
        if self.organisation_names_tree.search(string) is None:
            return
        for x in self.organisation_names_tree.search(string):
            if mas is None:
                ans.append(x)
            else:
                if x in mas:
                    ans.append(x)
        return ans

    def search(self, name=None, family_name=None, father_name=None, organisation_name=None) -> []:
        """
        суммарный поиск по всем 4 параметрам
        :param name:
        :param family_name:
        :param father_name:
        :param organisation_name:
        :return:
        """
        if (name is None and family_name is None and father_name is None and organisation_name is None):
            return (None)
        return self._search_organisation_name(organisation_name, self._search_father_name(father_name,
                                                                                          self._search_family(
                                                                                              family_name,
                                                                                              self._search_name(name))))

    def change(self, index: int):
        """
        функция изменения некотрого элемента
        :param index:
        :return:
        """
        print("Введите имя(не вводите ничего если оставить неизмененным)")
        string = input()
        if string:
            temp = self.persons_array[index].name
            self.persons_array[index].name = self.names_tree.insert(string, index)
            self.names_tree.delete(temp)
        print("Введите фамилию(не вводите ничего если оставить неизмененным)")
        string = input()
        if string:
            temp = self.persons_array[index].family_name
            self.persons_array[index].family_name = self.family_names_tree.insert(string, index)
            self.fathers_names_tree.delete(temp)
        print("Введите отчество(не вводите ничего если оставить неизмененным)")
        string = input()
        if string:
            temp = self.persons_array[index].fathers_name
            self.persons_array[index].fathers_name = self.fathers_names_tree.insert(string, index)
            self.fathers_names_tree.delete(temp)
        print("Введите имя организации(не вводите ничего если оставить неизмененным)")
        string = input()
        if string:
            temp = self.persons_array[index].organisation_name
            if (temp.name == string):
                print("Имя тоже что и было")
            else:
                self.persons_array[index].organisation_name = self.organisation_names_tree.insert(string, index)
                self.organisation_names_tree.delete(temp)
        print("Введите рабочий номер телефона(не вводите ничего если оставить неизмененным)")
        string1 = input()
        if string1:
            if string1 in self.personal_number_to_person or string1 in self.work_number_to_person:
                print("Этот номер занят")
                return
            self.work_number_to_person[string1] = self.persons_array[index]
            del self.work_number_to_person[self.persons_array[index].work_number]
            self.persons_array[index].work_number = string1

        print("Введите домашний номер телефона(не вводите ничего если оставить неизмененным)")
        string = input()
        if string:
            if string1 == string:
                self.personal_number_to_person[string] = self.persons_array[index]
                del self.personal_number_to_person[self.persons_array[index].personal_number.strip()]
                self.persons_array[index].personal_number = string
            else:
                if string in self.personal_number_to_person or string in self.work_number_to_person:
                    print("Этот номер занят")
                    return
                self.personal_number_to_person[string] = self.persons_array[index]
                del self.personal_number_to_person[self.persons_array[index].personal_number]
                self.persons_array[index].personal_number = string
        print("Данные успешно обновлены")
        self._save_changes()

    def _save_changes(self):
        with open(self.pathfile + '.txt', 'w', encoding='utf-8') as file:
            for i in range(len(self.persons_array)):
                file.write(
                    self.persons_array[i].name.name + "," + self.persons_array[i].family_name.name + "," +
                    self.persons_array[
                        i].fathers_name.name +
                    "," + self.persons_array[i].organisation_name.name + "," + self.persons_array[i].work_number + "," +
                    self.persons_array[i].personal_number + "\n")


print("Добро пожаловать в телефонный справочник")
table1 = Table("base")
arr = table1._search_name("Артем")
while (True):
    print(
        "Выберите действие(введите номер в терминал):" + '\n' + "1. Вывести весь справочник" + '\n' +
        "2. Вставить новый объект" + '\n' + "3. Найти запись в справочнике" + '\n' + "4. Редактировать запись" +
        '\n' + "5. Выход")
    choice = str(input())
    if choice == "":
        print("Неопознанная команда")
        continue
    if choice[0] == '5':
        print("До новых встреч!")
        table1._save_changes()
        break
    if choice[0] == '1':
        table1.read_all_data()
    if choice[0] == '2':
        mas = []
        print("Введите фамилию владельца номера(нажмите ENTER чтобы пропустить)")
        mas.append(input())
        print("Введите имя владельца номера(нажмите ENTER чтобы пропустить)")
        mas.append(input())
        print("Введите отчество")
        mas.append(input())
        print("Введите название организации(нажмите ENTER чтобы пропустить)")
        mas.append(input())
        print("Введите рабочий номер(нажмите ENTER чтобы пропустить)")
        mas.append(input())
        print("Введите домашний номер(нажмите ENTER чтобы пропустить)")
        mas.append(input())
        if (mas[4] in table1.work_number_to_person or mas[5] in table1.work_number_to_person
                or mas[4] in table1.personal_number_to_person or mas[5] in table1.personal_number_to_person):
            print("Человек с таким номером уже существует")
            continue
        for i in range(len(mas)):
            if mas[i] == "":
                mas[i] = "_"
        table1.insert_data(mas[1], mas[0], mas[2], mas[3], mas[4], mas[5])
    if choice[0] == "3":
        print(
            "Выберите вариант поиска:" + "\n" + "1: По номеру телефона(любого)" + "\n" + "2: По имени/фамилии/отчеству/имени организации")
        choice2 = input()
        if choice2 == '1':
            print("Введите номер:")
            person = table1.search_number(input())
            if person == None:
                continue
            table1.read_data(person.index)
        if choice2 == '2':
            mas = []
            print("Введите фамилию владельца номера(нажмите ENTER чтобы пропустить)")
            mas.append(input())
            print("Введите имя владельца номера (нажмите ENTER чтобы пропустить)")
            mas.append(input())
            print("Введите отчество (нажмите ENTER чтобы пропустить)")
            mas.append(input())
            print("Введите название организации (нажмите ENTER чтобы пропустить)")
            mas.append(input())
            for i in range(0, len(mas)):
                if mas[i] == "":
                    mas[i] = None
            temp = table1.search(mas[1], mas[0], mas[2], mas[3])
            if temp is None or len(temp) == 0:
                print("Не найдено таких записей")
                continue
            for x in temp:
                table1.read_data(x)
        else:
            print("Неопознанная команда")
            continue
    if choice[0] == "4":
        print(
            "Выберите вариант поиска:" + "\n" + "1: По номеру телефона(любого)" + "\n" + "2: По имени/фамилии/отчеству/имени организации")
        choice2 = input()
        if choice2 == '1':
            print("Введите номер:")
            person = table1.search_number(input())
            table1.read_data(person.index)
            table1.change(person.index)
        if choice2 == '2':
            mas = []
            print("Введите фамилию владельца номера(нажмите ENTER чтобы пропустить)")
            mas.append(input())
            print("Введите имя владельца номера (нажмите ENTER чтобы пропустить)")
            mas.append(input())
            print("Введите отчество (нажмите ENTER чтобы пропустить)")
            mas.append(input())
            print("Введите название организации (нажмите ENTER чтобы пропустить)")
            mas.append(input())
            for i in range(0, len(mas)):
                if mas[i] == "":
                    mas[i] = None
            temp = table1.search(mas[1], mas[0], mas[2], mas[3])
            if temp is None or len(temp) == 0:
                print("Не найдено таких записей")
                continue
            for i,x in enumerate(temp):
                print(str(i) + ": ")
                table1.read_data(x)
            print("Выберите запись")
            choice3 = input()
            if not choice3.isdigit() or int(choice3) > len(temp) or int(choice3) < 0:
                print("Неопознанная команда")
                continue
            else:
                table1.change(temp[int(choice3)])
        else:
            print("Неопознанная команда")
            continue
    if choice[0] != 1 and choice[0] != 2 and choice[0] != 3 and choice[0] !=4:
        print("Неопознанная команда")
        continue
