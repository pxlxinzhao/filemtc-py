import re

def trim(x):
    return re.sub('[\[\]]', '', x);

def capitalize(x):
    return x[0].upper() + x[1:]

def deCapitalize(x):
    return x[0].lower() + x[1:]


def camel_case(x):
    x = trim(x)

    index = x.find('_')
    if index == -1:
        return x
    else:
        result = x[:index] + capitalize(x[index + 1:])
        return camel_case(result)

def make_alias(x):
    return capitalize(camel_case(x))

def replaceTask(x, tableName):
    x = x.replace('Task', tableName)
    x = x.replace('TASK', tableName)
    x = x.replace('task', deCapitalize(tableName))
    return x
