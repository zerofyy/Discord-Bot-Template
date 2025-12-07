try:
    from .bot import *
    from .database import *

except ImportError:
    pass

from .installer import *
