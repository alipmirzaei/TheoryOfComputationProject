#   TheoryOfComputationProject by Ali mirzaei and Bardia Vahedi
import networkx as nx
from collections import defaultdict, deque

class DFA:
    def __init__(self, states=set(), alphabets=set(), initial_state=str(), accept_states=set(), transitions=dict()):
        self.states = states
        self.alphabets = alphabets
        self.initial_state = initial_state
        self.accept_states = accept_states
        self.transitions = transitions
    
    def add_state(self, state):
        self.states.add(state)

    def add_alphabet(self, alpha):
        self.alphabets.add(alpha)

    def add_initial_state(self, initial_state):
        self.initial_state = initial_state

    def add_accept_state(self, accept_state):
        self.accept_states.add(accept_state)

    def add_transition(self, state, alpha, dest):
        if state in self.transitions:
            self.transitions[state][alpha] = dest
        else:
            self.destination = {}
            self.destination[alpha] = dest
            self.transitions[state] = self.destination

    def toGraph(self):
        return nx.DiGraph([(start_state, dest_state) for start_state, transition in self.transitions.items() for dest_state in transition.values()])

    def printDFA(self):
        print("\n**************************************")
        print("states are:        ", self.states)
        print("alphabets are:     ", self.alphabets)
        print("initial_state is:  ", self.initial_state)
        print("accept_states are: ", self.accept_states)
        print("transitions are:   ", self.transitions)
        print("**************************************\n")

    def isAccept(self, test_string:str):
            state = self.initial_state
            for symbol in test_string:
                state = self.transitions[state][symbol]
            if state in self.accept_states: return True
            else: return False
        
    def isNull(self):
        visited = [self.initial_state]
        states = deque([self.initial_state])
        while len(states)>0:
            state = states.popleft()
            for next_state in self.transitions[state].values():
                if next_state not in visited: 
                    if next_state in self.accept_states: return False
                    visited.append(next_state)
                    states.append(next_state)
        return True
            
    def isInfinite(self):
        if self.isNull(): return False
        graph = self.toGraph()
        states = nx.descendants(graph, self.initial_state)
        Reachable2Accept = self.accept_states.union(*(nx.ancestors(graph,state)for state in self.accept_states))
        commonstates = states.intersection(Reachable2Accept)
        sub = graph.subgraph(commonstates)
        try:
            longest = nx.dag_longest_path_length(sub)
            return False
        except:
            return True 

    def acceptStringLength(self):
        if not(self.isInfinite() or self.isNull()):
            max_string_length = self.maxstringlength()
            if max_string_length:
                min_string_length = self.minstringlength()
                dfa_graph = self.toGraph()
                count = 0
                for word_length in range(min_string_length, max_string_length + 1):
                    for accept_state in self.accept_states:
                        paths = nx.all_simple_paths(dfa_graph, self.initial_state, accept_state)
                        for path in paths:
                            if len(path) == word_length:
                                count += 1
                return count
   
    def maxstringlength(self):
        if self.isNull(): return 0
        elif self.isInfinite(): return "Infinite!"
        else:
            graph = self.toGraph()
            states=nx.descendants(graph, self.initial_state)
            Reachable2Accept=self.accept_states.union(*(nx.ancestors(graph,state)for state in self.accept_states))
            commonstates=states.intersection(Reachable2Accept)
            sub=graph.subgraph(commonstates)
            return nx.dag_longest_path_length(sub) + 1
            
    def minstringlength(self):
        queue = deque([self.initial_state])
        distances = defaultdict(lambda: None)
        distances[self.initial_state] = 0
        while queue:
            state = queue.popleft()
            if state in self.accept_states:
                return distances[state]
            for next_state in self.transitions[state].values():
                if distances[next_state] is None:
                    distances[next_state] = distances[state] + 1
                    queue.append(next_state)
        return 0
        
    def Complement(self):
        NewAccept=set()
        for state in self.states:
            if state not in self.accept_states: NewAccept.add(state)
        newDFA = DFA(self.states, self.alphabets, self.initial_state, NewAccept, self.transitions)
        return newDFA
        
    def NewDFA(self,dfa2):
            seen=[]
            if self.alphabets != dfa2.alphabets: raise Exception('input symbols do not match!')
            newinitial=self.initial_state+'_'+dfa2.initial_state
            usefulstates={newinitial}
            visited=[newinitial]
            newtransitions={}
            while len(visited)>0:
                state=visited.pop(0)
                for symbol in self.alphabets:
                    nextdfastate=self.transitions[state.split('_')[0]][symbol]+'_'+dfa2.transitions[state.split('_')[1]][symbol]
                    newtransitions[state]=newtransitions.get(state,{})
                    newtransitions[state][symbol]=nextdfastate
                    if nextdfastate not in seen:
                        visited.append(nextdfastate)
                    usefulstates.add(nextdfastate)
                seen.append(state)
            return usefulstates,newinitial,newtransitions
                
        
    def Union(self,other):
        newstates,newinitial,newtransitions=self.NewDFA(other)
        newaccepts=set()
        for state1 in self.accept_states:
            for state2 in other.states:
                newaccepts.add(state1+'_'+state2)
        for state1 in self.states:
            for state2 in other.accept_states:
                newaccepts.add(state1+'_'+state2)
        newDFA=DFA(newstates,self.alphabets,newinitial,newaccepts,newtransitions)
        return newDFA        
                
    
    @classmethod
    def Union(cls,dfa1,dfa2):
        newstates,newinitial,newtransitions=dfa1.NewDFA(dfa2)
        newaccepts=set()
        for state1 in dfa1.accept_states:
            for state2 in dfa2.states:
                newaccepts.add(state1+'_'+state2)
        for state1 in dfa1.states:
            for state2 in dfa2.accept_states:
                newaccepts.add(state1+'_'+state2)
        newDFA=DFA(newstates,dfa1.alphabets,newinitial,newaccepts,newtransitions)
        return newDFA
    
    
    def Difference(self,other):
        newstates,newinitial,newtransitions=self.NewDFA(other)
        newaccepts=set()
        for state1 in self.accept_states:
            for state2 in other.states:
                if state2 not in other.accept_states:
                    newaccepts.add(state1+'_'+state2)
        newDFA=DFA(newstates,self.alphabets,newinitial,newaccepts,newtransitions)
        return newDFA
    
    
    @classmethod
    def Difference(cls,dfa1,dfa2):
        newstates,newinitial,newtransitions=dfa1.NewDFA(dfa2)
        newaccepts=set()
        for state1 in dfa1.accept_states:
            for state2 in dfa2.states:
                if state2 not in dfa2.accept_states:
                    newaccepts.add(state1+'_'+state2)
        newDFA=DFA(newstates,dfa1.alphabets,newinitial,newaccepts,newtransitions)
        return newDFA
    
        
    def Intersection(self,other):
        newstates,newinitial,newtransitions=self.NewDFA(other)
        #def __init__(self, states=set(), alphabets=set(), initial_state=str(), accept_states=set(), transitions=dict()):
        newaccepts=set()
        for state1 in self.states:
            if state1 not in self.accept_states: continue
            for state2 in other.states:
                if state2 in other.accept_states:
                    newaccepts.add(state1+'_'+state2)
        newDFA=DFA(newstates,self.alphabets,newinitial,newaccepts,newtransitions)
        return newDFA
    
    @classmethod
    def Intersection(cls,dfa1,dfa2):
        newstates,newinitial,newtransitions=dfa1.NewDFA(dfa2)
        newaccepts=set()
        for state1 in dfa1.states:
            if state1 not in dfa1.accept_states:continue
            for state2 in dfa2.states:
                if state2 in dfa2.accept_states:
                    newaccepts.add(state1+'_'+state2)
        newDFA = DFA(newstates,dfa1.alphabets,newinitial,newaccepts,newtransitions)
        return newDFA
    
    def isSubset(self, other):
        newstates, newinitial, newtransitions = self.NewDFA(other)
        newaccepts = set()
        #print(newstates)
        for state in newstates:
            state1, state2 = state.split('_')
            #print(state1)
            #print(state2)
            if state1 in self.accept_states and state2 not in other.accept_states:
                newaccepts.add(state1+'_'+state2)
        return not len(newaccepts)

    @classmethod
    def isSubset(cls,dfa1,dfa2):
        newstates, newinitial, newtransitions = dfa1.NewDFA(dfa2)
        newaccepts = set()
        #print(newstates)
        for state in newstates:
            state1, state2 = state.split('_')
            #print(state1)
            #print(state2)
            if state1 in dfa1.accept_states and state2 not in dfa2.accept_states:
                newaccepts.add(state1+'_'+state2)
        return not len(newaccepts)





