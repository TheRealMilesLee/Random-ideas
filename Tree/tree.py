class Tree:

  def __init__(self, data):
    self.data = data
    self.child = None
    self.down = None
    self.up = None
    self.left = None
    self.right = None


def construct_a_tree() -> list:
  Tree_list = []
  root_node = Tree(0)

  node_1 = Tree(1)
  root_node.child = node_1
  root_node.down = node_1

  node_2 = Tree(2)
  node_1.child = node_2
  node_1.left = node_2

  node_3 = Tree(3)
  node_2.child = node_3
  node_2.left = node_3

  node_4 = Tree(4)
  node_3.right = node_4
  node_2.right = node_4
  node_3.child = node_4
  node_2.child = node_4
  node_4.left = node_1

  node_5 = Tree(5)
  node_1.child = node_5
  node_1.right = node_5

  Tree_list.append(root_node)
  Tree_list.append(node_1)
  Tree_list.append(node_2)
  Tree_list.append(node_3)
  Tree_list.append(node_4)
  Tree_list.append(node_5)
  return Tree_list


if __name__ == '__main__':
  tree = construct_a_tree()
  print(tree[0].data)
  for nodes in tree:
    if (nodes.left != None):
      print(nodes.left.data)
    if (nodes.right != None):
      print(nodes.right.data)
