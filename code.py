import datetime
import random
# TODO: 實作日期功能 # 使用不同模式進行搜尋已搞定
importance_level = {'High': 0, 'Medium': 1, 'Low': 2}  # 需創建UI介面讓使用者選擇


class Task:
    importance = None  # TODO: 處理重要性
    date = None  # TODO: 處理日期
    tag = None  # TODO: 處理標籤
    repeat = None  # 任務重複性

    def __init__(self, name, mother=None, importance=None, date=None, tag=None, repeat=None):
        self.name = name
        self.mother = mother
        self.importance = importance
        self.date = date
        self.tag = tag
        self.repeat = repeat
        self.done = False  # 任務是否完成

    def __repr__(self):
        return f"{self.name}"

    def is_overdue(self):  # 確認這個任務是否過期
        if self.date is not None and self.date < datetime.date.today():
            return True
        return False

    def turn_to_lst(self):
        new_lst = TaskList(name=self.name, mother=self.mother)
        new_lst.importance = self.importance  # 要怎麼讓一個list的importance不同？
        new_lst.date = self.date
        new_lst.tag = self.tag
        new_lst.repeat = self.repeat
        return new_lst


class TaskList(Task):

    def __init__(self, name="Root", mother=None):
        super().__init__(name=name, mother=mother)
        self.name = name
        self.full = []  # 所有的Task
        self.tag_dict = {}  # 用於存儲標籤對應的任務

    def generate_random_task(self):  # 當你很無聊的時候可以啟用的功能
        task_names = ['Do the dishes', 'Complete assignment', 'Go for a run', 'Read a book', 'Call a friend']
        random_tasks = Task(random.choice(task_names), date=datetime.date.today(), tag='random')
        self.full.append(random_tasks)

    def add_task(self, name, tag=None, importance=None, date=None, repeat=None, done=False):
        for t in self:
            if t.name == name:
                raise ValueError  # 防止添加重複名稱的任務
        self.full.append(Task(name, self, importance, date, tag, repeat))

    def remove_all_done(self):
        for task in self:
            if task.done:
                self.remove_task(task.name)  # 移除所有已完成的任務

    def remove_task(self, name):
        try:
            self.full.remove(self[name])
        except ValueError:
            raise IndexError  # 當任務名稱不存在時拋出異常

    def finish_task(self, name):
        self[name].done = True  # 標記任務為已完成
        tracker.track_task(self[name])  # 通知 Tracker 任務已完成

    def rewrite(self, name, mode='name', content=None):
        if mode == "name":
            self[name].name = content  # 修改任務名稱
        if mode == "importance":
            self[name].importance = content  # 修改任務重要性
        if mode == "tag":
            self[name].tag = content  # 修改任務標籤

    def refresh_tag_dict(self):
        self.tag_dict = {}  # 重置標籤字典
        for t in self:
            if t.tag not in self.tag_dict:
                self.tag_dict.setdefault(t.tag, [t.name])
            else:
                self.tag_dict[t.tag].append(t.name)

    def get(self, mode='tag', content=None):
        if mode == 'tag':
            self.refresh_tag_dict()
            return self.tag_dict[content]  # 根據標籤獲取任務

    def get_all(self, mode=0):
        lst = []
        if mode == 0:
            for t in self:
                if type(t) is Task:
                    lst.append(t)
                elif type(t) is TaskList:
                    lst.append({t.name: t.get_all()})  # 獲取所有任務  # {t.name: t.get_all()} 是一個字典
            return lst
        if mode == 1:
            for t in self:
                if type(t) is Task:
                    lst.append(t.name)
                elif type(t) is TaskList:
                    lst.append(t.name)
                    for i in t.get_all(1):
                        lst.append(i if type(i) is str else i.name)  # 獲取所有任務名稱
            return lst

    def make_task_list(self, name):
        self[name] = self[name].turn_to_lst()
        # print("making_list", self[name])

    def export(self):
        pass

    def search(self, keyword, mode="name", in_sub=False):
        ans = []

        def match(task):
            if mode == "name" and keyword in task.name:
                return True
            if mode == "importance" and keyword == task.importance:
                return True
            if mode == "date" and keyword == task.date:
                return True
            if mode == "tag" and keyword == task.tag:
                return True
            return False

        if not in_sub:
            for task in self:
                if match(task):
                    ans.append(task.name)
            return ans

        if in_sub:
            for task in self.get_all(mode=1):
                if match(task):
                    ans.append(task.name)
            return ans

    def sort_with(self, mode='name', sub_mode='datetime'):  # TODO: 根據不同模式進行排序
        lst = []
        if mode == 'name':  # 找出所有任務後依照名稱直接排序
            lst = sorted(self.get_all(mode=1))
        if mode == 'importance':  # 透過搜尋找出不同重要性的任務
            lst = self.full.copy()
            lst.sort(key=lambda task: importance_level.get(task.importance, 3))
        if mode == 'date':
            lst = self.full.copy()
            lst.sort(key=lambda task: (task.date is None, task.date))
        if mode == 'tag':
            lst = self.full.copy()
            self.refresh_tag_dict()
            lst.sort(key=lambda task: self.tag_dict.keys())
        return lst

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
    def __init__(self):
        self.weekly_tasks = []
        self.monthly_tasks = []
        self.weekly_tags = {}
        self.monthly_tags = {}

    def track_task(self, task):
        today = datetime.date.today()  # 獲取今天的日期
        if task.done:
            if task.date:
                # 判斷任務是否在當週完成（7 天之內）
                if task.date.isocalendar()[1] == today.isocalendar()[1]:  # 當週
                    self.weekly_tasks.append(task)
                    if task.tag not in self.weekly_tags:
                        self.weekly_tags[task.tag] = [task]
                    else:
                        self.weekly_tags[task.tag].append(task)
                # 判斷任務是否在當月完成
                if today.year == task.date.year and today.month == task.date.month:
                    self.monthly_tasks.append(task)
                    if task.tag not in self.monthly_tags:
                        self.monthly_tags[task.tag] = [task]
                    else:
                        self.monthly_tags[task.tag].append(task)

    def generate_weekly_report(self):
        weekly_completed_task = len(self.weekly_tasks)
        report = f"Weekly completed tasks: {weekly_completed_task}\n"
        report += "Tasks by tag:\n"
        for tag, tasks in self.weekly_tags.items():
            report += f"  {tag}: {len(tasks)} tasks\n"
        return report

    def generate_monthly_report(self):
        monthly_completed_task = len(self.monthly_tasks)
        report = f"Monthly completed tasks: {monthly_completed_task}\n"
        report += "Tasks by tag:\n"
        for tag, tasks in self.monthly_tags.items():
            report += f"  {tag}: {len(tasks)} tasks\n"
        return report


