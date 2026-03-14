from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class Route:
    route_id: int | None = None
    destination_address: str = ""
    next_hop: str = ""
    metric: int = 0
    interface: str = ""

    def display_info(self) -> str:
        return (
            f"Route(id={self.route_id}, destination={self.destination_address}, "
            f"next_hop={self.next_hop}, metric={self.metric}, interface={self.interface})"
        )


@dataclass
class NetworkDevice:
    device_id: int | None = None
    device_name: str = ""
    manufacturer: str = ""
    model: str = ""
    company_id: int | None = None
    device_type: str = "network_device"

    def summary(self) -> str:
        return (
            f"ID: {self.device_id} | Type: {self.device_type} | Name: {self.device_name} | "
            f"Manufacturer: {self.manufacturer} | Model: {self.model} | Company ID: {self.company_id}"
        )


@dataclass
class Router(NetworkDevice):
    routing_protocol: str = ""
    routing_table: List[Route] = field(default_factory=list)
    device_type: str = "router"

    def add_route(self, route: Route) -> None:
        self.routing_table.append(route)

    def add_routes(self, routes: List[Route]) -> None:
        self.routing_table.extend(routes)

    def print_routing_table(self) -> str:
        if not self.routing_table:
            return "No routes registered."
        return "\n".join(route.display_info() for route in self.routing_table)

    def detailed_summary(self) -> str:
        return f"{self.summary()} | Routing Protocol: {self.routing_protocol}"


@dataclass
class Modem(NetworkDevice):
    modulation_type: str = ""
    downstream_speed_mbps: int = 0
    upstream_speed_mbps: int = 0
    device_type: str = "modem"

    def detailed_summary(self) -> str:
        return (
            f"{self.summary()} | Modulation: {self.modulation_type} | "
            f"Downstream: {self.downstream_speed_mbps} Mbps | "
            f"Upstream: {self.upstream_speed_mbps} Mbps"
        )


@dataclass
class Switch(NetworkDevice):
    number_of_ports: int = 0
    managed: bool = False
    switching_capacity_gbps: float = 0.0
    device_type: str = "switch"

    def detailed_summary(self) -> str:
        return (
            f"{self.summary()} | Ports: {self.number_of_ports} | Managed: {self.managed} | "
            f"Capacity: {self.switching_capacity_gbps} Gbps"
        )


@dataclass
class Company:
    company_id: int | None = None
    name: str = ""
    city: str = ""
    devices: List[NetworkDevice] = field(default_factory=list)

    def add_device(self, device: NetworkDevice) -> None:
        self.devices.append(device)

    def add_devices(self, devices: List[NetworkDevice]) -> None:
        self.devices.extend(devices)

    def print_company(self) -> str:
        header = f"Company: {self.name} (ID: {self.company_id}) - City: {self.city}"
        if not self.devices:
            return header
        return header + "\n" + "\n".join(f"  {device.summary()}" for device in self.devices)
