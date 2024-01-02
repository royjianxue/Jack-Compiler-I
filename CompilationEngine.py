class CompilationEngine:
    def __init__(self, input_file, output_file):
        """
        creates a new compilation engine with the given input and output

        The next routine called(by the JackAnalyzer module) must be compile_class
        
        """
        pass

    def compile_class(self):
        """
        compiles a complete class
        """
        pass

    def compile_class_var_dec(self):
        """
        compiles a static variable declaration, or a field declaration.
        """
        pass

    def compile_subroutine(self):
        """
        compiles a complete method, function, or constructor
        """
        pass

    def compile_parameter_list(self):
        """
        compiles a (possibly empty) parameter list. Does not handle the enclising parenthese tokens (and)
        """
        pass

    def compile_subroutine_body(self):
        """
        compiles a subroutine's body
        """
        pass

    def compile_var_dec(self):
        """
        compiles a var declaration
        """
        pass

    def compile_statements(self):
        """
        compiles a sequence of statements.

        does not handle the enclosing curly bracket tokens {and}
        """
        pass

    def compile_let(self):
        """
        compiles a let statement
        """
        pass

    def compile_if(self):
        """
        compiles an if statement, possibly with a trailing else clause
        """
        pass

    def compile_while(self):
        """
        compiles a while statement
        """

        pass

    def compile_do(self):
        """
        compiles a do statement
        """
        pass

    def compile_return(self):
        """
        compiles a return statement
        """
        pass

    def compile_expression(self):
        """
        compiles an expression
        """

        pass

    def compile_term(self):
        """
        compiles a term. If the current token is an identifier, the routine must resolve it into a variable, an array element, or a subroutine call.
        A single lookahead token, which maybe [, (, or., suffices to distinguish between the possibilities. 
        Any other token is not part of this term and should not be advanced over.
        """

        pass

    def compile_expression_list(self):

        """
        compiles a (possibly empty) comma-separated list of expressions. Returns the number of expressions in the list.
        """
        pass