import csv
import os

DELIMITER = [',', ';', ':', '(', ')', '{', '}', '[', ']']
OPERATOR = ['=', '+', '-', '*', '/', '%', '^', '!', '|', '&', '<', '>']
SPECIAL_CHAR = ['~', '?', '@', '$', '|', '$', '.', '#']
# TODO: Edit later if tapos na paper
UNIT = ['m', 'in', 'ft', 'yd', 'mi', 'm2', 'sqin', 'sqft', 'sqyd', 'sqmi', 'acre', 'hectare', 'm3', 'L', 'cc', 'teaspoon', 'tablespoon', 'rad', 'deg', 'grad', 'sec', 'min', 'hr', 'day', 'week', 'month', 'year', 'decade', 'century', 'g', 'ton', 'oz', 'lbs']


# Main function
def main():
    try:
        # Prompt user for the file name
        fileName = input('Enter the file name: ')
        
        # Validate the file extension
        validate_file_extension(fileName)
        print('Processing file...')
        
        # Open the file and read the contents
        with open(fileName, 'r') as file:
            inputCode = file.read()
            
        # Perform lexical analysis
        tokens = lexical_analyzer(inputCode)
        
        # Output the tokens to a CSV file
        outputName = input('Enter the output file name (don\'t include file extension): ')
        if not outputName:
            raise ValueError('Output file name cannot be empty.')
        
        outputFileName = outputName + '.csv'
        
        # Write tokens to the CSV file
        with open(outputFileName, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, quotechar=None, escapechar=' ')
            writer.writerow(['Token Value', 'Token Type'])
            
            for token in tokens:
                writer.writerow([token['value'], token['type']])
        
        print(f'Tokens have been written to {outputFileName}')
    except ValueError as valueE:
        print(valueE)
    except FileNotFoundError as fnfE:
        print(fnfE)
    except Exception as e:
        print(f'An unexpected error occurred!\n{e}')

# Check if the file has a .calc extension
def validate_file_extension(fileName):
    if not fileName.endswith('.calc'):
        raise ValueError(f'Invalid file extension: "{fileName}". Only .calc files are allowed.')
    if not os.path.isfile(fileName):
        raise FileNotFoundError(f'File not found: {fileName}')
    return True

# Lexical analyzer
def lexical_analyzer(inputCode):
    index = 0
    tokens = []
    length = len(inputCode)
    previousToken = None
    
    while index < length:
        char = inputCode[index]
        
        # Skip whitespace
        if char.isspace():
            index += 1
            continue
        
        # Handle comments
        elif char == '#':
            token, index = handle_comments(inputCode, index, length)
            tokens.append(token)
            continue
        
        # Handle quotation marks
        elif char in ["'", '"']:
            token, index = handle_quotes(inputCode, index, length)
            tokens.append(token)
            previousToken = token
            continue
        
        # Handle delimiters
        elif char in DELIMITER:
            token = handle_delimiters(inputCode, index)
            tokens.append(token)
            previousToken = token  
            index += 1
            continue
        
        # Handle operators
        elif char in OPERATOR:
            token, index = handle_operators(inputCode, index, length, previousToken)
            tokens.append(token)
            previousToken = token
            continue
        
        # Handle numbers
        elif char.isdigit() or (char == '.' and index + 1 < length and inputCode[index + 1].isdigit()):
            token, unitToken, index = handle_numbers(inputCode, index, length)
            tokens.append(token)
            if unitToken:
                tokens.append(unitToken)
                previousToken = unitToken
            else:
                previousToken = token
            continue
        
        # # Handle words (keywords, reserved words, identifiers, or invalid identifiers)
        # elif char.isalpha() or char == '_' or inputCode[index] in SPECIAL_CHAR:
        #     token, index = handle_words(inputCode, index, length)
        #     tokens.append(token)
        #     previousToken = token
        #     continue
        
        # TODO: Remove this block after handling all tokens
        else:
            index += 1
        
    return tokens

# Process comments
def handle_comments(inputCode, index, length):
    startIndex = index
    index += 1
    
    while index < length and inputCode[index] != '#':
        index += 1
    
    if index < length and inputCode[index] == '#':
        index += 1
        return {'value': inputCode[startIndex:index], 'type': 'COMMENT'}, index
    else:
        return {'value': inputCode[startIndex:index], 'type': 'INVALID_COMMENT'}, index

