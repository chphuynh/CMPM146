#bt_nodes
from copy import deepcopy
import logging


def log_execution(fn):
    def logged_fn(self, state):
        logging.debug('Executing:' + str(self))
        result = fn(self, state)
        logging.debug('Result: ' + str(self) + ' -> ' + ('Success' if result else 'Failure'))
        return result
    return logged_fn

    

############################### Base Classes ##################################
class Node:
    def __init__(self):
        raise NotImplementedError

    def execute(self, state):
        raise NotImplementedError

    def copy(self):
        return deepcopy(self)


class Composite(Node):
    def __init__(self, child_nodes=[], name=None):
        self.child_nodes = child_nodes
        self.name = name

    def execute(self, state):
        raise NotImplementedError

    def __str__(self):
        return self.__class__.__name__ + ': ' + self.name if self.name else ''

    def tree_to_string(self, indent=0):
        string = '| ' * indent + str(self) + '\n'
        for child in self.child_nodes:
            if hasattr(child, 'tree_to_string'):
                string += child.tree_to_string(indent + 1)
            else:
                string += '| ' * (indent + 1) + str(child) + '\n'
        return string


class Decorator(Node):
    def __init__(self,child_node=None, name=None):
        self.child_node = child_node
        self.name = name
        
    def execute(self, state):
        raise NotImplementedError
        
    def __str__(self, state):
        return self.__class__.__name__ + ': ' + self.name if self.name else ''
        
    def tree_to_string(self, indent=0):
        string = '| ' * indent + str(self) + '\n'
        if hasattr(self.child_node, 'tree_to_string'):
            string += self.child_nodechild_node.tree_to_string(indent + 1)
        else:
            string += '| ' * (indent + 1) + str(self.child_node) + '\n'
        return string        

      
############################# Decorator Nodes ###############################

class Inverter(Decorator):
    @log_execution
    def execute(self, state):
        invert_execution = self.child_node.execute(state)
        if not continue_execution:
            return True
        else:
            return False


class Succeeder(Decorator):
    @log_execution
    def execute(self, state):
        succeed_execution = self.child_node.execute(state)
        return True

class RepeatUntilFail(Decorator):
    @log_execution
    def execute(self, state):
        repeat_execution = True
        while repeat_execution:
            repeat_execution = self.child_node.execute(state)
        return True    

class Repeater(Decorator):
    @log_execution
    def execute(self, state):
        repeat_counter = 0;
        while repeat_counter < 3:
            repeat_execution = self.child_node.execute(state)
            repeat_counter = repeat_counter + 1
        return True
        
    
############################### Composite Nodes ##################################
class Selector(Composite):
    @log_execution
    def execute(self, state):
        for child_node in self.child_nodes:
            success = child_node.execute(state)
            if success:
                return True
        else:  # for loop completed without success; return failure
            return False


class Sequence(Composite):
    @log_execution
    def execute(self, state):
        for child_node in self.child_nodes:
            continue_execution = child_node.execute(state)
            if not continue_execution:
                return False
        else:  # for loop completed without failure; return success
            return True


############################### Leaf Nodes ##################################
class Check(Node):
    def __init__(self, check_function):
        self.check_function = check_function

    @log_execution
    def execute(self, state):
        return self.check_function(state)

    def __str__(self):
        return self.__class__.__name__ + ': ' + self.check_function.__name__


class Action(Node):
    def __init__(self, action_function):
        self.action_function = action_function

    @log_execution
    def execute(self, state):
        return self.action_function(state)

    def __str__(self):
        return self.__class__.__name__ + ': ' + self.action_function.__name__
