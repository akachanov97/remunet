from mininet.net import Containernet


REMUNET_VERSION = "0.0.1"


class Remunet( Containernet ):
    """
        Remote access to containernet
    """

    def __init__(self, **params):
        super().__init__(**params)
