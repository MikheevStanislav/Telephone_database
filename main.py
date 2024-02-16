from typing import Any
import os


# Для начала создадим класс, который хранит из имен номера. Это будет Древо поиска, т.к пользователь может не знать
# имени искомого человека целиком. Если мы реализуем хранение пары имя -> номер то временная сложность при удобном
# для пользователя способе(к примеру есть имена Артем, Анатолий, Борис, пользователь воодит А, программа выдает
# Артема и Анатолия) ьудет O(N), а у дерева O(logN) P.S именно ради этой фичи нужен этот класс. Т.к. для пары телефон
# -> такая фича не нужна, мы можем использовать простую хэштаблицу.
class SearchTreeNode:
    def __init__(self, name=None, parent=None, person=None):
        self.name = name  # Имя конкретной ноды
        self.parent = parent
        self.child = {}  # Хэштаблица всех сыновей ноды
        self.person = person
        self.indexes = set()


class NameSearchTree:
    def __init__(self):
        self.root = SearchTreeNode("")  # создаем корень. Корень не будет иметь имени

    # метод добавления данных в древо
    def insert(self, name, index) -> SearchTreeNode:
        current = self.root  # заводим переменную текущей ноды
        for i in range(
                len(name)):  # проходимся по всему имени. Для каждой буквы делаем ноду, имя которой являются все
            # буквы то текущей буквы. Если буква последняя, даем ноде индекс
            ch = name[i]
            if ch not in current.child:
                current.child[ch] = SearchTreeNode(str(current.name) + str(ch), current)
            current = current.child[ch]
            if i == len(name) - 1:
                current.indexes.add(index)
        return current

    # Вспомогательный метод, для поиска всех листов конкретной вершины. Нужен для поиска по древу.
    def _find_leaf(self, node) -> []:
        if node is None:
            return []
        if len(node.child) == 0:
            return [node]
        else:
            leaf_nodes = []
            leaf_nodes.extend(self._find_leaf(node.left))
            leaf_nodes.extend(self._find_leaf(node.right))
            return leaf_nodes

    # Возвращает все подходящие под описание объекты
    def search(self, name: str) -> []:
        current = self.root
        for i in range(len(name)):
            ch = name[i]
            if ch not in current.child:
                return None
            current = current.child[ch]
            if i == len(name) - 1:
                if(current.child is not None):
                    return(self._find_leaf(current))
                else:
                    return [current]

    def delete(self, node: SearchTreeNode) -> bool:
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
    def __init__(self, name: SearchTreeNode, family_name: SearchTreeNode, fathers_name: SearchTreeNode,
                 organisation_name: SearchTreeNode, work_number: str, personal_number: str, index: int):
        self.name = name
        self.family_name = family_name
        self.fathers_name = fathers_name
        self.organisation_name = organisation_name
        self.work_number = work_number
        self.personal_number = personal_number
        self.index = index


