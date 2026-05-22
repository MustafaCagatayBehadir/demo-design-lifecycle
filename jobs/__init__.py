"""The __init__.py module is required for Nautobot to load the jobs via Git."""

from .vlan_svi_design import VlanSviDesign

__all__ = [
    "VlanSviDesign",
]
