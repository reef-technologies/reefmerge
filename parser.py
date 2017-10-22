import ast
import astunparse


class Parser(object):
    @classmethod
    def parse_code(cls, code_text):
        return ast.parse(code_text)

    @classmethod
    def unparse_tree(cls, syntax_tree):
        return astunparse.unparse(syntax_tree)
