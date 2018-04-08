# -*- coding: utf-8 -*-
from typing import Any, Dict, Generator

__all__ = ["ChaosParameters", "ServiceFabricAuth"]


ServiceFabricAuth = Generator[Dict[str, Any], None, None]
ChaosParameters = Dict[str, Any]
