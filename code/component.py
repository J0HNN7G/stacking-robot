# -*- coding: utf-8 -*-

import error


class Component():
    """A class for the hardware components of the robot."""


    def __init__(self):
        """Initialise the component."""
        self.status = False


    def setup(self):
        """Setup the component."""
        pass


    def cleanup(self):
        """Cleanup the component."""
        pass
