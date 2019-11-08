def isValidQuestion(data):
    ''' checks whether the proper body was sent in
        the request
     '''
    expected = [
        'question',
        'answer',
        'category',
        'difficulty'
    ]
    isValid = True
    for item in data.keys():
        if item not in expected:
            isValid = False
    if len(data.keys()) != len(expected):
        isValid = False
    return isValid