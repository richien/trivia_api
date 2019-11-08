def isValidQuestion(data):
    ''' checks whether the proper body was sent in
        the request
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