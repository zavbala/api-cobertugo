from .ana import Ana
from .qualitas import Qualitas
from .zurich import Zurich
from .afirme import Afirme
from .hdi import Hdi
from .primero import Primero


__all__ = ["Ana", "Qualitas", "Zurich"]

TREE = {
    "ANA": Ana,
    "HDI": Hdi,
    "AFIRME": Afirme,
    "ZURICH": Zurich,
    "PRIMERO": Primero,
    "QUALITAS": Qualitas,
}
