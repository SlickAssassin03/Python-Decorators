"""
work from here
"""

class Commands(object):

  class Command(object):
    def __init__(self,*args,name=None,aliases=None):
      if (name is None):
        raise Exception('A name must be passed!')
      if (aliases is None):
        self.names = [name]
      else:
        self.names = [name,*aliases]
      self.function = None
      # Continues in __call__...
    def __call__(self,function,*args,**kwargs):
      # Continued from __init__...
      if self.function is None:
        self.function = function
        Commands.add_command(self.function,self.names)
      return self.function

  def __init__(self,debug=False):
    """Parent function to command decorator."""
    if not isinstance(debug, bool):
        raise ValueError('Debug should be type "bool"')
        debug = False
    self.debug = debug
    self.command_list = []   # [[name,aliases],...] [0] should be main name
    self.function_dict = {}  # {name:function,...}

  @classmethod
  def parse_input(cls,command):
    in_quote,quotes = [False,''],['"',"'"]
    string = []
    final = []
    for char in command:
      if in_quote[0]:
        if (char==in_quote[1]):
          in_quote = [False,'']
          final.append(''.join(string))
          string.clear()
          continue
        string.append(char)
      elif char in quotes:
        in_quote = [True,char]
        final.append(''.join(string))
        string.clear()
        continue
      elif (char==' '):
        final.append(''.join(string))
        string.clear()
      else:
        string.append(char)
      continue
    final.append(''.join(string))
    return [word for word in final if word.strip()]

  def command_input(self,cmd,*args):
    """Returns [0] if not found, and [function,name] if found."""
    out = [0,cmd]
    for names in self.command_list:
      if cmd in names:
        out = [self.function_dict.get(names[0],1),names[0]]
        break
    if (out[0]==1):
      raise Exception('Unknown Error: Command name found but key not!')
    return out

  def add_command(self,function,names):
    """Not to be called, use @object.Command(name='',aliases=[])"""
    self.command_list.append(names)
    self.function_dict.update({names[0]:function})


Commands = Commands()

@Commands.Command(name='clear')
def clear():
  system('clear')

@Commands.Command(name='test',aliases=['test1','test2'])
def test():
  print('test')

@Commands.Command(name='dump',aliases=['list'])
def dump():
  out = []
  for names in Commands.command_list:
    out.append(f'Command: {names[0]}\nAliases: {", ".join(names[1:])}\nFunction: {Commands.function_dict.get(names[0])}')
  print('\n\n'.join(out))

while True:
  cmd = Commands.parse_input(input('>>> '))
  out = Commands.command_input(cmd[0])

  if (out[0]==0):
    print(f'\'{out[1]}\' not recognized as a command')
    continue
  else:
    run,last_command = out
    print('\nOutput:')
    
    try:
      run(*cmd[1:])
    except TypeError:
      print('TypeError: Too few or too little arguments given!')
    except:
      print('Unknown error...')
