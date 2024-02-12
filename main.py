from typing import Any


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
            if 'А' <= name[i] <= 'Я' or 'A' <= name[i] <= 'Z':
                ch = name[i].lower()
            else:
                ch = name[i]
            if ch not in current.child:
                current.child[ch] = SearchTreeNode(str(current.name) + str(ch), current)
            current = current.child[ch]
            print(current.name)
            if i == len(name) - 1:
                current.indexes.add(index)
        return (current)

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
    def search(self, name) -> []:
        current = self.root
        for i in range(len(name)):
            if 'А' <= name[i] <= 'Я' or 'A' <= name[i] <= 'Z':
                ch = name[i].lower()
            else:
                ch = name[i]
            if ch not in current.child:
                return None
            current = current.child[ch]
            if i == len(name) - 1:
                return [current]

    def delete(self, name) -> bool:
        ans = self.search(name)
        if ans is None or len(ans) == 0:
            print("Не найдено таких записей")
            return
        if (len(ans) == 1):
            del ans[0].parent.child[ans[0].name[0]]
        else:
            print("Выберите какой номер вы хотите удалить(счет от 1):")
            for i, x in enumerate(ans):
                print(str(int(i + 1)) + " " + x.name + " " + str(x.number))
            index = int(input()) - 1
            del ans[index].parent.child[ans[index].name[-1]]


class Person:
    def __init__(self, name: SearchTreeNode, family_name: SearchTreeNode, fathers_name: SearchTreeNode,
                 organisation_name: SearchTreeNode, work_number: str, personal_number: str):
        self.name = name
        self.family_name = family_name
        self.fathers_name = fathers_name
        self.organisation_name = organisation_name
        self.work_number = work_number
        self.personal_number = personal_number


class Table:
    def __init__(self, pathfile):
        self.pathfile = pathfile
        self.persons_array = []
        self.names_Tree = NameSearchTree()
        self.family_names_tree = NameSearchTree()
        self.fathers_names_tree = NameSearchTree()
        self.organisation_names_tree = NameSearchTree()
        self.personal_number_to_person = {}
        self.work_number_to_person = {}
        with open(self.pathfile + '.txt', 'r') as file:
            for i, line in enumerate(file):
                name, family_name, fathers_name, organisation_name, work_number, personal_number = line.split(',')
                new_person = Person(self.names_Tree.insert(name, i), self.family_names_tree.insert(family_name, i),
                                    self.fathers_names_tree.insert(fathers_name, i),
                                    self.organisation_names_tree.insert(organisation_name, i),
                                    work_number, personal_number)
                self.persons_array.append(new_person)
                self.personal_number_to_person[personal_number] = self.persons_array[-1]
                self.work_number_to_person[work_number] = self.persons_array[-1]

    def insert_data(self, name: str, family_name: str, fathers_name: str, organisation_name: str, work_number: str,
                    personal_number: str) -> Person:
        i = len(self.persons_array)
        new_person = Person(self.names_Tree.insert(name, i), self.family_names_tree.insert(family_name, i),
                            self.fathers_names_tree.insert(fathers_name, i),
                            self.organisation_names_tree.insert(organisation_name, i),
                            work_number, personal_number)
        self.persons_array.append(new_person)
        self.personal_number_to_person[personal_number] = self.persons_array[-1]
        self.work_number_to_person[work_number] = self.persons_array[-1]
        with open(self.pathfile + '.txt', 'a') as file:
            file.write(
                name + ',' + family_name + ',' + fathers_name + ',' + organisation_name + ',' + work_number + ',' + personal_number + '\n')
            print("Данные успешно загружены")
            file.close()
        return new_person

    def _read_data(self, index: int) -> None:
        print(self.persons_array[index].family_name.name + " " + self.persons_array[index].name.name + " " +
              self.persons_array[index].fathers_name.name + ", " + self.persons_array[index].organisation_name.name + "     Рабочий номер:" +
              self.persons_array[index].work_number + "      Домашний номер:" + self.persons_array[index].personal_number)

    def read_all_data(self) -> None:
        for i in range (len(self.persons_array)):
            self._read_data(i)

    def _search_number(self, string) ->  Person:
        if string in self.personal_number_to_person:
            return self.personal_number_to_person[string]
        if string in self.work_number_to_person:
            return self.work_number_to_person[string]
    def _search_name(self, string) -> []:
        ans = []
        ans.extend(self.names_Tree.search(string).indexes)

        return ans


    def delete(self, index: int) -> None:
        return



print("Добро пожаловать в телефонный справочник")
table1 = Table("C:\\Users\\Батя и Я\\PycharmProjects\\Telephone_database\\base")
test = False
while (test):

    print(
        "Выберите действие(введите номер в терминал):" + '\n' + "1. Вывести весь справочник" + '\n' + "2. Вставить новый объект" + '\n' + "3. Найти запись в справочнике" + '\n' + "4. Редактировать справочник" + '\n' + "5. Удалить номер")
    choice = input()
    if (choice == 'Выход'):
        print("До новых встреч!")
        break
    if (choice == '1'):
        table1.read_all_data()
    if (choice == '2'):
        print("Введите имя владельца номера")
        name = input()
        print("Введите номер")
        number = input()
        table1.insert_data(name, number)
    if (choice == "3"):
        print("Введите номер или имя")
        string = input()
        table1.__search(string)

    testtree = NameSearchTree()
current = testtree.insert("Stas", 1)
# testtree.delete("Stas")
