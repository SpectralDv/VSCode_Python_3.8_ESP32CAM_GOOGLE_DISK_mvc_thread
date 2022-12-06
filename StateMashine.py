
from IState import IState


class StateMashine:
    currentState = IState()
    def Initialize(self,startState):
        self.currentState = startState
        self.currentState.Enter()
    def ChangeState(self,newState):
        self.currentState.Exit()
        self.currentState = newState
        self.currentState.Enter()