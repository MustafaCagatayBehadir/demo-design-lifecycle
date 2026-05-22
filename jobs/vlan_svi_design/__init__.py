"""Design job to provision L2 datacenter VLANs and SVI interfaces."""

from nautobot.apps.jobs import MultiObjectVar, ObjectVar, register_jobs
from nautobot.dcim.models import Device, Location
from nautobot.ipam.models import Namespace, VLANGroup
from nautobot_design_builder.choices import DesignModeChoices
from nautobot_design_builder.design_job import DesignJob

from .context import VlanSviContext


class VlanSviDesign(DesignJob):
    """Provision VLANs, IP prefixes, SVI interfaces, and gateway IPs across L3 switches."""

    location = ObjectVar(
        label="Location",
        description="Datacenter location to associate VLANs with",
        model=Location,
        required=True,
    )

    vlan_group = ObjectVar(
        label="VLAN Group",
        description="VLAN group to assign created VLANs to",
        model=VLANGroup,
        required=True,
    )

    ip_namespace = ObjectVar(
        label="Namespace",
        description="IP namespace for prefix and address allocation",
        model=Namespace,
        required=True,
    )

    devices = MultiObjectVar(
        label="Devices",
        description="Layer-3 switches to provision SVI interfaces on",
        model=Device,
        required=True,
    )

    class Meta:
        """Metadata for the L2 datacenter VLAN and SVI design job."""

        name = "L2 Datacenter VLAN and SVI Design"
        design_mode = DesignModeChoices.DEPLOYMENT
        dryrun_default = True
        has_sensitive_variables = False
        design_files = [
            "designs/0001_vlans.yaml.j2",
            "designs/0002_prefixes.yaml.j2",
            "designs/0003_svi.yaml.j2",
        ]
        context_class = VlanSviContext
        version = "0.1.1"
        description = (
            "Provisions VLANs, IP prefixes, SVI virtual interfaces, and gateway "
            "IP addresses for a Layer 2 datacenter service across specified switches."
        )


name = "Service Lifecycle"
register_jobs(VlanSviDesign)
