import ply.lex as lex
import ply.yacc as yacc

"""
ply is an implementation of lexer and parser
lex is lexer generator // extracts token from the input condition
yacc is parser generator // validates the syntax against the grammar and generates syntax tree 
"""

tokens = [
	'INT',
	'COLUMNNAME',
	'FLOAT',
	'GREATERTHAN',
	'LESSTHAN',
	'EQUALS',
	'NOTEQUALS',
	'GREATERTHANEQUAL',
	'LESSTHANEQUAL',
	'AND',
	'OR',
	'NOT',
	'STRING',
	'LPAREN',
	'RPAREN'
]

''' Simple tokens definition below '''
t_GREATERTHANEQUAL = r'\>='
t_LESSTHANEQUAL = r'\<='
t_GREATERTHAN = r'\>'
t_LESSTHAN = r'\<'
t_EQUALS = r'\=='
t_NOTEQUALS = r'\!='
t_AND = r'AND|and'
t_OR = r'OR|or'
t_NOT = r'NOT|not'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ignore = ' '

"""Complex tokens are defined below"""


def t_STRING(t):
	r'\"[a-zA-Z0-9_\-\s]*\"'
	t.type = 'STRING'
	return t


def t_COLUMNNAME(t):
	r'\#[a-zA-Z0-9]*'
	t.type = 'COLUMNNAME'
	return t


def t_FLOAT(t):
	r'\d+\.\d+'
	t.value = t.value
	return t


def t_INT(t):
	r'\d+'
	t.value = t.value
	return t


def t_error(t):
	print(t)
	print("Illegal characters")
	raise (f'Illegal character {t}')
	# print("Illegal characters in the condition")
	t.lexer.skip(1)


lexer = lex.lex()


def p_select(p):
	'''

	select : simpleexpression
		   | empty


	'''
	if len(p) == 2:
		p[0] = p[1]
	if len(p) == 3:
		p[0] = (p[2], p[1], p[3])


def p_value(p):
	'''
	value : INT
		  | FLOAT

	'''
	p[0] = p[1]


def p_string(p):
	'''
	string : STRING

	'''
	p[0] = p[1]


def p_attribute(p):
	'''
	attribute : COLUMNNAME

	'''
	p[0] = p[1]


def p_relational(p):
	'''
	relational : GREATERTHANEQUAL
			   | LESSTHANEQUAL
			   | GREATERTHAN
			   | LESSTHAN
			   | NOTEQUALS
			   | EQUALS

	'''
	p[0] = p[1]


def p_logical_op(p):
	'''
		logical : AND
				| OR
				| NOT

		'''
	p[0] = p[1]


def p_simpleexpression(p):
	'''

	simpleexpression : attribute relational value
			   | attribute relational string
			   | LPAREN simpleexpression RPAREN
			   | simpleexpression logical simpleexpression
			   | LPAREN simpleexpression logical simpleexpression RPAREN

	'''
	# print(f'simple expression function {p} len:{len(p)}')
	if len(p) == 4:
		if p[1] == "(":
			p[0] = p[2]
		else:
			p[0] = (p[2], p[1], p[3])
	# print(f'simple expression function results {p[0]}')
	elif len(p) == 6:
		p[0] = (p[3], p[2], p[4])
	# print(f'simple expression function results {p[0]}')
	else:
		print(f'simple expression function invoked but none of the conditions matched')


def p_error(p):
	print("Syntax error", p)
	raise (f'Syntax Error {p}')


def p_empty(p):
	'''

	empty :

	'''
	p[0] = None


# lexer.input()

parser = yacc.yacc()

testcases = [
	"#1 > 2",
	'#2 == "teststring"',
	'#id >  2',
	'#name ==  "test"',
	'#1 > 2 and #2 == "test"',
	'#name == "test" and #id >= 5',
	'#1 > 2 or ( #2 >= 5 and #2 == "test" )',
	'( #2 >= 5 or #2 == "test" ) and #1 > 2',
	'(#1 > 2 or #5 >= 6) and ( #2 >= 5 and #2 == "test" )',
	'((#1 > 2 or #5 >= 6) and ( #2 >= 5 and #2 == "test" )) and #1 > 2',
	'(((#1 > 2 or #5 >= 6) and ( #2 >= 5 and #2 == "test" )) or #20 > 2) not #17 > 2'
]


def parsecondition(cond):
	return parser.parse(cond)


def runtestcases():
	for test in testcases:
		print("Query \n", test)
		print("Query Parsing Tree\n", parsecondition(test))

# runtestcases()