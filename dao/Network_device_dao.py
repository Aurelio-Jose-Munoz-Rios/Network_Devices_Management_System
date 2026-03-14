from __future__ import annotations

from typing import Any

from model.Network_devices_model import Company, Modem, NetworkDevice, Route, Router, Switch


class CompanyDAO:
    def __init__(self, db_connector):
        self.db = db_connector

    def create(self, company: Company) -> int:
        query = "INSERT INTO Company (name, city) VALUES (%s, %s)"
        return self.db.execute_query(query, (company.name, company.city))

    def get_all(self) -> list[Company]:
        rows = self.db.fetch_all("SELECT id, name, city FROM Company ORDER BY id")
        return [Company(company_id=row["id"], name=row["name"], city=row["city"]) for row in rows]

    def update(self, company_id: int, name: str, city: str) -> None:
        self.db.execute_query("UPDATE Company SET name = %s, city = %s WHERE id = %s", (name, city, company_id))

    def delete(self, company_id: int) -> None:
        self.db.execute_query("DELETE FROM Company WHERE id = %s", (company_id,))


class NetworkDeviceDAO:
    def __init__(self, db_connector):
        self.db = db_connector

    def create_base_device(self, device: NetworkDevice) -> int:
        query = """
            INSERT INTO NetworkDevice (device_name, manufacturer, model, company_id, device_type)
            VALUES (%s, %s, %s, %s, %s)
        """
        return self.db.execute_query(
            query,
            (device.device_name, device.manufacturer, device.model, device.company_id, device.device_type),
        )

    def update_base_device(self, device_id: int, device: NetworkDevice) -> None:
        query = """
            UPDATE NetworkDevice
            SET device_name = %s, manufacturer = %s, model = %s, company_id = %s
            WHERE id = %s
        """
        self.db.execute_query(
            query,
            (device.device_name, device.manufacturer, device.model, device.company_id, device_id),
        )

    def delete_base_device(self, device_id: int) -> None:
        self.db.execute_query("DELETE FROM NetworkDevice WHERE id = %s", (device_id,))


class RouteDAO:
    def __init__(self, db_connector):
        self.db = db_connector

    def create(self, router_id: int, route: Route) -> int:
        query = """
            INSERT INTO Route (router_id, destination_address, next_hop, metric, interface)
            VALUES (%s, %s, %s, %s, %s)
        """
        return self.db.execute_query(
            query,
            (router_id, route.destination_address, route.next_hop, route.metric, route.interface),
        )

    def get_all(self) -> list[Route]:
        rows = self.db.fetch_all(
            "SELECT id, destination_address, next_hop, metric, interface FROM Route ORDER BY id"
        )
        return [
            Route(
                route_id=row["id"],
                destination_address=row["destination_address"],
                next_hop=row["next_hop"],
                metric=row["metric"],
                interface=row["interface"],
            )
            for row in rows
        ]

    def get_by_router(self, router_id: int) -> list[Route]:
        rows = self.db.fetch_all(
            """
            SELECT id, destination_address, next_hop, metric, interface
            FROM Route
            WHERE router_id = %s
            ORDER BY id
            """,
            (router_id,),
        )
        return [
            Route(
                route_id=row["id"],
                destination_address=row["destination_address"],
                next_hop=row["next_hop"],
                metric=row["metric"],
                interface=row["interface"],
            )
            for row in rows
        ]

    def update(self, route_id: int, route: Route) -> None:
        query = """
            UPDATE Route
            SET destination_address = %s, next_hop = %s, metric = %s, interface = %s
            WHERE id = %s
        """
        self.db.execute_query(
            query,
            (route.destination_address, route.next_hop, route.metric, route.interface, route_id),
        )

    def delete(self, route_id: int) -> None:
        self.db.execute_query("DELETE FROM Route WHERE id = %s", (route_id,))


