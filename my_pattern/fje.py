from abc import ABC
import argparse
from Abstractfactory import *
from composite import *


# Abstract Builder Interface
class Builder(ABC):

    @abstractmethod
    def add_object(self, name, parent=None):
        pass

    @abstractmethod
    def add_leaf(self, name, value=None, parent=None):
        pass

    @abstractmethod
    def get_total(self, obj):
        pass

    @abstractmethod
    def set_total(self, total):
        pass

    @abstractmethod
    def display(self):
        pass


# Concrete Builder Class
class JsonBuilder(Builder, ABC):
    def __init__(self, name, factory: StyleFactory, icon: int):
        self.factory = factory
        self.icon = icon
        self.name = name
        self.root = self.factory.create_style("node", name, 0, 0, 0)
        self.total_nodes = 0
        self.position = 0
        self.modify = 0

    def add_object(self, name, parent=None):
        self.position += 1
        obj = self.factory.create_style("node", name, self.position, self.total_nodes, self.icon)
        if parent:
            parent.add(obj)
        else:
            self.root.add(obj)
        return obj

    def add_leaf(self, name, value=None, parent=None):
        self.position += 1
        leaf = self.factory.create_style("leaf", name, self.position, self.total_nodes, self.icon)
        if parent:
            parent.add(leaf)
        else:
            self.root.add(leaf)
        return leaf

    # 获取节点总数
    def get_total(self, obj):
        if isinstance(obj, dict):
            count = 1
            for key, value in obj.items():
                num = self.get_total(value)
                count = count + num
            return count
        else:
            return 1

    def set_total(self, total):
        self.total_nodes = total
        self.modify = 1

    def display(self):
        self.root.display()

# Director Class
class Director:
    def __init__(self, builder: Builder):
        self.builder = builder

    # Convert input object to DataNode
    def convert_to_data_node(self, data, parent=None):
        if parent is None and self.builder.modify == 0:
            total = self.builder.get_total(data)
            self.builder.set_total(total)
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    obj = self.builder.add_object(key, parent)
                    self.convert_to_data_node(value, obj)
                elif value is not None:
                    self.builder.add_leaf(key + ": " + value, value=value, parent=parent)
                else:
                    self.builder.add_leaf(key, value=value, parent=parent)
        elif isinstance(data, list):
            for index, item in enumerate(data):
                if isinstance(item, (dict, list)):
                    obj = self.builder.add_object(f"[{index}]", parent)
                    self.convert_to_data_node(item, obj)
                else:
                    self.builder.add_leaf(f"[{index}]", value=item, parent=parent)
        else:
            self.builder.add_leaf(str(data), value=data, parent=parent)
        # 输出
        if parent is None:
            self.builder.display()


def main():
    parser = argparse.ArgumentParser(description='Funny JSON Explorer (FJE)')
    parser.add_argument('-f', '--file', required=True, help='JSON file to be read')
    parser.add_argument('-s', '--style', choices=['tree', 'rectangle'], required=True, help='Visualization style')
    parser.add_argument('-i', '--icon', choices=list(map(str, range(len(icon_family)))), required=True, help='Icon set to use')
    args = parser.parse_args()

    with open(args.file, "r") as file:
        input_json = file.read()

    # Parse the JSON input
    json_data = json.loads(input_json)

    factory = TreeStyleFactory()
    if args.style == 'tree':
        factory = TreeStyleFactory()
    elif args.style == 'rectangle':
        factory = RectangleStyleFactory()

    icon = int(args.icon)
    builder = JsonBuilder("root", factory, icon)
    director = Director(builder)
    director.convert_to_data_node(json_data, None)

if __name__ == "__main__":
    main()
