# 2.1
def estimate(target, role):
    return 'ESTIMATE Agent[' + "{0:02d}".format(target) + '] ' + role

def comingout(target, role):
    return 'COMINGOUT Agent[' + "{0:02d}".format(target) + '] ' + role

# 2.2
def divine(target):
    return 'DIVINE Agent[' + "{0:02d}".format(target) + ']'

def guard(target):
    return 'GUARD Agent[' + "{0:02d}".format(target) + ']'

def vote(target):
    return 'VOTE Agent[' + "{0:02d}".format(target) + ']'

def attack(target):
    return 'ATTACK Agent[' + "{0:02d}".format(target) + ']'

# 2.3
def divined(target, species):
    return 'DIVINED Agent[' + "{0:02d}".format(target) + '] ' + species

def identified(target, species):
    return 'IDENTIFIED Agent[' + "{0:02d}".format(target) + '] ' + species

def guarded(target):
    return 'GUARDED Agent[' + "{0:02d}".format(target) + ']'

# 2.4
def agree(message):
    return 'AGREE '+ message

def disagree(message):
    return 'DISAGREE '+ message

# 2.5
def skip():
    return 'Skip'

def over():
    return 'Over'

# 3
def request(text):
    return 'REQUEST ANY (' + text + ')'

# 5
def because(premise, conclusion):

    support = '('+premise+')'
    claim = '('+conclusion+')'

    return 'BECAUSE '+ support +' '+ claim
