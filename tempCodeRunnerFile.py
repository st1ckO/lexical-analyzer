 #     charStartIndex = index
        
    #     # Find the end of the possible unit
    #     while index < length and not inputCode[index].isspace() and inputCode[index] not in DELIMITER:
    #         index += 1
        
    #     if inputCode[charStartIndex:index] in UNIT:
    #         unitToken = classify_unit(inputCode[charStartIndex:index])
    #     else:   # Invalid Identifier since it's not a valid unit
    #         return {'value': inputCode[startIndex:index], 'type': 'INVALID_UNIT'}, unitToken, index
    