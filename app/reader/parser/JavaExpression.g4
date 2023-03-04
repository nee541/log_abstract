grammar JavaExpression;

// Lexer rules

LPAREN : '(';
RPAREN : ')';
COMMA : ',';
DOT : '.';

PLUS : '+';
MINUS : '-';
MULT : '*';
DIV : '/';
MOD : '%';

BITWISE_AND : '&';
BITWISE_OR : '|';
XOR : '^';
SHIFT_LEFT : '<<';
SHIFT_RIGHT : '>>';

GREATER_THAN : '>';
LESS_THAN : '<';
GREATER_THAN_OR_EQUAL_TO : '>=';
LESS_THAN_OR_EQUAL_TO : '<=';
EQUALS : '==';
NOT_EQUALS : '!=';
INSTANCEOF : 'instanceof';

LOGICAL_AND : '&&';
LOGICAL_OR : '||';
QUESTION_MARK : '?';
COLON : ':';

WHITESPACE : [ \t\r\n]+ -> skip ;

IDENTIFIER : [a-zA-Z_] [a-zA-Z0-9_]* ;

NULL_LITERAL : 'null';

// REGULAR_EXPRESSION : '/' ( options {greedy=false;} : . )* '/' ;

// Parser rules

expression:
    literal
    | IDENTIFIER
    | functionCall
    | IDENTIFIER functionCall
    | MULT expression
    | '(' IDENTIFIER ')' expression
    | expression '.' IDENTIFIER
    | expression '.' functionCall
    | '(' expression ')'
//    | expression '[' INTEGER_LITERAL ']'
    | expression '[' expression ']'
//    | REGULAR_EXPRESSION
    | expression PLUS expression
    | expression MINUS expression
    | expression MULT expression
    | expression DIV expression
    | expression MOD expression
    | expression BITWISE_AND expression
    | expression BITWISE_OR expression
    | expression XOR expression
    | expression SHIFT_LEFT expression
    | expression SHIFT_RIGHT expression
    | expression GREATER_THAN expression
    | expression LESS_THAN expression
    | expression GREATER_THAN_OR_EQUAL_TO expression
    | expression LESS_THAN_OR_EQUAL_TO expression
    | expression EQUALS expression
    | expression NOT_EQUALS expression
    | expression LOGICAL_AND expression
    | expression LOGICAL_OR expression
    | expression QUESTION_MARK expression COLON expression
    | expression INSTANCEOF IDENTIFIER
    ;

literal:
    INTEGER_LITERAL
    | FLOATING_POINT_LITERAL
    | BOOLEAN_LITERAL
    | CHARACTER_LITERAL
    | STRING_LITERAL
    | NULL_LITERAL
    ;

functionCall:
    IDENTIFIER '(' arguments? ')'
//    | functionCall '(' arguments? ')'
//    | IDENTIFIER '.' IDENTIFIER '(' arguments? ')'
//    | functionCall '.' IDENTIFIER '(' arguments? ')'
    ;

arguments:
    expression (',' expression)*
    ;

// Lexer rules for literals

INTEGER_LITERAL :
    DECIMAL_LITERAL
    | HEX_LITERAL
    | OCTAL_LITERAL
    | BINARY_LITERAL
    ;

fragment DECIMAL_LITERAL :
    '0' | '1'..'9' ('_'? '0'..'9')*
    ;

fragment HEX_LITERAL :
    '0' [xX] ('_'? [0-9a-fA-F])+ 
    ;

fragment OCTAL_LITERAL :
    '0' ('_'? [0-7])+ 
    ;

fragment BINARY_LITERAL :
    '0' [bB] ('_'? [01])+ 
    ;

FLOATING_POINT_LITERAL :
    DECIMAL_FLOATING_POINT_LITERAL
    | HEX_FLOATING_POINT_LITERAL
    ;

fragment DECIMAL_FLOATING_POINT_LITERAL :
    ('0'..'9')+ ('_'? ('.' ('0'..'9')* EXPONENT? | EXPONENT) | 'f' | 'F' | 'd' | 'D')
    ;

fragment HEX_FLOATING_POINT_LITERAL :
    ('0' [xX] [0-9a-fA-F]+ ('_'? [0-9a-fA-F])*) ('.' [0-9a-fA-F]* EXPONENT? | EXPONENT)
    ;

fragment EXPONENT :
    [eE] [+-]? ('_'? [0-9])+ 
    ;

BOOLEAN_LITERAL :
    'true' | 'false'
    ;

CHARACTER_LITERAL: '\'' ( EscapeSequence | ~['\\\r\n] ) '\'' ;
STRING_LITERAL: '"' ( EscapeSequence | ~["\\\r\n] )* '"' ;

fragment EscapeSequence: '\\' [btnfr"'\\] | UnicodeEscape;

fragment UnicodeEscape: '\\' 'u' HexDigit HexDigit HexDigit HexDigit;

fragment HexDigit: [0-9a-fA-F];
