class Component:
    pass

class Import(Component):
    def __init__(self, module: str, imports: list[str]) -> None:
        self.module = module
        self.imports = imports
    
    def __str__(self) -> str:
        return f"Import({self.module}, {self.imports})"
    
    def __dict__(self):
        return {
            'type': self.__class__.__name__,
            'module': self.module,
            'imports': self.imports
        }

class CodeBlock(Component):
    def __init__(self, code: str) -> None:
        self.code = code

    def __str__(self) -> str:
        return f"CodeBlock({self.code})"
    
    def __dict__(self):
        return {
            'type': self.__class__.__name__,
            'code': self.code
        }

class Call(Component):
    def __init__(self, name: str, args: list[str] = None) -> None:
        self.name = name
        self.args = args

    def __str__(self) -> str:
        return f"Call({self.name}, {self.args})"
    
    def __dict__(self):
        return {
            'type': self.__class__.__name__,
            "name": self.name,
            "args": self.args
        }

class Decorator(Component):
    def __init__(self, calls: list[Call]) -> None:
        self.calls = calls

    def __str__(self) -> str:
        return f"Decorator({self.calls})"
    
    def __dict__(self):
        return {
            'type': self.__class__.__name__,
            'calls': [call.__dict__() for call in self.calls]
        }

class Function(Component):
    def __init__(self, name: str, args: list[str], body:CodeBlock, decorators: list[Decorator] = []) -> None:
        self.decorators = decorators
        self.name = name
        self.args = args
        self.body = body
    
    def __str__(self) -> str:
        return f"Function({self.decorators}, {self.name}, {self.args}, {self.body})"
    
    def __dict__(self):
        return {
            'type': self.__class__.__name__,
            'decorators': [decorator.__dict__() for decorator in self.decorators],
            'name': self.name,
            'args': self.args,
            'body': self.body
        }

class Class(Component):
    def __init__(self, name: str, superclasses: list[str], attributes: list[str], methods: list[Function], decorators: list[Decorator] = []) -> None:
        self.decorators = decorators
        self.name = name
        self.superclasses = superclasses
        self.attributes = attributes
        self.methods = methods
    
    def __str__(self) -> str:
        return f"Class({self.decorators}, {self.name}, {self.superclasses}, {self.attributes}, {self.methods})"
    
    def __dict__(self):
        return {
            'type': self.__class__.__name__,
            "decorators": [decorator.__dict__() for decorator in self.decorators],
            "name": self.name,
            "superclasses": self.superclasses,
            "attributes": self.attributes,
            "methods": [method.__dict__() for method in self.methods]
        }

class Module:
    def __init__(self, path: str, components: list[Component] = []) -> None:
        self._id = None
        self.path = path
        self.components = components
    
    def __str__(self) -> str:
        return f"Module({self.path}, {self.components})"
    
    def __dict__ (self):
        try:
            return {
                'type': self.__class__.__name__,
                "path": self.path,
                "components": [component.__dict__() for component in self.components]
            }
        except Exception as e:
            print(e)
            print(f'Path: {self.path}')

class Repository:
    def __init__(self, github_id: int, name: str, url: str, modules: list[Module]) -> None:
        self._id = None
        self.github_id = github_id
        self.name = name
        self.url = url
        self.modules = modules
    
    def __str__(self) -> str:
        return f"Repository({self.modules})"
    
    def __dict__ (self):
        return {
            'type': self.__class__.__name__,
            'github_id': self.github_id,
            'name': self.name,
            'url': self.url,
            # 'modules': [module.__dict__() for module in self.modules]
        }