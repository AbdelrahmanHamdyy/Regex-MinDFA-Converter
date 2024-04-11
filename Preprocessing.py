import re

class RegexToPostfix:
    def __init__(self, regex):
        self.regex = regex
        self.valid = self.validate_regex()
        self.operator_precedence = {'*': 5, '+': 4, '?': 3, '.': 2, '|': 1}
        self.postfix = self.infix_to_postfix()
        print(self)
        
    def validate_regex(self):
        try:
            re.compile(self.regex)
        except re.error:
            return False
        return True
        
    def remove_spaces(self, regex):
        return regex.replace(" ", "")
        
    def convert_square_brackets(self, regex):
        '''
        Convert square brackets to parenthesis and insert a | between each character
        '''
        new_regex = ''
        i = 0
        while i < len(regex):
            if regex[i] == '[':
                new_regex += '('
                i += 1
                while regex[i] != ']' and i + 1 < len(regex):
                    if regex[i].isalnum() and regex[i + 1].isalnum():
                        new_regex += regex[i] + '|'
                    else:
                        new_regex += regex[i]
                    i += 1
                new_regex += ')'
            else:
                new_regex += regex[i]
            i += 1
        
        return new_regex
                    
    def replace_hyphens(self, regex):
        '''
        Replace hyphens with a range of characters
        '''
        new_regex = ''
        i = 1
        while i <= len(regex):
            if i + 1 < len(regex) and regex[i - 1].isalnum() and regex[i + 1].isalnum() and regex[i] == '-':
                start = regex[i - 1]
                end = regex[i + 1]
                for j in range(ord(start), ord(end)):
                    new_regex += chr(j) + '|'
                new_regex += chr(ord(end))
                i += 3
            else:
                new_regex += regex[i - 1]
                i += 1
                
        return new_regex
    
    def insert_concatenation(self, regex):
        '''
        Insert a . between two characters
        '''
        result = ''
        for i in range(len(regex)):
            if i > 0 and (((regex[i].isalnum() or regex[i] == '(') and (regex[i - 1].isalnum() or regex[i - 1] == ')')) or (regex[i] not in '*+.|' and regex[i - 1] in '*+)')):
                result += '.'
            result += regex[i]
        return result
    
    def preprocess(self):    
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
        postfix = ''
        stack = []
        for token in regex:
            if token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    postfix += stack.pop()
                stack.pop()
            elif token in self.operator_precedence:
                while stack and self.operator_precedence.get(token, 0) <= self.operator_precedence.get(stack[-1], 0):
                    postfix += stack.pop()
                stack.append(token)
            else:
                postfix += token
    
        while stack:
            postfix += stack.pop()
    
        return postfix
    
    def infix_to_postfix(self):
        if not self.valid:
            return ''
        regex = self.preprocess()
        postfix = self.apply_shunting_yard(regex)
        return postfix
    
    def __str__(self) -> str:
        return f"Regex: {self.regex}\nPostfix: {self.postfix}" if self.valid else f"Invalid regex: {self.regex}"
    
if __name__ == '__main__':
    regex = '[abc][a-z]ab*c'
    R2P = RegexToPostfix(regex)