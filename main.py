import os

CONSTANT = ['e', 'pi']
DATA_TYPE = ['length', 'surface_area', 'volume', 'angle', 'time', 'mass']
DELIMITER = [',', ';', ':', '(', ')', '{', '}', '[', ']']
KEYWORD = ['let', 'range', 'print', 'input', 'for', 'if', 'else']
OPERATOR = ['=', '+', '-', '*', '/', '%', '^', '!', '|', '&', '<', '>']
RESERVED_WORD = ['null', 'true', 'false', 'import']
SPECIAL_CHAR = ['~', '?', '@', '$', '.', '`']
UNIT = ['m', 'meter', 'in', 'inch', 'ft', 'feet', 'yd', 'yard', 'm2', 'sqin', 'sqft', 'sqyd', 'sqmi', 'acre', 'hectare', 'm3', 'L', 'cc', 'teaspoon', 'tablespoon', 'rad', 'deg', 'degrees', 'grad', 'sec', 'seconds', 'min', 'minutes', 'hr', 'hour', 'day', 'week', 'month', 'year', 'decade', 'century', 'g', 'ton', 'oz', 'lbs']

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
        
        # Output the tokens to a text file
        outputName = input("Enter the output file name (don’t include file extension): ")
        if not outputName:
            raise ValueError("Output file name cannot be empty.")

        outputFileName = outputName + ".txt"

        # Write tokens to the text file in table format
        with open(outputFileName, "w") as txtfile:
            # Write table headers
            txtfile.write(f"{'Token Value':<20} {'Token Type':<20}\n")
            txtfile.write("=" * 40 + "\n")

            # Write each token as a formatted row
            for token in tokens:
                txtfile.write(f"{token['value']:<20} {token['type']:<20}\n")

        print(f"Symbol table has been written to {outputFileName}")
    except ValueError as valueE:
        print(valueE)
    except FileNotFoundError as fnfE:
        print(fnfE)
    except Exception as e:
        print(f'An unexpected error occurred!\n{e}')

# Check if the file has a .calq extension
def validate_file_extension(fileName):
    if not fileName.endswith('.calq'):
        raise ValueError(f'Invalid file extension: "{fileName}". Only .calq files are allowed.')
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
        
        # Handle numbers and units
        elif char.isdigit() or (char == '.' and index + 1 < length and inputCode[index + 1].isdigit()):
            token, index = handle_numbers(inputCode, index, length)
            tokens.append(token)
            previousToken = token
            continue
        
        # Handle words (keywords, reserved words, identifiers)
        elif char.isalpha() or char == '_' or inputCode[index] in SPECIAL_CHAR:
            token, index = handle_words(inputCode, index, length)
            tokens.append(token)
            previousToken = token
            continue
        
        # Handle unknown characters
        else:
            print(f"Warning: Unrecognized character '{char}' at index {index}")
            index += 1
        
    return tokens

# Process comments
def handle_comments(inputCode, index, length):
    startIndex = index
    index += 1
    
    while index < length and inputCode[index] != '\n':
        index += 1
    
    return {'value': inputCode[startIndex:index], 'type': 'COMMENT'}, index


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
    if inputCode[index - 1] == '\n':
        return {'value': inputCode[startIndex:index - 1], 'type': 'INVALID_LITERAL'}, index
    else:
        return {'value': inputCode[startIndex:index], 'type': 'INVALID_LITERAL'}, index

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
            if operatorSequence == '+':
                    tokenType = 'PLUS_OP'
            elif operatorSequence == '-':
                    tokenType = 'MINUS_OP'
            elif operatorSequence == '%':
                # Percentage operator must be right beside a number (e.g. 10%)
                if previousToken and previousToken['type'] in ['INTEGER', 'FLOAT'] and not inputCode[index - 2].isspace():
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
    startIndex = index
    
    # Check if the number has a decimal point
    if inputCode[index] == '.':
        hasDot = True
    else:
        hasDot = False
    
    while index < length:
        char = inputCode[index]
        
        if char.isdigit():
            index += 1
        elif char == '.':
            if hasDot: # Invalid float
                index += 1
                return {'value': inputCode[startIndex:index], 'type': 'INVALID_NUM'}, None, index
            
            # Ensure there is a digit after the decimal point
            if index + 1 < length and inputCode[index + 1].isdigit(): 
                hasDot = True
                index += 1
            else:
                index += 1
                return {'value': inputCode[startIndex:index], 'type': 'INVALID_NUM'}, None, index
        else:
            break
    
    # Determine if the number is a float or an integer
    if hasDot:
        return {'value': inputCode[startIndex:index], 'type': 'FLOAT'}, index
    else:
        return {'value': inputCode[startIndex:index], 'type': 'INTEGER'}, index
    
