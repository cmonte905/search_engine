class binary_tree():
    def __init__(self,rootid):
      self.left = None
      self.right = None
      self.rootid = rootid

    def get_left_child(self):
        return self.left
        
    def get_right_child(self):
        return self.right

    def set_node_value(self,value):
        self.rootid = value

    def get_node_value(self):
        return self.rootid