##   A DFA that accept strings '*aa'
#dfa1 = DFA()
#dfa1.add_state('0')
#dfa1.add_state('1')
#dfa1.add_state('2')
#dfa1.add_alphabet('a')
#dfa1.add_alphabet('b')
#dfa1.add_initial_state('0')
#dfa1.add_accept_state('2')
#dfa1.add_transition('0', 'a', '1')
#dfa1.add_transition('0', 'b', '0')
#dfa1.add_transition('1', 'a', '2')
#dfa1.add_transition('1', 'b', '0')
#dfa1.add_transition('2', 'a', '2')
#dfa1.add_transition('2', 'b', '0')
#
#dfa1.printDFA()
#
#print(dfa1.isAccept('aa'))
#
#print(dfa1.isNull())
#
#print(dfa1.isInfinite())
#
#print(dfa1.acceptStringLength())
#
#print(dfa1.maxstringlength())
#
#print(dfa1.minstringlength())
#
#dfa1.Complement().printDFA()



#   A DFA that accept strings 'b*'
dfa2 = DFA({'0', '1', '2'}               #states
            , {'a','b'}                  #alphabet
            , '0'                        #initial state
            , {'1'}                      #accept_states
            ,{'0': {'a': '2', 'b': '1'}  #transitions
            , '1': {'a': '1', 'b': '1'}  #transitions
            , '2': {'a': '2', 'b': '2'}})#transitions

