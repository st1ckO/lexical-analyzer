 # elif char == '.':
        #     if hasDot: # Invalid float
        #         return {'value': inputCode[numStartIndex:index], 'type': 'INVALID_NUM'}, index
        #     if index + 1 < length and inputCode[index + 1].isdigit(): # Ensure there is a digit after the decimal point
        #         hasDot = True
        #         index += 1
        #     else:
        #         break
        # else:
        #     break