# Process quotation marks   
def handle_quotes(inputCode, index, length):
    quoteType = inputCode[index] # Single or double quote
    startIndex = index
    index += 1
    value = ''
    
    while index < length:
        char = inputCode[index]
        
        # Matching closing quote encountered
        if char == quoteType:
            index += 1
            value = inputCode[startIndex:index]
            if len(value) == 3: # Example 'a' -> CHAR
                return {'value': value, 'type': 'CHAR_LITERAL'}, index
            else:
                return {'value': value, 'type': 'STRING_LITERAL'}, index
        
        if char == '\n':
            index += 1
            break
        
        # Otherwise, add the character to the value
        value += char
        index += 1
        
    # If the closing quote is not found, it's invalid
    return {'value': value[startIndex:index], 'type': 'INVALID_QUOTE'}, index

# Process delimiters
def handle_delimiters(inputCode, index):
    char = inputCode[index]
    tokenType = ''
    
    # Determine the token type
    if char == ',':
        tokenType = 'COMMA'
    elif char == ';':
        tokenType = 'SEMICOLON'
    elif char == ':':
        tokenType = 'COLON'
    elif char == '(':
        tokenType = 'OPEN_PAREN'
    elif char == ')':
        tokenType = 'CLOSE_PAREN'
    elif char == '{':
        tokenType = 'OPEN_BRACE'
    elif char == '}':
        tokenType = 'CLOSE_BRACE'
    elif char == '[':
        tokenType = 'OPEN_BRACKET'
    elif char == ']':
        tokenType = 'CLOSE_BRACKET'
        
    return {'value': char, 'type': tokenType}

# Process operators
# TODO: Revise PRECEDING_TOKENS for ambiguous operators after completing all tokens
def handle_operators(inputCode, index, length, previousToken):
    VALID_OP = ['=', '+=', '-=', '*=', '/=', '%=', '+', '-', '*', '/', '%', '^', '++', '--', '!', '||', '&&', '==', '!=', '>', '<', '>=', '<=']
    ASSIGNMENT_OP = ['=', '+=', '-=', '*=', '/=', '%=']
    ARITHMETIC_OP = ['*', '/', '^']
    UNARY_OP = ['++', '--']
    AMBIGUOUS_OP = ['+', '-', '%'] # Can be arithmetic or unary
    LOGICAL_BOOL_OP = ['!', '||', '&&']
    RELATIONAL_BOOL_OP = ['==', '!=', '>', '<', '>=', '<=']
    
    startIndex = index
    
    # Check for sequence of operators (e.g. ++, --, +=, -=)
    while index < length and inputCode[index] in OPERATOR:
        index += 1
        
    # Get the sequence of operators
    operatorSequence = inputCode[startIndex:index]
    
    # Determine the token type
    if operatorSequence in VALID_OP:
        if operatorSequence in ASSIGNMENT_OP:
            if operatorSequence == '=':
                tokenType = 'ASSIGN_OP'
            elif operatorSequence == '+=':
                tokenType = 'ADD_ASSIGN_OP'
            elif operatorSequence == '-=':
                tokenType = 'SUB_ASSIGN_OP'
            elif operatorSequence == '*=':  
                tokenType = 'MULT_ASSIGN_OP'
            elif operatorSequence == '/=':
                tokenType = 'DIV_ASSIGN_OP'
            elif operatorSequence == '%=':
                tokenType = 'MOD_ASSIGN_OP'
        elif operatorSequence in ARITHMETIC_OP:
            if operatorSequence == '*':
                tokenType = 'MULT_OP'
            elif operatorSequence == '/':
                tokenType = 'DIV_OP'
            elif operatorSequence == '^':
                tokenType = 'POW_OP'
        elif operatorSequence in UNARY_OP:
            if operatorSequence == '++':
                tokenType = 'INC_OP'
            elif operatorSequence == '--':
                tokenType = 'DEC_OP'
        elif operatorSequence in AMBIGUOUS_OP:
            PRECEDING_TOKENS = ['COMMA', 'SEMICOLON', 'COLON', 'OPEN_PAREN', 'OPEN_BRACE', 'OPEN_BRACKET', 'ASSIGN_OP', 'ADD_ASSIGN_OP', 'SUB_ASSIGN_OP', 'MULT_ASSIGN_OP', 'DIV_ASSIGN_OP', 'MOD_ASSIGN_OP', 'MULT_OP', 'DIV_OP', 'POW_OP', 'ADD_OP', 'SUB_OP', 'MOD_OP', 'NOT_OP', 'OR_OP', 'AND_OP', 'EQU_OP', 'NOT_EQU_OP', 'GRT_OP', 'LST_OP', 'GRT_EQU_OP', 'LST_EQU_OP']
            
            if operatorSequence == '+':
                if previousToken == None or previousToken['type'] in PRECEDING_TOKENS:
                    tokenType = 'UNARY_PLUS_OP'
                else:
                    tokenType = 'ADD_OP'
            elif operatorSequence == '-':
                if previousToken == None or previousToken['type'] in PRECEDING_TOKENS:
                    tokenType = 'UNARY_MINUS_OP'
                else:
                    tokenType = 'SUB_OP'
            elif operatorSequence == '%':
                # Percentage operator must be right beside a number (e.g. 10%)
                if previousToken and previousToken['type'] in ['INTEGER', 'FLOAT'] and inputCode[index - 1] != ' ':
                    tokenType = 'PERCENTAGE_OP'
                else:
                    tokenType = 'MOD_OP'
        elif operatorSequence in LOGICAL_BOOL_OP:
            if operatorSequence == '!':
                tokenType = 'NOT_OP'
            elif operatorSequence == '||':
                tokenType = 'OR_OP'
            elif operatorSequence == '&&':
                tokenType = 'AND_OP'
        elif operatorSequence in RELATIONAL_BOOL_OP:
            if operatorSequence == '==':
                tokenType = 'EQU_OP'
            elif operatorSequence == '!=':
                tokenType = 'NOT_EQU_OP'
            elif operatorSequence == '>':
                tokenType = 'GRT_OP'
            elif operatorSequence == '<':
                tokenType = 'LST_OP'
            elif operatorSequence == '>=':
                tokenType = 'GRT_EQU_OP'
            elif operatorSequence == '<=':
                tokenType = 'LST_EQU_OP'
    else:
        tokenType = 'INVALID_OP'
        
    return {'value': operatorSequence, 'type': tokenType}, index

