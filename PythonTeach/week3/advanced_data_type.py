var = list()
print(var)
var.append(4)
print(var)
var.append('String')
print(var)
var.append(10.44)
print(var)
var.remove('String')
print(var)
# var.remove('Unknown')

var = set()
print(var)
var.add(10)
print(var)
var.add('String')
print(var)
var.add(14)
print(var)
var.remove('String')
print(var)
# s.remove('Value')

var = dict()
print(var)
var['Key'] = 'Value'
print(var)
var[4] = 'String'
print(var)
var[20.2] = 99.4
print(var)
var.pop(4)
print(var)
# print(var.pop('Key'))
# var.pop('Unknown')