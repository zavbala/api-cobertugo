from .ana import Ana
from .qualitas import Qualitas
from .zurich import Zurich
from .afirme import Afirme


__all__ = ["Ana", "Qualitas", "Zurich"]

TREE = {
    "ANA": Ana,
    "AFIRME": Afirme,
    "ZURICH": Zurich,
    "QUALITAS": Qualitas,
}
