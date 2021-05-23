# -*- coding: utf-8 -*-

import error


class Component():
    """A class for the hardware components of the robot."""


    def __init__(self):
        # type: (...) -> (...)
        """Initialise the component."""
        self.status = False


    def setup(self):
        # type: (...) -> (...)
        """Setup the component."""
        pass


    def cleanup(self):
        # type: (...) -> (...)
        """Cleanup the component."""
        pass
