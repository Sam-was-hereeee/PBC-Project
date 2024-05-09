import datetime
import random
# TODO: search with different modes, implement datetime


class Task:
    importance = None  # TODO: work with importance
    date = None  # TODO: work with dates
    tag = None  # TODO: work with tags
    repeat = None

    def __init__(self, name, mother=None, importance=None, date=None, tag=None, repeat=None):
        self.name = name
        self.mother = mother
        self.importance = importance
        self.date = date
        self.tag = tag
        self.repeat = repeat
        self.done = False

    def __repr__(self):
        return f"{self.name}"

    def turn_to_lst(self):
        new_lst = TaskList(name=self.name, mother=self.mother)
        new_lst.importance = self.importance
        new_lst.date = self.date
        new_lst.tag = self.tag
        new_lst.repeat = self.repeat
        # print("new list:", new_lst)
        return new_lst


class TaskList(Task):

    def __init__(self, name="Root", mother=None):
        super().__init__(name=name, mother=mother)
        self.name = name
        self.full = []
        self.tag_dict = {}

    def random_task(self):  # TODO: generate random task
        pass

    def add_task(self, name, tag=None, importance=None, date=None, repeat=None):
        for t in self:
            if t.name == name:
                raise ValueError
        self.full.append(Task(name, self, importance, tag, date, repeat))

    def remove_all_done(self):
        for task in self:
            if task.done:
                self.remove_task(task.name)

    def remove_task(self, name):
        try:
            self.full.remove(self[name])
        except ValueError:
            raise IndexError

    def finish_task(self, name):
        self[name].done = True

    def write(self, name, mode='name', content=None):
        if mode == "name":
            self[name].name = content
        if mode == "importance":
            self[name].importance = content
        if mode == "tag":
            self[name].tag = content

    def refresh_tag_dict(self):
        self.tag_dict = {}
        for t in self:
            if t.tag not in self.tag_dict:
                self.tag_dict.setdefault(t.tag, [t.name])
            else:
                self.tag_dict[t.tag].append(t.name)

    def get(self, mode='tag', content=None):
        if mode == 'tag':
            self.refresh_tag_dict()
            return self.tag_dict[content]

    def get_all(self, mode=0):
        lst = []
        if mode == 0:
            for t in self:
                if type(t) is Task:
                    lst.append(t)
                elif type(t) is TaskList:
                    lst.append({t.name: t.get_all()})
            return lst
        if mode == 1:
            for t in self:
                if type(t) is Task:
                    lst.append(t.name)
                elif type(t) is TaskList:
                    lst.append(t.name)
                    for i in t.get_all(1):
                        lst.append(i if type(i) is str else i.name)
            return lst

    def make_task_list(self, name):
        self[name] = self[name].turn_to_lst()
        # print("making_list", self[name])

    def export(self):
        pass

    def search(self, keyword, mode="name", in_sub=False):
        ans = []
        if not in_sub:
            for task in self:
                if keyword in task.name:
                    ans.append(task.name)
            return ans
        if in_sub:
            for task in self.get_all(mode=1):
                if keyword in task:
                    ans.append(task)
            return ans

    def sort(self):  # TODO: sort with different modes
        pass

    def __repr__(self):
        return f"{self.name}: {[i for i in self.full]}"

    def __iter__(self):
        self.current = 0
        return self

    def __next__(self):
        try:
            self.current += 1
            return self.full[self.current - 1]
        except IndexError:
            raise StopIteration

    def __setitem__(self, key, value):
        for i in self.full:
            if i.name == key:
                self.remove_task(i.name)
                self.full.append(value)

    def __contains__(self, name):
        return name in [i.name for i in self.full]

    def __getitem__(self, index):
        for i in self.full:
            if i.name == index:
                return i
        raise IndexError


class Viewer:

    def __init__(self, init):
        self.current = init


class Tracker:
    pass


def task_to_text(t, layer=0):
    if type(t) is Task:
        return f"{"    "*layer} - {t.name} - {t.tag} - {t.importance} - {t.date} - {t.repeat} - {t.done}"
    if type(t) is TaskList:
        ans = ""
        ans += f"{"    "*layer} - {t.name} - {t.tag} - {t.importance} - {t.date} - {t.repeat} - {t.done}" + '\n'
        for task in t:
            ans += task_to_text(task, layer + 1) + '\n'
        return ans


def save(root):  # this should only take in the root TaskList
    f = open("save", "wt", encoding="utf-8")
    f.write(task_to_text(root).replace('\n\n', '\n'))
    f.close()


def read(file):  # TODO: read from save file
    pass


root = TaskList()
root.add_task("One")
root.add_task("Two")
root.add_task("Three")
root.add_task("Four")
root.add_task("Five")
root.make_task_list("One")
root["One"].add_task("1:1")
root["One"].make_task_list("1:1")
root["One"].add_task("1:2")
root["One"].add_task("1:3")
root["One"]["1:1"].add_task("1:1:1")
print(root)
print(root["Two"])
print(root.get_all(0))
print(root.get_all(1))
print(root.search("One"))
save(root)
print(task_to_text(root["One"]).replace('\n\n', '\n'))