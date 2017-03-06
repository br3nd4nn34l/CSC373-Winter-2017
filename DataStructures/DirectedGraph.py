from DataStructures import Helpers
from copy import deepcopy

class DirectedGraph:

    def __init__(self):
        # Current id number of this graph
        self.id_number = 0

        # Set of used ids
        self.ids = set()

        # Dict that maps node ids to node contents
        self.content_map = {}

        # Set of free id-numbers (allows for deletion)
        self.free_ids = set()

        # Dicts for mapping children with parents
        # Dict that maps node IDs to the IDs of nodes that they enter
        self.children = {}
        # Dict that maps node IDs to the IDs of nodes that are entered fro
        self.parents = {}

    def add_node(self, content):

        # Get an id number
        new_id = self._get_new_id()

        # Add content to content map
        self.content_map[new_id] = content

        # Register the id number in the parent and child dictionaries
        self.children[new_id] = {}
        self.parents[new_id] = {}

    def connect_nodes(self, id1, id2, weight):
        """
        Creates an edge from id1 -> id2 (id1 parent of id2) with weight weight
        """
        # Register id2 as a child of id1
        self.children[id1][id2] = weight
        # Register id2 as a parent of id1
        self.parents[id2][id1] = weight

    # TODO: Need to fix deletion
    def disconnect_nodes(self, id1, id2):
        """
        Removes the edge going from id1 -> id2
        """
        Helpers.safe_dict_delete(self.children[id1], id2)
        Helpers.safe_dict_delete(self.parents[id2], id1)

    def remove_node(self, target_id):

        # Remove the target id from the set of used ids
        self.ids.remove(target_id)
        # Add the target id to the set of free ids
        self.free_ids.add(target_id)

        # Remove the node from the content map
        Helpers.safe_dict_delete(self.content_map, target_id)

        # Disconnect the target from all relatives

        # Disconnect all entering edges
        for parent_id in self.parents:
            self.disconnect_nodes(parent_id, target_id)
        Helpers.safe_dict_delete(self.parents, target_id)

        # Disconnect all leaving edges
        child_ids = list(self.children[target_id].keys())
        for child_id in child_ids:
            self.disconnect_nodes(target_id, child_id)
        Helpers.safe_dict_delete(self.children, target_id)

    def _get_new_id(self):

        # Grab a free id if possible
        if len(self.free_ids) != 0:
            ret_id = self.free_ids.pop()

        # Otherwise just use the stored value and increment it after grabbing it
        else:
            ret_id = self.id_number
            self.id_number += 1

        # Add the id to the used id set
        self.ids.add(ret_id)

        # Return the id
        return ret_id

    def transpose(self):
        """
        Flip direction of edges in graph
        """

        ret_graph = deepcopy(self)
        parents, children = ret_graph.parents, ret_graph.children
        ret_graph.parents = children
        ret_graph.children = parents

        return ret_graph

    def children_of(self, target_id):
        return self.children[target_id].keys()





G = DirectedGraph()
for i in range(5):
    G.add_node(i + 1)
G.connect_nodes(0, 1, 4)
G.connect_nodes(1, 2, 5)
G.connect_nodes(1, 4, 9)
G.connect_nodes(2, 3, 7)
G.connect_nodes(2, 4, 6)
G.connect_nodes(4, 3, 8)
print(G.children)
print(G.parents)
G.remove_node(2)
print(G.children)
print(G.parents)