class RouterDAO:
    def __init__(self, db_connector):
        self.db = db_connector
        self.device_dao = NetworkDeviceDAO(db_connector)
        self.route_dao = RouteDAO(db_connector)

    def create(self, router: Router) -> int:
        device_id = self.device_dao.create_base_device(router)
        self.db.execute_query(
            "INSERT INTO Router (id, routing_protocol) VALUES (%s, %s)",
            (device_id, router.routing_protocol),
        )
        for route in router.routing_table:
            self.route_dao.create(device_id, route)
        return device_id

    def get_all(self) -> list[Router]:
        query = """
            SELECT nd.id, nd.device_name, nd.manufacturer, nd.model, nd.company_id, r.routing_protocol
            FROM Router r
            INNER JOIN NetworkDevice nd ON nd.id = r.id
            ORDER BY nd.id
        """
        rows = self.db.fetch_all(query)
        routers = []
        for row in rows:
            router = Router(
                device_id=row["id"],
                device_name=row["device_name"],
                manufacturer=row["manufacturer"],
                model=row["model"],
                company_id=row["company_id"],
                routing_protocol=row["routing_protocol"],
            )
            router.add_routes(self.route_dao.get_by_router(row["id"]))
            routers.append(router)
        return routers

    def update(self, router_id: int, router: Router) -> None:
        self.device_dao.update_base_device(router_id, router)
        self.db.execute_query(
            "UPDATE Router SET routing_protocol = %s WHERE id = %s",
            (router.routing_protocol, router_id),
        )

    def delete(self, router_id: int) -> None:
        self.device_dao.delete_base_device(router_id)


class ModemDAO:
    def __init__(self, db_connector):
        self.db = db_connector
        self.device_dao = NetworkDeviceDAO(db_connector)

    def create(self, modem: Modem) -> int:
        device_id = self.device_dao.create_base_device(modem)
        query = """
            INSERT INTO Modem (id, modulation_type, downstream_speed_mbps, upstream_speed_mbps)
            VALUES (%s, %s, %s, %s)
        """
        self.db.execute_query(
            query,
            (device_id, modem.modulation_type, modem.downstream_speed_mbps, modem.upstream_speed_mbps),
        )
        return device_id

    def get_all(self) -> list[Modem]:
        query = """
            SELECT nd.id, nd.device_name, nd.manufacturer, nd.model, nd.company_id,
                   m.modulation_type, m.downstream_speed_mbps, m.upstream_speed_mbps
            FROM Modem m
            INNER JOIN NetworkDevice nd ON nd.id = m.id
            ORDER BY nd.id
        """
        rows = self.db.fetch_all(query)
        return [
            Modem(
                device_id=row["id"],
                device_name=row["device_name"],
                manufacturer=row["manufacturer"],
                model=row["model"],
                company_id=row["company_id"],
                modulation_type=row["modulation_type"],
                downstream_speed_mbps=row["downstream_speed_mbps"],
                upstream_speed_mbps=row["upstream_speed_mbps"],
            )
            for row in rows
        ]

    def update(self, modem_id: int, modem: Modem) -> None:
        self.device_dao.update_base_device(modem_id, modem)
        query = """
            UPDATE Modem
            SET modulation_type = %s, downstream_speed_mbps = %s, upstream_speed_mbps = %s
            WHERE id = %s
        """
        self.db.execute_query(
            query,
            (modem.modulation_type, modem.downstream_speed_mbps, modem.upstream_speed_mbps, modem_id),
        )

    def delete(self, modem_id: int) -> None:
        self.device_dao.delete_base_device(modem_id)


class SwitchDAO:
    def __init__(self, db_connector):
        self.db = db_connector
        self.device_dao = NetworkDeviceDAO(db_connector)

    def create(self, switch: Switch) -> int:
        device_id = self.device_dao.create_base_device(switch)
        query = """
            INSERT INTO SwitchDevice (id, number_of_ports, managed, switching_capacity_gbps)
            VALUES (%s, %s, %s, %s)
        """
        self.db.execute_query(
            query,
            (device_id, switch.number_of_ports, switch.managed, switch.switching_capacity_gbps),
        )
        return device_id

    def get_all(self) -> list[Switch]:
        query = """
            SELECT nd.id, nd.device_name, nd.manufacturer, nd.model, nd.company_id,
                   s.number_of_ports, s.managed, s.switching_capacity_gbps
            FROM SwitchDevice s
            INNER JOIN NetworkDevice nd ON nd.id = s.id
            ORDER BY nd.id
        """
        rows = self.db.fetch_all(query)
        return [
            Switch(
                device_id=row["id"],
                device_name=row["device_name"],
                manufacturer=row["manufacturer"],
                model=row["model"],
                company_id=row["company_id"],
                number_of_ports=row["number_of_ports"],
                managed=bool(row["managed"]),
                switching_capacity_gbps=float(row["switching_capacity_gbps"]),
            )
            for row in rows
        ]

    def update(self, switch_id: int, switch: Switch) -> None:
        self.device_dao.update_base_device(switch_id, switch)
        query = """
            UPDATE SwitchDevice
            SET number_of_ports = %s, managed = %s, switching_capacity_gbps = %s
            WHERE id = %s
        """
        self.db.execute_query(
            query,
            (switch.number_of_ports, switch.managed, switch.switching_capacity_gbps, switch_id),
        )

    def delete(self, switch_id: int) -> None:
        self.device_dao.delete_base_device(switch_id)


