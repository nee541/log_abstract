# Generated from JavaExpression.g4 by ANTLR 4.12.0
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .JavaExpressionParser import JavaExpressionParser
else:
    from JavaExpressionParser import JavaExpressionParser

# This class defines a complete listener for a parse tree produced by JavaExpressionParser.
class JavaExpressionListener(ParseTreeListener):
    
    def __init__(self):
        self.nest_depth = 0
        self.str_literals = []
        super().__init__()

    # Enter a parse tree produced by JavaExpressionParser#expression.
    def enterExpression(self, ctx:JavaExpressionParser.ExpressionContext):
        pass

    # Exit a parse tree produced by JavaExpressionParser#expression.
    def exitExpression(self, ctx:JavaExpressionParser.ExpressionContext):
        pass


    # Enter a parse tree produced by JavaExpressionParser#literal.
    def enterLiteral(self, ctx:JavaExpressionParser.LiteralContext):
        str_literal = ctx.STRING_LITERAL()
        if str_literal:
            self.str_literals.append(str(str_literal).strip('"'))

    # Exit a parse tree produced by JavaExpressionParser#literal.
    def exitLiteral(self, ctx:JavaExpressionParser.LiteralContext):
        pass


    # Enter a parse tree produced by JavaExpressionParser#functionCall.
    def enterFunctionCall(self, ctx:JavaExpressionParser.FunctionCallContext):
        self.nest_depth += 1
        if self.nest_depth == 1:
            self.log_level = ctx.IDENTIFIER().getText()

    # Exit a parse tree produced by JavaExpressionParser#functionCall.
    def exitFunctionCall(self, ctx:JavaExpressionParser.FunctionCallContext):
        self.nest_depth -= 1
        if self.nest_depth == 0:
            self.template = ''.join(self.str_literals)

    # Enter a parse tree produced by JavaExpressionParser#arguments.
    def enterArguments(self, ctx:JavaExpressionParser.ArgumentsContext):
        pass

    # Exit a parse tree produced by JavaExpressionParser#arguments.
    def exitArguments(self, ctx:JavaExpressionParser.ArgumentsContext):
        pass




del JavaExpressionParser