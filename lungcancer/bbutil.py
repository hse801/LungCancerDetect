from collections import defaultdict, namedtuple
BB = namedtuple("BoundingBox", "patient slice x y w h klass confidence")
from typing import Dict, List
BBCollections = Dict[str, Dict[str, List[BB]]]