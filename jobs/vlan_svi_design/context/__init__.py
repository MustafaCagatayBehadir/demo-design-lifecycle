"""Render context for the L2 datacenter VLAN and SVI design."""

from nautobot.dcim.models import Location
from nautobot.ipam.models import Namespace, VLANGroup
from nautobot_design_builder.context import Context, context_file
from nautobot_design_builder.errors import DesignValidationError


@context_file("context.yaml")
class VlanSviContext(Context):
    """Render context for L2 datacenter VLAN and SVI design.

    Job input vars (location, vlan_group, ip_namespace, devices) are populated
    at runtime from the job form. The vlans list is loaded from context.yaml
    and defines the service's VLAN topology.
    """

    location: Location
    vlan_group: VLANGroup
    ip_namespace: Namespace
    devices: list
    vlans: list

    def validate_vlan_ids(self):
        """Ensure all VLAN IDs are within the valid 802.1Q range."""
        for vlan in self.vlans:
            vid = vlan.get("id")
            if not isinstance(vid, int) or not (1 <= vid <= 4094):
                raise DesignValidationError(
                    f"VLAN id {vid!r} is invalid — must be an integer between 1 and 4094."
                )

    def validate_unique_vlan_ids(self):
        """Ensure no duplicate VLAN IDs exist in the context."""
        seen = set()
        for vlan in self.vlans:
            vid = vlan.get("id")
            if vid in seen:
                raise DesignValidationError(
                    f"Duplicate VLAN id {vid} found in context.yaml."
                )
            seen.add(vid)
