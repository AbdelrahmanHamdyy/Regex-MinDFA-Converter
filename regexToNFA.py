from Preprocessing import RegexToPostfix
from NFA import NFA

if __name__ == '__main__':
    postfix = RegexToPostfix("a(b|c)*")
    NFA(None, None).execute(postfix.postfix)
    