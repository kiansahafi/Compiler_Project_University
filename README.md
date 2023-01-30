# Compiler_Project_University

Project for Compiler class in University of zanjan
Professor: Dr.Leila Safari

Description of the Project:

First Phase:
Lexical analysis of language manual

Second Phase:
Lexical analysis using the Lexer Tool

Third Phase:
syntactical analysis using Yacc

Fourth Phase:
semantic analysis

Fifth Phase:
Intermediate code generation

1. Mini_Java
   The Mini_Java language is a subset of Java. Every Mini_Java program is a legal Java program with Java semantics. Following is an informal summary of the syntactic restrictions of Java that define Mini_Java. Later assignments will modify restrictions.
   A Mini_Java program is a single file without a package declaration (hence corresponds to the default package) and without imports. It consists of zero or more Java classes. The classes are simple; there are no interface classes, subclasses, or nested classes.
   The members of a class are fields and methods. Member declarations can specify public or private access, and can specify static instantiation. Fields cannot have an initializing expression in their declaration. Methods have a parameter list and a body. There are no constructor methods.
   The types of Mini_Java are primitive types, class types, and array types. The primitive types are limited to void, int, boolean, and the array types are limited to the integer array int [] and the class [] array where class is any class type.
   The statements of Mini_Java are limited to the statement block, the assignment statement, method invocation, the conditional statement (if), and the repetitive statement (while).
   A declaration of a local variable (with required initializing expression) can only appear as a statement within a statement block.
   The return statement, if present at all, can only appear as the last statement in a method and yields a result.
   The expressions of Mini_Java consist of operations applied to literals, variables (including indexed and qualified references), method invocation, and new arrays and objects. Expressions may be parenthesized to specify evaluation order.
   The operators in Mini_Java are limited to
   • relational operations: > < == <= >= !=
   • logical operations: && || !
   • arithmetic operations: + - \* /
   All operators are infix binary operators (binop) with the exception of the unary prefix operators (unop) logical negation (!), and arithmetic negation (-). The latter is both a unary and binary operator.

1.1. Lexical rules
The terminals in the Mini*Java grammar are the tokens produced by the scanner. The token id stands for any identifier formed from a sequence of letters, digits, and underscores, starting with a letter. Uppercase letters are distinguished from lowercase letters. The token num stands for any integer literal that is a sequence of decimal digits. Tokens binop and unop stand for the operators listed above, and the token eot stands for the end of the input text. The remaining tokens stand for themselves (i.e. for the sequence of characters that are used to spell them). Keywords of the language are shown in bold for readability only; they are written in regular lowercase text.
Whitespace and comments may appear before or after any token. Whitespace is limited to spaces, tabs (\t), newlines (\n) and carriage returns (\r). There are two forms of comments. One starts with /* and ends with \_/, while the other begins with // and extends to the end of the line.
The text of Mini_Java programs is written in ASCII. Any characters other than those that are part of a token, whitespace or a comment are erroneous.
1.2. Grammar
The Mini_Java grammar is shown on the next page. Non-terminals are displayed in the normal font and start with a capital letter, while terminals are displayed in this font. Terminals id, num, unop, and binop and represent a set of possible terminals. The remaining symbols are part of the BNF extensions for grouping, choice, and repetition. Besides these extensions the option construct is also used and is defined as follows: (α)? = (α | ε). To help distinguish the parentheses used in grouping from the left and right parenthesis used as terminals, the latter are shown in bold. The start symbol of the grammar is “Program”.

Mini*Java Grammar
Program ::= (ClassDeclaration)* eot
ClassDeclaration::= class id < (FieldDeclaration | MethodDeclaration)_ \
FieldDeclaration ::= Declarators id;
MethodDeclaration ::= Declarators id (ParameterList? ) < Statement* (return Expression
:? '
Declarators ::= (public | private? static? Type Type::= PrimType | ClassType | ArrType PrimType ::= int boolean void
ClassType ::= id
ArrType ::= (int | ClassType ) [I
ParameterList:= Type id ( Type id)*
ArgumentList::= Expression (, Expression)_ Reference::= (this id) (.id \_
Statement ::= { Statement\* } | Type id = Expression ; | Reference ([ Expression ])? =
Expression ; | Reference (ArgumentList?) ; | if ( Expression) Statement (else Statement)?
while (Expression) Statement
Expression ::= Reference ( [ Expression ] )? | Reference (ArgumentList?) unop
Expression Expression binop Expression| (Expression) | num true false new (id ( )
int [ Expression ] | id [ Expression ])