dfa2.printDFA()

#print(dfa2.isAccept('b'))

#print(dfa2.isNull())

#print(dfa2.isInfinite())

#print(dfa2.acceptStringLength())

#print(dfa2.maxstringlength())

#print(dfa2.minstringlength())

#dfa2.Complement().printDFA()

#dfa1.Intersection(dfa2).printDFA()
#print(dfa1.Intersection(dfa2).isAccept('baa'))


#   A DFA that accept strings 'bb*'
dfa3 = DFA({'0', '1', '2', '3'}          #states
            , {'a','b'}                  #alphabet
            , '0'                        #initial state
            , {'1'}                      #accept_states
            ,{'0': {'a': '3', 'b': '1'}  #transitions
            , '1': {'a': '3', 'b': '2'}  #transitions
            , '2': {'a': '2', 'b': '2'}  #transitions
            , '3': {'a': '3', 'b': '3'}})#transitions

dfa3.printDFA()

print(dfa3.isSubset(dfa2))
#print(DFA.isSubset(dfa3, dfa2))
#dfa2.Intersection(dfa3).printDFA()
#DFA.Intersection(dfa2, dfa3).printDFA()
#dfa4 = DFA({'q0','q1','q2','q3'}       #states
#            ,{'a','b'}                 #alphabet
#            ,'q0'                      #initial state
#            ,{'q3'}                    #Accept state
#            ,{'q0':{'a':'q1','b':'q2'} #transitions
#            ,'q1':{'a':'q1','b':'q0'}  #transitions
#            ,'q2':{'a':'q3','b':'q0'}  #transitions
#            ,'q3':{'a':'q3','b':'q3'}})#transitions
#if dfa4.isAccept('b'):
#    print('Accepted')
#else: print('Rejected')
#if dfa4.isNull():
#    print('Null')
#else: print('Not Null')
#
#
#dfa5 = DFA({'q0','q1'},
#           {'a','b'},
#           'q0',
#           {'q1'},
#           {'q0':{'a':'q1','b':'q0'},
#           'q1':{'a':'q1','b':'q0'}})
#
#dfa6 = DFA({'p0','p1','p2'},
#           {'a','b'},
#           'p0',
#           {'p1'},
#           {'p0':{'a':'p2','b':'p1'},
#           'p1':{'a':'p1','b':'p1'},
#           'p2':{'a':'p2','b':'p2'}})
#print(1)
#usefulstate,newinitial,newtransitions=dfa5.NewDFA(dfa6)
#print(2)
#print(usefulstate,'\n\n',newinitial,'\n\n',newtransitions)