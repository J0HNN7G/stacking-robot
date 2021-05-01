# -*- coding: utf-8 -*-

import error
from abc import ABC, abstractmethod

class Component(ABC):

    @property
    def status(self):
        return self._status

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def cleanup(self):
        pass

    @status.setter
    def status(self, val):
        error.checkType(val, bool, 'status must be a boolean!')
        self._status = val