import re
from projects.stacks import Stack


def infix_to_postfix(expression):
    stack = Stack()
    postfix = []

    operators = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
        '^': 3
    }

    # Separate operands, operators, and parentheses
    tokens = re.findall(r'[A-Za-z0-9]+|[()+\-*/^]', expression)

    if not tokens:
        raise ValueError("Please enter an expression.")

    # Reject invalid characters
    cleaned_expression = re.sub(r'\s+', '', expression)
    token_expression = ''.join(tokens)

    if cleaned_expression != token_expression:
        raise ValueError("Invalid character in expression.")

    for token in tokens:
        if token.isalnum():
            postfix.append(token)

        elif token == '(':
            stack.push(token)

        elif token == ')':
            while stack.peek() is not None and stack.peek() != '(':
                postfix.append(stack.pop())

            if stack.peek() is None:
                raise ValueError("Mismatched parentheses.")

            stack.pop()

        elif token in operators:
            while (
                stack.peek() is not None
                and stack.peek() != '('
                and (
                    operators[stack.peek()] > operators[token]
                    or (
                        operators[stack.peek()] == operators[token]
                        and token != '^'
                    )
                )
            ):
                postfix.append(stack.pop())

            stack.push(token)

        else:
            raise ValueError(f"Invalid token: {token}")

    while stack.peek() is not None:
        operator = stack.pop()

        if operator in ('(', ')'):
            raise ValueError("Mismatched parentheses.")

        postfix.append(operator)

    return ' '.join(postfix)
