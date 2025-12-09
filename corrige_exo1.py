from abc import ABC, abstractmethod

class PositionState(ABC):

    def __init__(self, hero):
        self.hero = hero

    def on_enter(self, from_state: "PositionState | None"):
        print(f"[ENTER] {self.name}"
              + (f" (from {from_state.name})" if from_state else ""))

    def on_exit(self, to_state: "PositionState"):
        print(f"[EXIT]  {self.name} -> {to_state.name}")

    @property
    @abstractmethod
    def name(self) -> str:
        pass

     # utilitaire
    def _transition(self, new_state_cls: type["PositionState"], ):
        self.hero.set_state(new_state_cls)

    @abstractmethod
    def to_top_left(self):
        pass

    @abstractmethod
    def to_top_right(self):
        pass

    @abstractmethod
    def to_bottom_left(self):
        pass

    @abstractmethod
    def to_bottom_right(self):
        pass

class TopLeftState(PositionState):

    @property
    def name(self) -> str:
        return "TOP_LEFT"
    
    def to_top_left(self):
        # déjà en TOP_LEFT
        print("Déjà en TOP_LEFT, aucune transition.")

    def to_top_right(self):
        self._transition(TopRightState)

    def to_bottom_left(self):
        self._transition(BottomLeftState)

    def to_bottom_right(self):
        self._transition(BottomRightState)

class TopRightState(PositionState):

    @property
    def name(self) -> str:
        return "TOP_RIGHT"
    
    def to_top_right(self):
        # déjà en TOP_RIGHT
        print("Déjà en TOP_RIGHT, aucune transition.")

    def to_top_left(self):
        self._transition(TopLeftState)

    def to_bottom_left(self):
        self._transition(BottomLeftState)

    def to_bottom_right(self):
        self._transition(BottomRightState)


class BottomLeftState(PositionState):

    @property
    def name(self) -> str:
        return "BOTTOM_LEFT"
    
    def to_bottom_left(self):
        # déjà en BOTTOM_LEFT
        print("Déjà en BOTTOM_LEFT, aucune transition.")

    def to_top_left(self):
        self._transition(TopLeftState)

    def to_top_right(self):
        self._transition(TopRightState)

    def to_bottom_right(self):
        self._transition(BottomRightState)


class BottomRightState(PositionState):

    @property
    def name(self) -> str:
        return "BOTTOM_RIGHT"
    
    def to_bottom_right(self):
        # déjà en BOTTOM_RIGHT
        print("Déjà en BOTTOM_RIGHT, aucune transition.")

    def to_top_left(self):
        self._transition(TopLeftState)

    def to_top_right(self):
        self._transition(TopRightState)

    def to_bottom_left(self):
        self._transition(BottomLeftState)



class PlayableState(ABC):

    def __init__(self, hero):
        self.hero = hero

    def on_enter(self, from_state: "PlayableState | None"):
        print(f"[ENTER] {self.name}"
              + (f" (from {from_state.name})" if from_state else ""))

    def on_exit(self, to_state: "PlayableState"):
        print(f"[EXIT]  {self.name} -> {to_state.name}")

    @property
    @abstractmethod
    def name(self) -> str:
        pass

     # utilitaire
    def _transition(self, new_state_cls: type["PlayableState"], ):
        self.hero.set_state(new_state_cls)

    @abstractmethod
    def to_finished(self):
        pass

    @abstractmethod
    def to_playing(self):
        pass


class PlayingState(PlayableState):

    @property
    def name(self) -> str:
        return "PLAYING"
    
    def to_playing(self):
        # déjà en STATIONARY
        print("Déjà en PLAYING, aucune transition.")

    def to_finished(self):
        self._transition(FinishedState)


class FinishedState(PlayableState):

    @property
    def name(self) -> str:
        return "FINISHED"
    
    def to_finished(self):
        # déjà en MOVING
        print("Déjà en Finished, aucune transition.")

    def to_playing(self):
        self._transition(StationaryState)