class QueryDAO:
    def __init__(self, db_connector):
        self.db = db_connector

    def get_all_devices_with_company_names(self) -> list[dict[str, Any]]:
        query = """
            SELECT nd.id, nd.device_name, nd.device_type, nd.manufacturer, nd.model, c.name AS company_name
            FROM NetworkDevice nd
            INNER JOIN Company c ON nd.company_id = c.id
            ORDER BY nd.id
        """
        return self.db.fetch_all(query)

    def get_routes_with_router_details(self) -> list[dict[str, Any]]:
        query = """
            SELECT r.id AS route_id, nd.device_name, nd.model, rt.routing_protocol,
                   r.destination_address, r.next_hop, r.metric, r.interface
            FROM Route r
            INNER JOIN Router rt ON r.router_id = rt.id
            INNER JOIN NetworkDevice nd ON rt.id = nd.id
            ORDER BY r.id
        """
        return self.db.fetch_all(query)

    def get_companies_without_routers(self) -> list[dict[str, Any]]:
        query = """
            SELECT c.id, c.name, c.city
            FROM Company c
            LEFT JOIN NetworkDevice nd ON c.id = nd.company_id AND nd.device_type = 'router'
            WHERE nd.id IS NULL
            ORDER BY c.id
        """
        return self.db.fetch_all(query)

    def count_devices_per_company(self) -> list[dict[str, Any]]:
        query = """
            SELECT c.id, c.name, COUNT(nd.id) AS total_devices
            FROM Company c
            LEFT JOIN NetworkDevice nd ON c.id = nd.company_id
            GROUP BY c.id, c.name
            ORDER BY total_devices DESC, c.id
        """
        return self.db.fetch_all(query)

    def find_most_used_interface(self) -> list[dict[str, Any]]:
        query = """
            SELECT interface, COUNT(*) AS usage_count
            FROM Route
            GROUP BY interface
            ORDER BY usage_count DESC, interface ASC
        """
        return self.db.fetch_all(query)

    def mean_hops_used_in_each_router(self) -> list[dict[str, Any]]:
        query = """
            SELECT nd.id AS router_id, nd.device_name, AVG(r.metric) AS average_hops
            FROM Router rt
            INNER JOIN NetworkDevice nd ON rt.id = nd.id
            LEFT JOIN Route r ON rt.id = r.router_id
            GROUP BY nd.id, nd.device_name
            ORDER BY nd.id
        """
        return self.db.fetch_all(query)

    def get_devices_by_type_and_company(self) -> list[dict[str, Any]]:
        query = """
            SELECT c.name AS company_name, nd.device_type, COUNT(nd.id) AS total
            FROM Company c
            LEFT JOIN NetworkDevice nd ON c.id = nd.company_id
            GROUP BY c.name, nd.device_type
            ORDER BY c.name, nd.device_type
        """
        return self.db.fetch_all(query)

    def get_highest_metric_route_per_router(self) -> list[dict[str, Any]]:
        query = """
            SELECT nd.device_name, MAX(r.metric) AS max_metric
            FROM Router rt
            INNER JOIN NetworkDevice nd ON rt.id = nd.id
            LEFT JOIN Route r ON rt.id = r.router_id
            GROUP BY nd.device_name
            ORDER BY max_metric DESC
        """
        return self.db.fetch_all(query)
