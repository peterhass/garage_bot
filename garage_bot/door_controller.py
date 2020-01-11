import time
from threading import Lock
import logging

class DoorStates:
    OPEN = 'open'
    CLOSED = 'closed'
    OPENING = 'opening'
    CLOSING = 'closing'

class UnexpectedDoorStateException(Exception):
    pass


class DoorController:
    def __init__(self, door_io=None):
        self.door_io = door_io
        self.lock = Lock()

        self.__wait()
        self._state = None

        if door_io.is_switch_on():
            self.state = DoorStates.OPEN
        else:
            self.state = DoorStates.CLOSED

        door_io.on_switch_changed(self.external_door_state_change)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        logging.info("Controller door state change from '{}' to '{}'".format(self._state, new_state))
        self._state = new_state

    def external_door_state_change(self, is_switch_on):
        logging.info("Controller notified about door switch state change. self.state = {}, is_switch_on={}".format(self.state, is_switch_on))
        if self.state in [DoorStates.OPENING, DoorStates.CLOSING]:
            return

        with self.lock:
            switch_state = is_switch_on
        
            if switch_state:
                self.state = DoorStates.OPEN
            else:
                self.state = DoorStates.CLOSED

    @property
    def status_text(self):
        TEXTS = {
                DoorStates.OPEN: 'Tor ist offen',
                DoorStates.CLOSED: 'Tor ist geschlossen',
                DoorStates.OPENING: 'Tor oeffnet gerade',
                DoorStates.CLOSING: 'Tor schliesst gerade'
                }

        return TEXTS[self.state]

    @property
    def can_open(self):
        return self.state is DoorStates.CLOSED

    def open(self):
        with self.lock:
            return self.__open()

    def __open(self):
        if not self.can_open:
            raise Exception('door not closed therefore cannot be opened')

        logging.info("Controller starts door opening process")
        self.door_io.trigger_relais()
        self.state = DoorStates.OPENING
        self.__wait()

        if self.door_io.is_switch_on():
            self.state = DoorStates.OPEN
        else:
            self.state = DoorStates.CLOSED
            raise UnexpectedDoorStateException('Door reports as closed')
            

    @property
    def can_close(self):
        return self.state is DoorStates.OPEN

    def close(self):
        with self.lock:
            return self.__close()

    def __close(self):
        if not self.can_close:
            raise Exception('door not open therefore cannot be closed')

        logging.info("Controller starts door closing process")
        self.door_io.trigger_relais()
        self.state = DoorStates.CLOSING
        self.__wait()

        if not self.door_io.is_switch_on():
            self.state = DoorStates.CLOSED
        else:
            self.state = DoorStates.OPEN
            raise UnexpectedDoorStateException('Door reports as open')

    @property
    def is_open(self):
        return self.state == DoorStates.OPEN
        
    def __wait(self):
        BUFFER = 5
        WAIT_TIME = 15 + BUFFER
        logging.info("Waiting {} seconds for door to fully close or open".format(WAIT_TIME))
        time.sleep(WAIT_TIME)