class Table:
    def __init__(self, pathfile):
        self.pathfile = pathfile
        self.persons_array = []
        self.names_tree = NameSearchTree()
        self.family_names_tree = NameSearchTree()
        self.fathers_names_tree = NameSearchTree()
        self.organisation_names_tree = NameSearchTree()
        self.personal_number_to_person = {}
        self.work_number_to_person = {}
        with open(self.pathfile + '.txt', 'r', encoding='utf-8') as file:
            for i, line in enumerate(file):
                if line == "\n":
                    continue
                name, family_name, fathers_name, organisation_name, work_number, personal_number = line.split(',')
                new_person = Person(self.names_tree.insert(name, i), self.family_names_tree.insert(family_name, i),
                                    self.fathers_names_tree.insert(fathers_name, i),
                                    self.organisation_names_tree.insert(organisation_name, i),
                                    work_number, personal_number, i)
                self.persons_array.append(new_person)
                self.personal_number_to_person[personal_number[:-1]] = self.persons_array[-1]
                self.work_number_to_person[work_number] = self.persons_array[-1]

    def insert_data(self, name: str, family_name: str, fathers_name: str, organisation_name: str, work_number: str,
                    personal_number: str) -> Person:
        i = len(self.persons_array)
        new_person = Person(self.names_tree.insert(name, i), self.family_names_tree.insert(family_name, i),
                            self.fathers_names_tree.insert(fathers_name, i),
                            self.organisation_names_tree.insert(organisation_name, i),
                            work_number, personal_number, i)
        if self._search_father_name(fathers_name, self._search_family(family_name, self._search_name(name))) is not None:
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

    def _read_data(self, index: int) -> None:
        print(str(index) + ":" + self.persons_array[index].family_name.name + " " + self.persons_array[
            index].name.name + " " +
              self.persons_array[index].fathers_name.name + ", " + self.persons_array[
                  index].organisation_name.name + "     Рабочий номер:" +
              self.persons_array[index].work_number + "      Домашний номер:" + self.persons_array[
                  index].personal_number)

    def read_all_data(self) -> None:
        for i in range(len(self.persons_array)):
            self._read_data(i)

    def _search_number(self, string: str) -> Person:
        if string in self.personal_number_to_person:
            return self.personal_number_to_person[string]
        if string in self.work_number_to_person:
            return self.work_number_to_person[string]
        else:
            print("Такого номера не найдено в базе данных")

    def _search_name(self, string: str, mas=None) -> []:
        ans = []
        if self.names_tree.search(string) is None:
            return
        for x in self.names_tree.search(string):
            for i in x.indexes:
                if mas == None:
                    ans.append(i)
                else:
                    if i in mas:
                        ans.append(i)
        return ans

    def _search_family(self, string, mas=None) -> []:
        ans = []
        if self.family_names_tree.search(string) is None:
            return
        for x in self.family_names_tree.search(string):
            for i in x.indexes:
                if mas == None:
                    ans.append(i)
                else:
                    if i in mas:
                        ans.append(i)
        return ans

    def _search_father_name(self, string, mas=None) -> []:
        ans = []
        if self.fathers_names_tree.search(string) is None:
            return
        for x in self.fathers_names_tree.search(string):
            for i in x.indexes:
                if mas == None:
                    ans.append(i)
                else:
                    if i in mas:
                        ans.append(i)
        return ans

    def _search_organisation_name(self, string, mas=None) -> []:
        ans = []
        if self.organisations_tree.search(string) is None:
            return
        for x in self.organisation_names_tree.search(string):
            if mas == None:
                ans.append(x)
            else:
                if x in mas:
                    ans.append(x)
        return ans

    def change(self, index: int):
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
            if(temp.name == string):
                print("Имя тоже что и было")
            else:
                self.persons_array[index].organisation_name = self.organisation_names_tree.insert(string, index)
                self.organisation_names_tree.delete(temp)
        print("Введите рабочий номер телефона(не вводите ничего если оставить неизмененным)")
        string = input()
        if string:
            self.work_number_to_person[string] = self.persons_array[index]
            del self.work_number_to_person[self.persons_array[index].work_number]
            self.persons_array[index].work_number = string

        print("Введите домашний номер телефона(не вводите ничего если оставить неизмененным)")
        string = input()
        if string:
            self.personal_number_to_person[string] = self.persons_array[index]
            del self.personal_number_to_person[self.persons_array[index].personal_number]
            self.persons_array[index].personal_number = string

    def _save_changes(self):
        with open(self.pathfile + '.txt', 'w', encoding='utf-8') as file:
            for i in range(len(self.persons_array)):
                file.write(
                    self.persons_array[i].name.name + ", " + self.persons_array[i].family_name.name + ", " + self.persons_array[
                        i].fathers_name.name +
                    "," + self.persons_array[i].organisation_name.name + "," + self.persons_array[i].work_number + "," +
                    self.persons_array[i].personal_number + "\n")


print("Добро пожаловать в телефонный справочник")
table1 = Table("base")
while (True):

    print(
        "Выберите действие(введите номер в терминал):" + '\n' + "1. Вывести весь справочник" + '\n' +
        "2. Вставить новый объект" + '\n' + "3. Найти запись в справочнике" + '\n' + "4. Редактировать запись" +
        '\n' + "5. Удалить номер" + '\n' + "6. Выход")
    choice = input()
    if (choice == '6'):
        print("До новых встреч!")
        table1._save_changes()
        break
    if (choice == '1'):
        table1.read_all_data()
    if (choice == '2'):
        mas = []
        print("Введите фамилию владельца номера")
        mas.append(input())
        print("Введите имя владельца номера")
        mas.append(input())
        print("Введите отчество")
        mas.append(input())
        print("Введите название организации")
        mas.append(input())
        print("Введите рабочий номер")
        mas.append(input())
        print("Введите домашний номер")
        mas.append(input())
        for i in range(mas):
            if(mas[i] == ""):
                mas[i] = "_"
        table1.insert_data(mas[1], mas[0], mas[2], mas[3], mas[4], mas[5])
    if (choice == "3"):




