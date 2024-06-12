import json
from abc import ABC, abstractmethod
from composite import *
from config import icon_family


# Abstract Factory for Style
class StyleFactory(ABC):
    @abstractmethod
    def create_style(self, type, name, index, total, icon):
        pass


# Concrete Factories for Tree and Rectangle Styles
class TreeStyleFactory(StyleFactory):
    def create_style(self, type, name, index, total, icon):
        if type == "node":
            return TreeStyleNode(name, None, index, total, icon)
        elif type == "leaf":
            return TreeStyleLeaf(name, None, index, total, icon)
        else:
            return None


class RectangleStyleFactory(StyleFactory):
    def create_style(self, type, name, index, total, icon):
        if type == "node":
            return RectangleStyleNode(name, None, index, total, icon)
        elif type == "leaf":
            return RectangleStyleLeaf(name, None, index, total, icon)
        else:
            return None
