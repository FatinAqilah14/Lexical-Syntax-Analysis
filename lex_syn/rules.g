grammar rules;		
prog:	(expr NEWLINE)* ;
expr:	expr ('*'|'/') expr
    |	expr ('+'|'-') expr
    |   IDENTIFIER
    |	INT
    |	'(' expr ')'
    ;
NEWLINE : [\r\n]+ ;

IDENTIFIER : [a-zA-Z_][a-zA-Z0-9_]*;
INT     : [0-9]+ ;