# Process numbers
def handle_numbers(inputCode, index, length):
    numStartIndex = index
    hasDot = False # Check if the number has a decimal point
    
    while index < length:
        char = inputCode[index]
        
        if char.isdigit():
            index += 1
        elif char == '.':
            if hasDot: # Invalid float
                index += 1
                return {'value': inputCode[numStartIndex:index], 'type': 'INVALID_NUM'}, None, index
            
            # Ensure there is a digit after the decimal point
            if index + 1 < length and inputCode[index + 1].isdigit(): 
                hasDot = True
                index += 1
            else:
                index += 1
                return {'value': inputCode[numStartIndex:index], 'type': 'INVALID_NUM'}, None, index
        else:
            break
    numEndIndex = index 
    
    # Check if the number has a unit
    if index < length and inputCode[index].isalpha():
        charStartIndex = index
        
        # Find the end of the possible unit
        while index < length and inputCode[index] not in [' ', '\n']:
            index += 1
        
        if inputCode[charStartIndex:index] in UNIT:
            unitToken = classify_unit(inputCode[charStartIndex:index])
        else:   # Invalid Identifier since it's not a valid unit
            return {'value': inputCode[numStartIndex:index], 'type': 'INVALID_IDENTIFIER'}, None, index
    
    # Determine if the number is a float or an integer
    if hasDot:
        return {'value': inputCode[numStartIndex:numEndIndex], 'type': 'FLOAT'}, unitToken, index
    else:
        return {'value': inputCode[numStartIndex:numEndIndex], 'type': 'INTEGER'}, unitToken, index
    
# TODO: Complete the function for units
# Handle units
def classify_unit(inputCode):
    if inputCode in UNIT:
        return {'value': inputCode, 'type': 'UNIT'}
    
# def handle_words(inputCode, index, length):
#     startIndex = index
    
#     while index < length and (inputCode[index].isalnum() or inputCode[index] == '_' or inputCode[index] in SPECIAL_CHAR):
#         index += 1
#     word = inputCode[startIndex:index]
    
#     # Determine the token type for word
#     if word in KEYWORD:
#         token = handle_keyword(word)

# Run the main function
if __name__ == '__main__':
    main()