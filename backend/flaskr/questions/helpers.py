def isValidQuestion(data):
    ''' checks whether the proper body was sent in
        the add question request
     '''
    # these are required fields
    expected = [
        'question',
        'answer',
        'category',
        'difficulty'
    ]
    isValid = True
    for item in expected:
        if item not in data.keys() or data[item] == '':
            isValid = False
    return isValid


def isValidQuizRequest(data):
    ''' checks whether the proper body was sent in
        the quiz request
    '''
    expected = [
        'previous_questions',
        'quiz_category'
    ]
    isValid = True
    for key in expected:
        if key not in data.keys():
            isValid = False
    return isValid
