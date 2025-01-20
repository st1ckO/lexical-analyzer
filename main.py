import csv
import os

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
            
        # Call the lexical analyzer
        tokens = lexical_analyzer(inputCode)
        
        # Output the tokens to a CSV file
        outputName = input('Enter the output file name (don\'t include file extension): ')
        if not outputName:
            raise ValueError('Output file name cannot be empty.')
        
        outputFileName = outputName + '.csv'
        
        # Write tokens to the CSV file
        with open(outputFileName, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, quotechar=None)
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
    DELIMITER = [',', ';', ':', '(', ')', '{', '}', '[', ']']
    OPERATOR = ['=', '+', '-', '*', '/' '%', '^', '!', '|', '&', '<', '>']
    
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
        
        # Handle quotation marks
        if char in ["'", '"']:
            token, index = handle_quotes(inputCode, index, length)
            tokens.append(token)
            previousToken = token
            continue
        
        # Handle delimiters
        if char in DELIMITER:
            token = handle_delimiters(inputCode, index)
            tokens.append(token)
            previousToken = token  
            index += 1
            continue
        
        # # Handle operators
        # if char in OPERATOR:
        #     token, index = handle_operators(inputCode, index, previousToken)
        
    return tokens

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
            break
        
        # Otherwise, add the character to the value
        value += char
        index += 1
        
    # If the closing quote is not found, it's invalid
    return {'value': value[startIndex:index], 'type': 'INVALID'}, index

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

# # Process operators
# def handle_operators(inputCode, index, previousToken)
#     VALID_OP = ['=', '+=', '-=', '*=', '/=', '%=' ]


# Run the main function
if __name__ == '__main__':
    main()