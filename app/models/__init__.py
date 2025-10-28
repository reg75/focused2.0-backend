# app/models/__init__.py

from app.database import Base  # re-export Base for convenience

# Import submodules so their table classes register with Base.metadata
from . import user          # noqa: F401
from . import school        # noqa: F401
from . import department    # noqa: F401
from . import template      # noqa: F401
from . import observation   # noqa: F401
from . import audit_event   # noqa: F401
from . import auth_token    # noqa: F401
from . import login_attempt # noqa: F401
from . import trust         # noqa: F401

__all__ = ["Base"]
