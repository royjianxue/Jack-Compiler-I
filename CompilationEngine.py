from JackTokenizer import JackTokenizer
import sys

class CompilationEngine:
    """
    Borrow this class to study from: https://github.com/BradenCradock/nand2tetris/blob/master/projects/10/Compiler/CompilationEngine.py
    
    """

    def __init__(self, input_filepath, output_filepath):
        """
        creates a new compilation engine with the given input and output

        The next routine called(by the JackAnalyzer module) must be compile_class

        Arg(s)


        local variable(s): 
            tokenizer (str) : token from JackTokenizer
            file (file) : open a new file for read and write
            xml_indentation(int) : tracking number of identation
            types (str): types of int, boolean, char
        
        """

        self.tokenizer = JackTokenizer(input_filepath)
        self.file = open(output_filepath, "w+")

        #keep track of the identation
        self.xml_indentation = 0
        self.types = ["int", "boolean", "char"]

        self.compile_class()

    def write_xml(self):
        """
        write tokens into xml file with respect identation and open and close tags
        
        """
        token = self.tokenizer.current_token
        rep = {"<"  : "&lt;",
               ">"  : "$gt;",
               "\"" : "&quot;",
               "&"  : "&amp;"}
        
        if token in rep.keys():
            token = rep[token]

        print("\t" * self.xml_indentation + "<" + self.tokenizer.current_token_type + "> " + token + " </" + self.tokenizer.current_token_type + "> ", file = self.file)


    def syntax_error(self, expected, recieved):
        self.xml_indentation = 0
        self.xml_close_tag("class")
        sys.exit("Invalid Syntax: Expected " + str(expected) + " but recieved " + recieved)

    def check_token(self, string):
        """
        check token and write into xml file
        this method automatically advance to the next toke
        """
        if self.tokenizer.current_token in string:
            self.write_xml()
            self.tokenizer.advance()
        else:
            self.syntax_error(string, self.tokenizer.current_token)

    def check_token_type(self, string):
        """
        check token type and wrtie into xml file
        this method automatically advance to the next token
        """
        if self.tokenizer.current_token_type in string:
            self.write_xml()
            self.tokenizer.advance()
        else:
            self.syntax_error(string, self.tokenizer.current_token_type)

    def check_var_type(self):
        """
        check token type in ["int", "boolean", "char"]
        """

        if self.tokenizer.current_token in self.types:
            self.write_xml()
            self.tokenizer.advance()
        else:
            self.xml_indentation = 0
            self.xml_close_tag("class")
            sys.exit("Invalid Syntax: " + self.tokenizer.current_token + " is not a valid type.")

    def xml_open_tag(self, tag):
        print("\t" * self.xml_indentation + "<" + tag + ">", file = self.file)
        self.xml_indentation += 1

    def xml_close_tag(self, tag):
        self.xml_indentation -= 1
        print("\t" * self.xml_indentation + "</" + tag + ">", file = self.file)

    def compile_class(self):
        """
        compiles a complete class:
                1. advance to get the next token
                2. write open tag <class>
                3. first token has to be a class token, check and write into the xml file
                4. second token must be an identifier type, check and write into xml file
                5. third token must be a left open bracket, check and write into xml file
                6. compile static or field variable declaration - if current token is not of {"}", "constructor", "function", "method", "void"}
                7. compile a complete method, function or constructor. if the token is not of "}"
                8. write closing tag </class>
        """

        self.tokenizer.advance()
        self.xml_open_tag("class")

        self.check_token("class")
        self.check_token_type("IDENTIFIER")
        self.check_token("{")
        while self.tokenizer.current_token not in {"}", "constructor", "function", "method", "void"} :
            self.compile_class_var_dec()
        while self.tokenizer.current_token != "}":
            self.compile_subroutine()

        self.xml_close_tag("class")

    
    def compile_class_var_dec(self):
        """
        compiles a complete variable declaration:
                1. write open tag <"classVarDec">
                2. check token in {"field", "static"}  and advance to the next token (automatically)
                3. check if next token after field or static is an class object name/identifier, if not, check if in ["int", "boolean", "char"]. wirte to the xml file
                4. check the name of the variable/identifier, write to xml file
                5. keep checking and writing to the xml until ";" is found.
                6. write closing tag </classVarDec>
        """
        self.xml_open_tag("classVarDec")

        self.check_token({"field", "static"})
        #check identifier afer field or static for potential class object name
        if self.tokenizer.current_token_type == "IDENTIFIER":
            self.check_token_type("IDENTIFIER") 
        else:
            self.check_token(self.types)
        self.check_token_type("IDENTIFIER")
        while self.tokenizer.current_token != ";":
            self.check_token(",")
            self.check_token_type("IDENTIFIER")
        self.check_token(";")

        self.xml_close_tag("classVarDec")

 
    def compile_subroutine(self):
        """
        compiles a complete subroutine that of the {"constructor", "function", "method", "void"}
                1. write open tag <subroutineDec>
                2. check current token in {"constructor", "function", "method", "void"}, write to xml file
                3. check if the token type is class type, write to xml file, else check if the current token type is in ["int", "boolean", "char", "void"]
                4. check if the token is an identifier following step 3. write to xml file
                5. check if the token is left parenthese following step 4. write to xml file
                6. compile a list of parameters
                7. check token right parenthese and write to xml file
                8. compile a subroutine body
                9. write closing tag </subroutineDec>
        """
        self.xml_open_tag("subroutineDec")

        self.check_token({"constructor", "function", "method", "void"})

        # the token after {"constructor", "function", "method", "void"} should be a class type (identifier) or one of ["int", "boolean", "char", "void"]
        if self.tokenizer.current_token_type == "IDENTIFIER":
            self.check_token_type("IDENTIFIER") 
        else:
            self.check_token(self.types + ["void"])

        self.check_token_type("IDENTIFIER")
        self.check_token("(")
        self.compile_parameter_list()
        self.check_token(")")
        self.compile_subroutine_body()

        self.xml_close_tag("subroutineDec")

  
    def compile_subroutine_body(self):
        """
        compiles a complete subroutine body
                1. write open tag <subroutineBody>
                2. check token left braket, write into xml file
                3. check if the current token is local variable declaration (current token not in {"let", "if", "while", "do", "return"})
                4. step 3 is true, compile a list of local variable and write to xml file
                5. compile complete statements
                6. check right bracket and write to xml file
                7. write closing tag </subroutineBody>
        """
        self.xml_open_tag("subroutineBody")

        self.check_token("{")
        while self.tokenizer.current_token not in {"let", "if", "while", "do", "return"}:
            self.compile_var_dec()
        self.compile_statements()
        self.check_token("}")

        self.xml_close_tag("subroutineBody")

   
    def compile_parameter_list(self):
        """
        compiles a complete list of parameters
                1. write open tag <parameterList>
                2. check the current token if it's class type or one of ["int", "boolean", "char"]
                3. token following the above must be an identifier
                4. iterate over the remaining parameters and write to xml file
                5. write closing tag </parameterList>
        
        """

        if self.tokenizer.current_token != ")":
            self.xml_open_tag("parameterList")

            if self.tokenizer.current_token_type == "IDENTIFIER":
                self.check_token_type("IDENTIFIER") 
            else:
                self.check_var_type()
            self.check_token_type("IDENTIFIER")
            while self.tokenizer.current_token != ")":
                self.check_token(",")
                self.check_var_type()
                self.check_token_type("IDENTIFIER")

            self.xml_close_tag("parameterList")

    
    def compile_var_dec(self):
        """
        compile a list of local variables:
                1. write open tag <varDec>
                2. check the current token if a var type write to xml file
                3. check the variable type
                4. loop to compete
                5. write closing tag
        """

        self.xml_open_tag("varDec")

        self.check_token("var")
        if self.tokenizer.current_token_type == "IDENTIFIER":
            self.check_token_type("IDENTIFIER") 
        else:
            self.check_var_type()
        self.check_token_type("IDENTIFIER")
        while self.tokenizer.current_token != (";"):
            self.check_token(",")
            self.check_token_type("IDENTIFIER")
        self.check_token(";")

        self.xml_close_tag("varDec")

    

    def compile_statements(self):
        """
        compile complete statements
            1. write open tag <statements>
            2. loop through if no closing tag found
            3. calls the function
            4. found the right bracket and write closing tag
        
        """

        self.xml_open_tag("statements")

        statement_prefixes = {
            "let"       : self.compile_let,
            "do"        : self.compile_do,
            "if"        : self.compile_if,
            "while"     : self.compile_while,
            "return"    : self.compile_return
        }
        while self.tokenizer.current_token != ("}"):
            if self.tokenizer.current_token in statement_prefixes:
                statement_prefixes[self.tokenizer.current_token]()
            else:
                print(self.tokenizer.current_token)
                self.syntax_error("One of (let, do, if, while, return)", self.tokenizer.current_token)

        self.xml_close_tag("statements")


    def compile_do(self):

        """
        Compile a do statement:
            1. opening tag
            2. check do token
            3. compile expression
            4. check ; token
            5. closing tag
        
        """
        self.xml_open_tag("doStatement")

        self.check_token("do")
        self.compile_expression()
        self.check_token(";")

        self.xml_close_tag("doStatement")


    def compile_let(self):
        """
        Compile a let statement
            1. opening tag
            2. check let token
            3. check IDENTIFIER token
            4. array, check left bracket, compile expression, check right bracket
            5. check = token
            6. compile expression
            7. check ; token
            8. closing tag
        
        """
        self.xml_open_tag("letStatement")

        self.check_token("let")
        self.check_token_type("IDENTIFIER")
        if self.tokenizer.current_token == "[":
            self.check_token("[")
            self.compile_expression()
            self.check_token("]")
        self.check_token("=")
        self.compile_expression()
        self.check_token(";")

        self.xml_close_tag("letStatement")


    def compile_while(self):
        """
        compile a while statement
        
        """

        self.xml_open_tag("whileStatement")

        self.check_token("while")
        self.check_token("(")
        self.compile_expression()
        self.check_token(")")
        self.check_token("{")
        self.compile_statements()
        self.check_token("}")

        self.xml_close_tag("whileStatement")


    def compile_return(self):
        """
        compile a return statement
        """

        self.xml_open_tag("returnStatement")

        self.check_token("return")
        if self.tokenizer.current_token != ";":
            self.compile_expression()
        self.check_token(";")

        self.xml_close_tag("returnStatement")

    
    def compile_if(self):
        """
        compile a if statement
        """
        self.xml_open_tag("ifStatement")

        self.check_token("if")
        self.check_token("(")
        self.compile_expression()
        self.check_token(")")
        self.check_token("{")
        self.compile_statements()
        self.check_token("}")
        if self.tokenizer.current_token == "else":
            self.check_token("else")
            self.check_token("{")
            self.compile_statements()
            self.check_token("}")

        self.xml_close_tag("ifStatement")

    def compile_expression(self):
        """
        compile expression
        """

        self.xml_open_tag("expression")

        self.compile_term()
        while self.tokenizer.current_token not in {"]", ")", ";", ",", "("}:
            self.check_token({"+", "-", "*", "/", "&", "|", ">", "<", "="})
            self.compile_term()

        self.xml_close_tag("expression")

 
    def compile_term(self):
        """
        compile term
        """
        self.xml_open_tag("term")

        invalidKeywords = {"class", "constructor", "function", "method", "field",
                           "static","var","int", "char", "boolean", "void",
                           "let", "do", "if", "else", "while", "return"}

        if self.tokenizer.current_token_type == "IDENTIFIER":
            self.check_token_type("IDENTIFIER")
            if self.tokenizer.current_token == "[":             
                self.check_token("[")
                self.compile_expression()
                self.check_token("]")
            elif self.tokenizer.current_token in {"(", "."}:    
                self.compileSubroutineCall()

        elif self.tokenizer.current_token in {"-", "~"}:
            self.check_token({"-", "~"})
            self.compile_term()

        elif self.tokenizer.current_token == "(":
            self.check_token("(")
            self.compile_expression()
            self.check_token(")")

        elif self.tokenizer.current_token not in invalidKeywords:
            self.write_xml()
            self.tokenizer.advance()

        else:
            self.syntax_error("One of (true, false, null, this)", self.tokenizer.current_token)

        self.xml_close_tag("term")

    def compileSubroutineCall(self):
        """
        compile subroutine Call
        """

        self.xml_open_tag("subroutineCall")

        if self.tokenizer.current_token == ".":
            self.check_token(".")
            self.check_token_type("IDENTIFIER")
        self.check_token("(")
        self.compileExpressionList()
        self.check_token(")")

        self.xml_close_tag("subroutineCall")
   
    def compileExpressionList(self):
        self.xml_open_tag("expressionList")

        if self.tokenizer.current_token != ")":
            self.compile_expression()
        while self.tokenizer.current_token != ")":
            self.check_token(",")
            self.compile_expression()

        self.xml_close_tag("expressionList")

