import re

class JackTokenizer:

    
    keywords = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']

    symbols = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']

    

    def __init__(self, input_file):
        """
        constructor of JackToenizer class. 

        Arg(s): 
                input_file: .jack file or stream
        
        local variable(s):
                command_stream (array): stores every line of Jack code in array
                current_command (string): current string from Jack array
                token_stream (array): stores final tokens
                current_token(string): current selelced token from the token_stream
                current_token_type(string): returns a current token type
                index (int): index the token_stream array for current token

        method call(s): 
                prep_tokens(input_file): takes the input_file and prepare and store tokens in token_stream array

        """
        self.command_stream = []
        self.current_command = ""
        self.token_stream = []
        self.current_token = ""
        self.current_token_type = ""
        self.index = 0
        self.prep_tokens(input_file)

    def prep_tokens(self, input_file):
        """
        method that prepares the tokens and store in instance array variable token_stream
        
        """
        with open(input_file, 'r') as jack_file:
            lines = jack_file.readlines()
            in_comment_block = True #switch for comment block

            #store every line of Jack code into command_stream array
            for line in lines:
                line_without_whitespace = line.strip()

                if in_comment_block:

                    #check for single line comment block
                    if line_without_whitespace.startswith('/**') and line_without_whitespace.endswith('*/'):
                        continue #skip

                    #check more than one line
                    elif line_without_whitespace.startswith('/**'):
                        in_comment_block = False # set switch to false so the comments block is extended until '*/' is found.
                        continue #skip current line

                    elif line_without_whitespace.startswith('//'):
                        continue #skip the current line

                    else:
                        if line_without_whitespace:
                            self.command_stream.append(line_without_whitespace)                      
                if line_without_whitespace.endswith('*/'):
                    in_comment_block = True # set switch to true to indicate end of comment block
                    continue
    
            #tokenize every command_stream and store into token_stream
            for command in self.command_stream:
                # if string contains item in symbol 
                self.tokenize(command)

    #helper function
    def tokenize(self, command):
        """
        method that prepares token and store in instance array variable token_stream

        Arg(s):
                command (string): string input
        """
        local_token = ""

        #switch for quotation
        quote_found = False

        for char in command:
            if char.isalpha() or char.isdigit() or char == '_':
                local_token = "".join([local_token, char])   
            else:
                #if no quotation mark found
                if not quote_found:
                    if local_token:
                        self.token_stream.append(local_token)
                        local_token = ""

                    if char.isspace():
                        continue

                    if char == '"':
                        #set quotation found to true
                        #this allows the program to append everything to the current token until the closing quote is found
                        quote_found = True

                        if not local_token:
                            local_token = "".join([local_token, char])
                        else:
                            local_token = "".join([local_token, char])
                            self.token_stream.append(local_token)
                            local_token = ""
                    else:
                        self.token_stream.append(char)

                else:
                    if char.isspace():
                        local_token = "".join([local_token, char])
                        continue

                    if char == '"':
                        #set quotation found to true
                        #this allows the program to append everything to the current token until the closing quote is found
                        quote_found = False

                        if not local_token:
                            local_token = "".join([local_token, char])
                        else:
                            local_token = "".join([local_token, char])
                            self.token_stream.append(local_token)
                            local_token = ""
                    else:
                        local_token = "".join([local_token, char])

    def has_more_tokens(self):
        """
        return true if there are more tokens in the input file
        """
        return self.index <= len(self.token_stream) 
    

    def advance(self):
        """
        gets the next token from the input and makes it the current token

        execute this only when has_more_tokens function returns True

        """
        if self.has_more_tokens():
            self.current_token = self.token_stream[self.index]
            self.index += 1

            self.current_token_type = self.token_type()
            if self.current_token_type == "KEYWORD":
                self.current_token = self.keyword()
            elif self.current_token_type == "SYMBOL":
                self.current_token = self.symbol()
            elif self.current_token_type == "IDENTIFIER":
                self.current_token = self.identifier()
            elif self.current_token_type == "INT_CONST":
                self.current_token = self.int_val()
            elif self.current_token_type == "STRING_CONST":
                self.current_token = self.string_val()


    def token_type(self):
        """
        return types of current token as a constant

        e.g. KEYWORD, SYMBOL, IDENTIFIER, INT_CONST, STRING_CONST
        
        """
        if self.current_token.startswith('"') and self.current_token.endswith('"'):
            self.current_token = self.current_token[1:-1]
            return "STRING_CONST"
        elif self.current_token.isalpha():
            if self.current_token in self.keywords:
                return "KEYWORD"
            else:
                return "IDENTIFIER"
        elif self.current_token in self.symbols:
            return "SYMBOL"
        elif self.current_token.isdecimal():
            return "INT_CONST"
        else:
            raise ValueError("Not a valid token type!")

    def keyword(self):
        """
        returns the keyword which is the current token, as a constant. This method should be called only if token_type is KEYWORD

        e.g. CLASS, METHOD, FUNCTION, CONSTRUCTION, INT, BOOLEAN, CHAR, VOID, VAR, STATIC, FIELD, LET, DO, IF, ELSE, WHILE, RETURN, TRUE, FALSE, NULL, THIS
        """

        return self.current_token

    def symbol(self):
        """
        returns the character which is the current token. Should be called only if token_type is SYMBOL
        """

        return self.current_token


    def identifier(self):
        """
        returns the string which is the current token. Should be called only if token_type is IDENTIFIER
        """
        return self.current_token

    def int_val(self):
        """
        returns the integer value of the current token. Should be called only if token_type is INIT_CONST
        
        """
        return self.current_token

    def string_val(self):
        """
        return the string value of the current token, without the opening and clising double quotes. Should be called only if token_type is STRING_CONST
        """

        return self.current_token

    def write_xml(self, command):
        pass




if __name__ == "__main__":

    jk = JackTokenizer("Main.jack")
   
    for _ in range(len(jk.token_stream)):
        jk.advance()
        line = "<{0}> {1} </{2}>".format(jk.current_token_type, jk.current_token, jk.current_token_type)
        print(line)
 







    