import os
import glob
from tree_sitter import Node, Tree
from src.extractor.parser.components import Component, Import, Class, Function, Decorator, Call, CodeBlock, Module, Repository
from src.extractor.parser.parser import parse_code, PYTHON

def process_repository(github_id, name, url, path):
    modules = glob.glob(os.path.join(path, "**/*.py"), recursive=True)
    processed_modules = []
    for module in modules:
        components = process_tree(parse_code(module, PYTHON))
        processed_modules.append(Module(module, components))
    
    repository = Repository(github_id, name, url, processed_modules)
    return repository

def process_tree(tree: Tree) -> list[Component]:
    components = []
    code_lines = []
    for node in tree.root_node.children:
        result = process_node(node)
        if result:
            if type(result) == str:
                code_lines.append(result)
            else:
                components.append(result)
    components.append(CodeBlock('\n'.join(code_lines)))
    return components

def process_node(node: Node) -> Component:
    if node.type == "import_from_statement":
        return process_import(node)
    elif node.type == "class_definition"  or (node.type == "decorated_definition" and node.child_by_field_name('definition').type == "class_definition"):
        return process_class(node)
    elif node.type == "function_definition" or (node.type == "decorated_definition" and node.child_by_field_name('definition').type == "function_definition"):
        return process_function(node)
    elif node.type == "expression_statement":
        return process_code_line(node)

def process_import(node: Node) -> Import:
    module = node.child_by_field_name('module_name').text.decode('utf-8')
    imports = [child.text.decode('utf-8') for child in node.children_by_field_name('name')]
    return Import(module, imports)

def process_code_line(node: Node) -> str:
    return node.text.decode('utf-8')

def process_decorator(node: Node) -> Decorator:
    node = node.children[1]
    calls = []

    while node:

        if node.type == "identifier":
            calls.append(Call(node.text.decode('utf-8')))
            node = None
        
        elif node.type == "call":
            func = node.child_by_field_name('function')
            args = [child.text.decode('utf-8') for child in node.child_by_field_name('arguments').children if child.type == "identifier"]
            
            if func.type == "identifier":
                calls.append(Call(func.text.decode('utf-8'), args))
                node = None
            
            elif func.type == "attribute":
                calls.append(Call(func.child_by_field_name('attribute').text.decode('utf-8'), args))
                node = func.child_by_field_name('object')
        else:
            node = None

    calls.reverse()
    return Decorator(calls)

def process_function(node: Node) -> Function:
    decorators = []
    
    if node.type == "decorated_definition":
        decorators = [process_decorator(child) for child in node.children if child.type == 'decorator']
        node = node.child_by_field_name('definition')
    
    name = node.child_by_field_name('name').text.decode('utf-8')
    args = [child.text.decode('utf-8') for child in node.child_by_field_name('parameters').children if child.type == 'identifier']
    body = node.child_by_field_name('body').text.decode('utf-8')
    
    return Function(name, args, body, decorators)

def process_class(node: Node) -> Class:
    decorators = []
    
    if node.type == "decorated_definition":
        decorators = [process_decorator(child) for child in node.children if child.type == 'decorator']
        node = node.child_by_field_name('definition')

    name = node.child_by_field_name('name').text.decode('utf-8')
    superclasses = []
    if node.child_by_field_name('superclasses'):
        superclasses = [child.text.decode('utf-8') for child in node.child_by_field_name('superclasses').children if child.type == "identifier"]
    attributes, methods = set(), []
    
    def process_body(body: Node):
        for node in body.children:
            process_body_node(node)

    def process_body_node(node: Node):
        if node.type == "function_definition":
            process_method(node)
            process_attributes(node)
    
    def process_attributes(node: Node):
        body = node.child_by_field_name('body')
        for expression in body.children:
            try:
                assignment = expression.children[0]
                left = assignment.child_by_field_name('left')
                obj = left.child_by_field_name('object')
                attribute = left.child_by_field_name('attribute')
                if obj.text.decode('utf-8') == 'self':
                    attributes.add(attribute.text.decode('utf-8'))
            except:
                pass

    def process_method(node: Node):
        methods.append(process_function(node))
    
    process_body(node.child_by_field_name('body'))
    return Class(name, superclasses, list(attributes), methods, decorators)
