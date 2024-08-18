import os

class ArgParser():
  def __init__(self, args : list) -> None:
    self.files : list = []
    self.out : str = ''
    self.delete : bool = False

    self.parse_args(args)

  def parse_args(self, args) -> None:
    # Raises ValueError is not in list
    out_index = args.index('--out')

    try:
      delete_index = args.index('--delete')
    except ValueError : 
      delete_index = None

    # Setting the values
    for j in args[:out_index] :
      # Case we just want to make a pdf out of a sorted directory
      if os.path.isdir(j):
        self.files = [os.path.join(j, f) for f in os.listdir(j)]
        continue
      # Usual case for image_maker
      if os.path.exists(j):
        self.files.append(j)
      else:
        raise FileNotFoundError("Check your path, the file or directory doesnt' exist.", j)
    
    # Parsing out path
    self.out = args[out_index + 1]
    dir = os.path.dirname(self.out)
    if not dir :
      self.out = os.path.join('.', self.out)

    elif not os.path.isdir(dir):
      raise FileNotFoundError("The folder specified for out doesn't exist", dir)
    
    # plot twist : you need to specify the name of the out file
    name, ext = os.path.splitext(os.path.basename(self.out))
    if not (name and ext):
      raise Exception("You must specify a file name and extension")

    if delete_index : 
      self.delete = True    