class MovementState(ABC):

    def __init__(self, hero):
        self.hero = hero

    def on_enter(self, from_state: "MovementState | None"):
        print(f"[ENTER] {self.name}"
              + (f" (from {from_state.name})" if from_state else ""))

    def on_exit(self, to_state: "MovementState"):
        print(f"[EXIT]  {self.name} -> {to_state.name}")

    @property
    @abstractmethod
    def name(self) -> str:
        pass

     # utilitaire
    def _transition(self, new_state_cls: type["MovementState"], ):
        self.hero.set_state(new_state_cls)

    @abstractmethod
    def to_movement(self):
        pass

    @abstractmethod
    def to_stationary(self):
        pass


class StationaryState(MovementState):

    @property
    def name(self) -> str:
        return "STATIONARY"
    
    def to_stationary(self):
        # déjà en STATIONARY
        print("Déjà en STATIONARY, aucune transition.")

    def to_movement(self):
        self._transition(MovingState)


class MovingState(MovementState):

    @property
    def name(self) -> str:
        return "MOVING"
    
    def to_movement(self):
        # déjà en MOVING
        print("Déjà en MOVING, aucune transition.")

    def to_stationary(self):
        self._transition(StationaryState)



class HeroState(ABC):

    def __init__(self, hero):
        self.hero = hero

    def on_enter(self, from_state: "HeroState | None"):
        print(f"[ENTER] {self.name}"
              + (f" (from {from_state.name})" if from_state else ""))

    def on_exit(self, to_state: "HeroState"):
        print(f"[EXIT]  {self.name} -> {to_state.name}")

    @property
    @abstractmethod
    def name(self) -> str:
        pass

     # utilitaire
    def _transition(self, new_state_cls: type["HeroState"], ):
        self.hero.set_state(new_state_cls)

    def to_movement(self):
        pass

    def to_stationary(self):
        pass

    def to_finished(self):
        pass

class MovingHeroState(HeroState):

    @property
    def name(self) -> str:
        return "MOVING"
    

    def on_enter(self, from_state: "HeroState | None"):
        print(f"[ENTER] {self.name}"
              + (f" (from {from_state.name})" if from_state else ""))

    def on_exit(self, to_state: "HeroState"):
        print(f"[EXIT]  {self.name} -> {to_state.name}")
    


    def to_movement(self):
        # déjà en MOVING
        print("Déjà en MOVING, aucune transition.")

    def to_stationary(self):
        self._transition(StationaryHeroState)

    def to_finished(self):
        self._transition(FinishedHeroState)


class StationaryHeroState(HeroState):

    @property
    def name(self) -> str:
        return "STATIONARY"
    
    def to_stationary(self):
        # déjà en STATIONARY
        print("Déjà en STATIONARY, aucune transition.")

    def to_movement(self):
        self._transition(MovingHeroState)

    def to_finished(self):
        self._transition(FinishedHeroState)

class FinishedHeroState(HeroState):

    @property
    def name(self) -> str:
        return "FINISHED"
    
    def to_finished(self):
        # déjà en FINISHED
        print("Déjà en FINISHED, aucune transition.")

    def to_movement(self):
         print("Déjà en FINISHED, aucune transition.")

    def to_stationary(self):
         print("Déjà en FINISHED, aucune transition.")



class Hero:
    def __init__(self):
        self.hero_state:HeroState = StationaryHeroState(self)
        self.hero_state.on_enter(None)

    # Modifier set_state ou créer une nouvelle méthode, pour gérer les 3 types d'état
    def set_state(self, new_state_cls, action=None):
        old_state = self.hero_state
        new_state = new_state_cls(self)
        # Hooks de sortie / entrée
        old_state.on_exit(new_state)
        new_state.on_enter(old_state)

        self.hero_state = new_state



hero = Hero()
print("Hero initial state:", hero.hero_state.name)
hero.hero_state.to_movement()
print("Hero current state:", hero.hero_state.name)
hero.hero_state.to_movement()
print("Hero current state:", hero.hero_state.name)
hero.hero_state.to_finished()
print("Hero current state:", hero.hero_state.name)
hero.hero_state.to_movement()
print("Hero current state:", hero.hero_state.name)
hero.hero_state.to_stationary()
print("Hero current state:", hero.hero_state.name)