def task_to_text(t, layer=0):
    if type(t) is Task:
        return f"{'    '*layer} - {t.name} - {t.tag} - {t.importance} - {t.date} - {t.repeat} - {t.done}"
    if type(t) is TaskList:
        ans = ""
        ans += f"{'    '*layer} - {t.name} - {t.tag} - {t.importance} - {t.date} - {t.repeat} - {t.done}" + '\n'
        for task in t:
            ans += task_to_text(task, layer + 1) + '\n'
        return ans


def save(root):  # 這應該只接受根TaskList
    f = open("save", "wt", encoding="utf-8")
    f.write(task_to_text(root).replace('\n\n', '\n'))
    f.close()


def read(file):
    file = open(file, "r", encoding="utf-8")
    root = TaskList()

    for line in file:
        line = line.strip(' _ ')
        name = line[0]
        importance = line[1]
        date = line[2]
        tag = line[3]
        repeat = line[4]
        done = True if line[5] == 'True' else False
        root.add_task(name, tag, importance, date, repeat, done)


# 創建一個 Tracker 實例
tracker = Tracker()

# 初始化根任務列表
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
root.add_task('task1', date=datetime.date.today(), tag="work")
root.add_task('task2', date=datetime.date.today(), tag="personal")
root.add_task('task3', date=datetime.date.today(), tag="personal")
root.finish_task('task1')

# 打印任務列表和搜尋結果
print(root)
print(root["Two"])
print(root.get_all(0))
print(root.get_all(1))
print(root.search("One", 'name'))
save(root)
print(task_to_text(root["One"]).replace('\n\n', '\n'))
print(root.full)
print(root['task1'].done)

# 生成並打印報告
print(tracker.generate_weekly_report())
