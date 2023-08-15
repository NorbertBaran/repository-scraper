from tree_sitter import Language, Parser

Language.build_library(
  # Store the library in the `build` directory
  'build/languages.so',

  # Include one or more languages
  [
    'vendor/tree-sitter-python'
    # 'vendor/tree-sitter-java'
  ]
)

PYTHON = Language('build/languages.so', 'python')

def create_parser(lang):
    parser = Parser()
    parser.set_language(lang)
    return parser

def parse_code(path, lang):
    with open(path, "rb") as file:
        code = file.read()
    
    parser = create_parser(lang)
    tree = parser.parse(code)

    return tree