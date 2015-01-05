class IntBidirectionalIndexer(object):
  def __init__(self):
    pass

  def resolve(self, index):
    if isinstance(index, (int, long)):
      return index
    else:
      raise TypeError("IntBidirectionalIndexer::resolve expects integer argument")

  def get_index(self, value):
    if isinstance(object, (int, long)):
      return value
    else:
      raise TypeError("IntBidirectionalIndexer::get_index expects integer argument")