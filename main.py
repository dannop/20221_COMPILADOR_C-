from sys import argv
import re

keyword = ['else', 'if', 'int', 'while', 'return', 'void', 'float']
oper = ['+', '-', '*', '/', '=', '<', '>', '<=', '>=', '==', '!=']
delim = ['\t','\n',',',';','(',')','{','}','[',']', ' ']
num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

p = re.compile(r'(\d+(\.\d+)?([E][+|-]?\d+)?)')

scripty, filename = argv

#file = open(filename)
comment_count = 0
line_comment = 0
is_comment = False
i = 0
iden = "" #null string for identifiers to be built up
print_list = []
end_comment = False #This is a bool value for a block comment
float_str = ""

def is_keyword(kw):
  if kw in keyword:
    return True
  return False

def is_delim(char):
  if char in delim:
    return True
  return False

def which_delim(char):
  if char in delim:
    if char != '\t' and char != '\n' and char != ' ':
      print(char)

def is_digit(char):
  if char in num:
    return True
  return False

def is_char(char):
  c = 0
  c = ord(char)
  if c >= 97 and c <= 122:
    return True
  return False

def is_oper(char):
  if char in oper:
    return True
  return False

def is_num(str):
  try:
    int(str)
    return True
  except:
    return False

def is_float(str):
  m = p.match(str)
  length = len(str)
  if m and length == len(m.group(0)):
    print("FLOAT: %s" %m.group(0))
    return True
  else:
    return False

for line in open(filename):
  if line != '\n':
    print("Input: %s" % (line)),
    
    while line[i] != '\n': #i and enumerate allows to iterate through line
      if line[i] is '/':
        if line[i + 1] is '/' and comment_count is 0: # it's a line comment print it out
          line_comment += 1
        elif line[i + 1] is '*':
          i += 1
          comment_count += 1
      elif (line[i] is '*') and (line[i+1] is '/') and comment_count > 0: 
        comment_count -= 1 
        i += 1
        if comment_count == 0:
          end_comment = True

      if comment_count is 0 and line_comment is 0 and end_comment == False:
        if is_digit(line[i]): #check for float
          j = i
          while not is_delim(line[j]):
            float_str += line[j]
            j += 1
          if is_float(float_str):
            if(j < len(line)):
              i = j
            iden = ''
          float_str = '' #reset string at end use
        if is_char(line[i]) or is_digit(line[i]) and not is_oper(line[i]):
            iden += line[i]
        if is_delim(line[i]) and iden == '': #for delims w/ blank space
            which_delim(line[i])
        if is_oper(line[i]) and iden is '':
          temp = line[i] + line[i + 1]
          if(is_oper(temp)):
            print(temp)
            i += 1
          else:
            print(line[i])
        if not is_char(line[i]) and not is_digit(line[i]) and not is_oper(line[i]) and iden is not '' and not is_delim(line[i]):
          if is_keyword(iden):
            print("keyword: %s" % iden)
            print("ERROR: %s" % line[i])
          elif is_oper(iden):
            print(iden)
            print("Error: %s" % line[i])
          elif is_num(iden):
            print("NUM: %s" % iden)
            print("Error: %s" % line[i])
          else:
            print("ID: %s" % iden)
            print("Error: %s" % line[i])
          iden = ''
        elif not is_char(line[i]) and not is_digit(line[i]) and not is_oper(line[i]) and not is_delim(line[i]):
          print("Error: %s" % line[i])
        if (is_delim(line[i]) or is_oper(line[i])) and iden != '':
          if is_keyword(iden):
            print("keyword: %s" % iden)
          elif is_oper(line[i]):
            temp = line[i] + line[i + 1]
            if is_oper(temp):
              if is_keyword(iden):
                  print("keyword: %s")% iden
              print(temp)
              i += 1
            else:
              print("ID: %s" % iden)
              print(line[i])
          elif is_num(iden):
            print("NUM: %s" % iden) 
          elif is_oper(iden):
            temp = iden + line[i + 1]
            if is_oper(temp):
              print(temp)
              i += 1
            else:
              print(iden)
          else:
              print("ID: %s" % iden)
          which_delim(line[i])
          iden = ''
      i += 1 #increment i
      end_comment = False
    if line[i] == '\n' and iden != '':
      if is_keyword(iden):
        print("keyword: %s" % iden)
      elif is_oper(iden):
        print(iden)
      else:
        print("ID: %s" % iden)
      iden = ''
    line_comment = 0 # reset line commment number
    i = 0 #reset i