class JackTokenizer:

    def __init__(self, input_file):
        """
        opens the input .jack file/stream and gets ready to tokenize it

        Arg(s): 
                input_file: .jack file or stream
        
        """
        pass

    def has_more_tokens(self):
        """
        return true if there are more tokens in the input file
        """
        pass

    def advance(self):
        """
        gets the next token from the input and makes it the current token

        execute this only when has_more_tokens function returns True

        """
        pass

    def token_type(self):
        """
        return types of current token as a constant

        e.g. KEYWORD, SYMBOL, IDENTIFIER, INT_CONST, STRING_CONST
        
        """

        pass

    def keyword(self):
        """
        returns the keyword which is the current token, as a constant. This method should be called only if token_type is KEYWORD

        e.g. CLASS, METHOD, FUNCTION, CONSTRUCTION, INT, BOOLEAN, CHAR, VOID, VAR, STATIC, FIELD, LET, DO, IF, ELSE, WHILE, RETURN, TRUE, FALSE, NULL, THIS
        """

        pass

    def symbol(self):
        """
        returns the character which is the current token. Should be called only if token_type is SYMBOL
        """

        pass


    def identifier(self):
        """
        returns the string which is the current token. Should be called only if token_type is IDENTIFIER
        """
        pass

    def int_val(self):
        """
        returns the integer value of the current token. Should be called only if token_type is INIT_CONST
        
        """
        pass

    def string_val(self):
        """
        return the string value of the current token, without the opening and clising double quotes. Should be called only if token_type is STRING_CONST
        """

        pass