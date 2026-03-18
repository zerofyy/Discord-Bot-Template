try:
    from .bot import *
    from .database import *

except ImportError:
    pass

from .command_args import *
from .installer import *