def handle_words(inputCode, index, length):
    startIndex = index
    
    while index < length and (inputCode[index].isalnum() or inputCode[index] == '_' or inputCode[index] in SPECIAL_CHAR):
        index += 1
    word = inputCode[startIndex:index]
    
    # Determine the token type for word
    if word in CONSTANT:
        if word == 'e':
            return {'value': word, 'type': 'CONST_E'}, index
        elif word == 'pi':
            return {'value': word, 'type': 'CONST_PI'}, index
    elif word in DATA_TYPE:
        if word == 'length':
            return {'value': word, 'type': 'TYPE_LENGTH'}, index
        elif word == 'surface_area':
            return {'value': word, 'type': 'TYPE_SURFACE_AREA'}, index
        elif word == 'volume':
            return {'value': word, 'type': 'TYPE_VOLUME'}, index
        elif word == 'angle':
            return {'value': word, 'type': 'TYPE_ANGLE'}, index
        elif word == 'time':
            return {'value': word, 'type': 'TYPE_TIME'}, index
        elif word == 'mass':
            return {'value': word, 'type': 'TYPE_MASS'}, index
    elif word in KEYWORD:
        if word == 'let':
            return {'value': word, 'type': 'KEYWORD_LET'}, index
        elif word == 'range':
            return {'value': word, 'type': 'KEYWORD_RANGE'}, index
        elif word == 'print':
            return {'value': word, 'type': 'KEYWORD_PRINT'}, index
        elif word == 'input':
            return {'value': word, 'type': 'KEYWORD_INPUT'}, index
        elif word == 'for':
            return {'value': word, 'type': 'KEYWORD_FOR'}, index
        elif word == 'if':
            return {'value': word, 'type': 'KEYWORD_IF'}, index
        elif word == 'else':
            return {'value': word, 'type': 'KEYWORD_ELSE'}, index
    elif word in RESERVED_WORD:
        if word == 'null':
            return {'value': word, 'type': 'RESERVED_NULL'}, index
        elif word == 'true':
            return {'value': word, 'type': 'RESERVED_TRUE'}, index
        elif word == 'false':
            return {'value': word, 'type': 'RESERVED_FALSE'}, index
        elif word == 'import':
            return {'value': word, 'type': 'RESERVED_IMPORT'}, index
    elif word in UNIT:
        return classify_unit(word), index
    elif word.startswith('_') or word[0].isdigit() or word[0].isupper():
        return {'value': word, 'type': 'INVALID_IDENTIFIER'}, index
    elif any(char in word for char in SPECIAL_CHAR):
        return {'value': word, 'type': 'INVALID_IDENTIFIER'}, index
    else:
        return {'value': word, 'type': 'IDENTIFIER'}, index
    
# Classify unit type
def classify_unit(inputCode):
    if inputCode == 'm' or inputCode == 'meter':
        return {'value': inputCode, 'type': 'UNIT_METER'}
    elif inputCode == 'in' or inputCode == 'inch':
        return {'value': inputCode, 'type': 'UNIT_INCH'}
    elif inputCode == 'ft' or inputCode == 'feet':
        return {'value': inputCode, 'type': 'UNIT_FEET'}
    elif inputCode == 'yd' or inputCode == 'yard':
        return {'value': inputCode, 'type': 'UNIT_YARD'}
    elif inputCode == 'm2':
        return {'value': inputCode, 'type': 'UNIT_SQM'}
    elif inputCode == 'sqin':
        return {'value': inputCode, 'type': 'UNIT_SQIN'}
    elif inputCode == 'sqft':
        return {'value': inputCode, 'type': 'UNIT_SQFT'}
    elif inputCode == 'sqyd':
        return {'value': inputCode, 'type': 'UNIT_SQYD'}
    elif inputCode == 'sqmi':
        return {'value': inputCode, 'type': 'UNIT_SQMI'}
    elif inputCode == 'acre':
        return {'value': inputCode, 'type': 'UNIT_ACRE'}
    elif inputCode == 'hectare':
        return {'value': inputCode, 'type': 'UNIT_HECTARE'}
    elif inputCode == 'm3':
        return {'value': inputCode, 'type': 'UNIT_CBM'}
    elif inputCode == 'L':
        return {'value': inputCode, 'type': 'UNIT_LITER'}
    elif inputCode == 'cc':
        return {'value': inputCode, 'type': 'UNIT_CC'}
    elif inputCode == 'teaspoon':
        return {'value': inputCode, 'type': 'UNIT_TEASPOON'}
    elif inputCode == 'tablespoon':
        return {'value': inputCode, 'type': 'UNIT_TABLESPOON'}
    elif inputCode == 'rad':
        return {'value': inputCode, 'type': 'UNIT_RADIAN'}
    elif inputCode == 'deg' or inputCode == 'degrees':
        return {'value': inputCode, 'type': 'UNIT_DEGREE'}
    elif inputCode == 'grad':
        return {'value': inputCode, 'type': 'UNIT_GRADIAN'}
    elif inputCode == 'sec' or inputCode == 'seconds':
        return {'value': inputCode, 'type': 'UNIT_SECOND'}
    elif inputCode == 'min' or inputCode == 'minutes':
        return {'value': inputCode, 'type': 'UNIT_MINUTE'}
    elif inputCode == 'hr' or inputCode == 'hour':
        return {'value': inputCode, 'type': 'UNIT_HOUR'}
    elif inputCode == 'day':
        return {'value': inputCode, 'type': 'UNIT_DAY'}
    elif inputCode == 'week':
        return {'value': inputCode, 'type': 'UNIT_WEEK'}
    elif inputCode == 'month':
        return {'value': inputCode, 'type': 'UNIT_MONTH'}
    elif inputCode == 'year':
        return {'value': inputCode, 'type': 'UNIT_YEAR'}
    elif inputCode == 'decade':
        return {'value': inputCode, 'type': 'UNIT_DECADE'}
    elif inputCode == 'century':
        return {'value': inputCode, 'type': 'UNIT_CENTURY'}
    elif inputCode == 'g':
        return {'value': inputCode, 'type': 'UNIT_GRAM'}
    elif inputCode == 'ton':
        return {'value': inputCode, 'type': 'UNIT_TON'}
    elif inputCode == 'oz':
        return {'value': inputCode, 'type': 'UNIT_OUNCE'}
    elif inputCode == 'lbs':
        return {'value': inputCode, 'type': 'UNIT_POUND'}
    else:
        return {'value': inputCode, 'type': 'INVALID_UNIT'}

# Run the main function
if __name__ == '__main__':
    main()