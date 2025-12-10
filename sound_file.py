import subprocess
import signal
from abc import ABC, abstractmethod


class AudioFileState(ABC):
    def __init__(self, player: "AudioPlayer"):
        self.player = player

    def _transition(self, new_state):
        self.player.state = new_state(self.player)

    @abstractmethod
    def play(self): pass
    @abstractmethod
    def pause(self): pass
    @abstractmethod
    def stop(self): pass


# -----------------------------------
# STATES
# -----------------------------------

class PlayState(AudioFileState):
    def play(self):
        print("Déjà en lecture.")

    def pause(self):
        print("Pause.")
        if self.player.process:
            self.player.process.send_signal(signal.SIGSTOP)
        self._transition(PauseState)

    def stop(self):
        print("Stop.")
        if self.player.process:
            self.player.process.kill()
            self.player.process = None
        self._transition(StopState)


class PauseState(AudioFileState):
    def play(self):
        print("Reprise.")
        if self.player.process:
            self.player.process.send_signal(signal.SIGCONT)
        self._transition(PlayState)

    def pause(self):
        print("Déjà en pause.")

    def stop(self):
        print("Stop.")
        if self.player.process:
            self.player.process.kill()
            self.player.process = None
        self._transition(StopState)


class StopState(AudioFileState):
    def play(self):
        print("Lecture.")
        self.player._start_audio()
        self._transition(PlayState)

    def pause(self):
        print("Impossible de mettre en pause, audio stoppé.")

    def stop(self):
        print("Déjà stoppé.")


# -----------------------------------
# AUDIO PLAYER
# -----------------------------------

class AudioPlayer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.process = None
        self.state = StopState(self)

    def _start_audio(self):
        self.process = subprocess.Popen(["afplay", self.file_path])

    def play(self):
        self.state.play()
        self.debug()

    def pause(self):
        self.state.pause()
        self.debug()

    def stop(self):
        self.state.stop()
        self.debug()

    def debug(self):
        print("État actuel:", self.state.__class__.__name__)
        print()
