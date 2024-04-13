import re

class RegexToPostfix:
    def __init__(self, regex):
        # Input regex
        self.regex = regex
        # Validate the regex before proceeding with the conversion
        self.valid = self.validate_regex()
        # Precedence of operators to be used in the shunting yard algorithm
        self.operator_precedence = {'*': 5, '+': 4, '?': 3, '.': 2, '|': 1}
        # Convert infix to postfix
        self.postfix = self.infix_to_postfix()
        
    def validate_regex(self):
        '''
        If the regex compiles without any errors, it is valid
        '''
        try:
            re.compile(self.regex)
        except re.error:
            return False
        return True
        
    def remove_spaces(self, regex):
        '''
        Remove spaces from the regex
        '''
        return regex.replace(" ", "")
        
    def convert_square_brackets(self, regex):
        '''
        Convert square brackets to parenthesis and insert a | between each character
        '''
        # We'll collect the new regex in this variable
        new_regex = ''
        # Loop counter
        i = 0
        # Loop over the entire regex
        while i < len(regex):
            # If we encounter a square bracket
            if regex[i] == '[':
                # Replace it with a parenthesis
                new_regex += '('
                # Move to the next character
                i += 1
                # Keep adding characters to the new regex until we encounter a closing square bracket or reach the end of the regex
                while regex[i] != ']' and i + 1 < len(regex):
                    # If the current character and the next character are both alphanumeric, insert a | between them
                    if regex[i].isalnum() and regex[i + 1].isalnum():
                        new_regex += regex[i] + '|'
                    else: # Otherwise, just add the character to the new regex
                        new_regex += regex[i]
                    # Increment the loop counter
                    i += 1
                # Here, we've encountered a closing square bracket, so we replace it with a closing parenthesis
                new_regex += ')'
            else:
                # If the current character is not a square bracket, just add it to the new regex
                new_regex += regex[i]
            # Increment the loop counter
            i += 1
        
        return new_regex
                    
    def replace_hyphens(self, regex):
        '''
        Replace hyphens with a range of characters
        '''
        # New regex with ranges repleaced by individual characters will be here
        new_regex = ''
        # Start the loop from the second element since the hyphen can't be the first or the last character
        i = 1
        # Since we are looking for the current and the previous character, we'll loop until after the last character
        while i <= len(regex):
            # If the current character is a hyphen and the previous and the next characters are alphanumeric, also i + 1 < len(regex) is to avoid index out of range error since we are looking for the next character
            if i + 1 < len(regex) and regex[i - 1].isalnum() and regex[i + 1].isalnum() and regex[i] == '-':
                # Set the start and end of the range
                start = regex[i - 1]
                end = regex[i + 1]
                # Loop over the range using ASCII until before the end and add each character to the new regex with a | between them
                for j in range(ord(start), ord(end)):
                    new_regex += chr(j) + '|'
                # Add the last character of the range to the new regex
                new_regex += chr(ord(end))
                # Increment the loop counter by 3 since we've already processed the previous and the next characters
                i += 3
            else:
                # If the current character is not a hyphen or the previous and the next characters are not alphanumeric, just add the current character to the new regex and increment the loop counter by 1 to move one step
                new_regex += regex[i - 1]
                i += 1
                
        return new_regex
    
    def insert_concatenation(self, regex):
        '''
        Insert a concatenation symbol . between two characters where they can be concatenated
        '''
        # Resulting regex will be stored here after inserting the concatenation symbol
        result = ''
        # Loop over the entire regex
        for i in range(len(regex)):
            # If the current character is alphanumeric or an opening parenthesis and the previous character is alphanumeric or a closing parenthesis directly after each other, insert a concatenation symbol between them
            # Or if the current character is not a special character and the previous character is a special character, insert a .
            if i > 0 and (((regex[i].isalnum() or regex[i] == '(') and (regex[i - 1].isalnum() or regex[i - 1] == ')')) or (regex[i] not in '*+.|)' and regex[i - 1] in '*+)')):
                result += '.'
            # Add the current character to the new regex
            result += regex[i]
        return result
    
    def preprocess(self):
        '''
        Call all the preprocessing functions in order
        '''
        regex = self.remove_spaces(self.regex)
        print("After removing spaces:", regex)
        
        regex = self.replace_hyphens(regex)
        print("After substituting hyphens:", regex)
        
        regex = self.convert_square_brackets(regex)
        print("After converting square brackets:", regex)
        
        regex = self.insert_concatenation(regex)
        print("After inserting concatenation:", regex)
        
        print("-----------------------------------------")
        return regex
                
    def apply_shunting_yard(self, regex):
        '''
        Apply the shunting yard algorithm to convert infix to postfix
        '''
        # Initialize an empty string to store the postfix expression
        postfix = ''
        # Initialize an empty stack to help with the conversion
        stack = []
        # Iterate through each token in the infix regular expression
        for token in regex:
            if token == '(':  # If the token is an opening parenthesis
                stack.append(token)  # Push it onto the stack
            elif token == ')':  # If the token is a closing parenthesis
                # Pop operators from the stack and add them to the postfix expression until an opening parenthesis is found
                while stack and stack[-1] != '(':
                    postfix += stack.pop()
                # Discard the opening parenthesis
                stack.pop()
            elif token in self.operator_precedence:  # If the token is an operator
                # Pop operators from the stack with greater precedence and add them to the postfix expression
                # Stop when encountering an operator with lesser precedence or when the stack is empty
                while stack and self.operator_precedence.get(token, 0) <= self.operator_precedence.get(stack[-1], 0):
                    postfix += stack.pop()
                stack.append(token)  # Push the current operator onto the stack
            else:  # If the token is an operand
                postfix += token  # Add it directly to the postfix expression

        # After processing all tokens, pop any remaining operators from the stack and add them to the postfix expression
        while stack:
            postfix += stack.pop()

        return postfix  # Return the postfix expression
    
    def infix_to_postfix(self):
        # If the regex is invalid, return an empty string
        if not self.valid:
            return ''
        # Preprocess the regex
        regex = self.preprocess()
        # Apply the shunting yard algorithm to convert infix to postfix
        postfix = self.apply_shunting_yard(regex)
        # Final result
        return postfix
    
    def __str__(self) -> str:
        return f"Regex: {self.regex}\nPostfix: {self.postfix}" if self.valid else f"Invalid regex: {self.regex}"
    
if __name__ == '__main__':
    regex = '[abc][a-z]ab*c'
    R2P = RegexToPostfix(regex)
    print(R2P)