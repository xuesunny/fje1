# Abstract Product for Style
from abc import ABC, abstractmethod
from config import icon_family


class Style(ABC):
    @abstractmethod
    def display(self, prefix="", is_last=True):
        pass


# Concrete Products for Tree and Rectangle Styles
class TreeStyle(Style):
    @abstractmethod
    def display(self, prefix="", is_last=True):
        pass

    def add(self, component):
        pass


# Concrete Products for Tree and Rectangle Styles
class TreeStyleNode(TreeStyle, ABC):
    def __init__(self, name, children=None, index=0, total=0, icon=0):
        self.name = name
        self.pos = index
        self.total = total
        self.icon = icon_family[icon][0]
        self.children = children or []

    def display(self, prefix="", is_last=True):
        # Print the current node without prefix for the first one
        if prefix or self.name != "root":
            print(prefix + ("└── " if is_last else "├── ") + self.icon + " " + self.name)

        # Prepare the prefix for children
        if self.name != "root":  # 根节点不加前缀
            prefix += "     " if is_last else "│    "
            if self.icon != "":
                prefix += " "

        # Display the children
        for i in range(len(self.children)):
            is_last_child = i == len(self.children) - 1
            self.children[i].display(prefix, is_last_child)

    def add(self, component: TreeStyle):
        self.children.append(component)


# Concrete Products for Tree and Rectangle Styles
class TreeStyleLeaf(TreeStyle, ABC):
    def __init__(self, name, children=None, index=0, total=0, icon=0):
        self.name = name
        self.pos = index
        self.total = total
        self.icon = icon_family[icon][1]
        self.children = children or []

    def display(self, prefix="", is_last=True):
        # Print the current node without prefix for the first one
        if prefix or self.name != "root":
            print(prefix + ("└── " if is_last else "├── ") + self.icon + " " + self.name)


class RectangleStyle(Style):
    @abstractmethod
    def display(self, prefix="", is_last=True):
        pass

    def add(self, component):
        pass


class RectangleStyleNode(RectangleStyle):
    def __init__(self, name, children=None, index=0, total=0, icon=0):
        self.name = name
        self.pos = index
        self.total = total
        self.icon = icon_family[icon][0]
        self.children = children or []
        self.max_width = 40

    def display(self, prefix="", is_last=True):
        if self.name != "root":
            if self.pos == 1:
                line = f"┌─ {self.icon} {self.name} {'─' * (self.max_width - len(self.name)-len(prefix))}─┐"
            elif self.pos == self.total - 1:
                line = f"└─ {self.icon} {self.name} {'─' * (self.max_width - len(self.name)-len(prefix))}─┘"
            else:
                line = f"├─ {self.icon} {self.name} {'─' * (self.max_width - len(self.name)-len(prefix))}─┤"
            print(f"{prefix}{line}")

        for i in range(len(self.children)):
            last = i == len(self.children) - 1
            if self.name != "root" and self.children[i].pos != self.children[i].total - 1:
                new_prefix = prefix + "│   "
                if self.icon != "":
                    new_prefix += " "
            elif self.children[i].pos == self.children[i].total - 1:
                new_prefix = prefix + "└───"
                if self.icon != "":
                    new_prefix += "─"
            else:
                new_prefix = ""
            self.children[i].display(new_prefix, last)

    def add(self, component: TreeStyle):
        self.children.append(component)


class RectangleStyleLeaf(RectangleStyle):
    def __init__(self, name, children=None, index=0, total=0, icon=0):
        self.name = name
        self.pos = index
        self.total = total
        self.icon = icon_family[icon][1]
        self.children = children or []
        self.max_width = 40

    def display(self, prefix="", is_last=True):
        if self.name != "root":
            if self.pos == 1:
                line = f"┌─ {self.icon} {self.name} {'─' * (self.max_width - len(self.name)-len(prefix))}─┐"
            elif self.pos == self.total - 1:
                line = f"└─ {self.icon} {self.name} {'─' * (self.max_width - len(self.name)-len(prefix))}─┘"
            else:
                line = f"├─ {self.icon} {self.name} {'─' * (self.max_width - len(self.name)-len(prefix))}─┤"
            print(f"{prefix}{line}")