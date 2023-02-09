
#   TheoryOfComputationProject by Ali mirzaei and Bardia Vahedi

class DFA:
    def __init__(self):
        self.states = set()
        self.alphabets = set()
        self.start_state = str()
        self.accept_states = set()
        self.transitions = dict()
    
    def add_state(self, state):
        self.states.add(state)

    def add_alphabet(self, alpha):
        self.alphabets.add(alpha)

    def add_start_state(self, start_state):
        self.start_state = start_state

    def add_accept_state(self, accept_state):
        self.accept_states.add(accept_state)

    def add_transition(self, state, alpha, dest):
        if state in self.transitions:
            self.transitions[state][alpha] = dest
        else:
            self.destination = {}
            self.destination[alpha] = dest
            self.transitions[state] = self.destination

    def printDFA(self):
        print("states are:        ", self.states)
        print("alphabets are:     ", self.alphabets)
        print("start_state is:    ", self.start_state)
        print("accept_states are: ", self.accept_states)
        print("transitions are:   ", self.transitions)

    def isAccept(self, string):

        self.current_state = self.start_state

        for char in string:
            self.current_state = self.transitions[(self.current_state, char)]
        if (self.current_state in self.accept_states):
            return True
        else:
            return False

    def isEmpty(self):
        Reachables = []
        queue = []
        Reachables.append(self.start_state)
        queue.append(self.start_state)
        isempty = True

        while queue:
            state = queue.pop(0)

            for next_state in self.transitions[state].values():
                if next_state not in Reachables:
                    if next_state in self.accept_states:
                        isempty = False
                    Reachables.append(next_state)
                    queue.append(next_state)

        return isempty

    def isInfinite(self):
        for test_string in range(len(self.states), len(self.states)*2):
            pass




#   A DFA that accept strings '*aa'
dfa = DFA()

dfa.add_state('0')
dfa.add_state('1')
dfa.add_state('2')

dfa.add_alphabet('a')
dfa.add_alphabet('b')

dfa.add_start_state('0')

dfa.add_accept_state('2')

dfa.add_transition('0', 'a', '1')
dfa.add_transition('0', 'b', '0')
dfa.add_transition('1', 'a', '2')
dfa.add_transition('1', 'b', '0')
dfa.add_transition('2', 'a', '2')
dfa.add_transition('2', 'b', '0')

dfa.printDFA()

dfa.isAccept('aaaabaa')

dfa.isEmpty()