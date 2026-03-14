from __future__ import annotations

from database.Database_connection import DatabaseConnector
from dao.Network_device_dao import CompanyDAO, ModemDAO, QueryDAO, RouteDAO, RouterDAO, SwitchDAO
from model.Network_devices_model import Company, Modem, Route, Router, Switch


def print_separator() -> None:
    print("\n" + "=" * 72)


class App:
    def __init__(self):
        self.db = DatabaseConnector(host="localhost", user="root", password="", database="myNetworkdb", port=3306)
        self.company_dao = CompanyDAO(self.db)
        self.router_dao = RouterDAO(self.db)
        self.modem_dao = ModemDAO(self.db)
        self.switch_dao = SwitchDAO(self.db)
        self.route_dao = RouteDAO(self.db)
        self.query_dao = QueryDAO(self.db)

    def start(self) -> None:
        self.db.connect()
        try:
            self.menu()
        finally:
            self.db.disconnect()

    def menu(self) -> None:
        while True:
            print_separator()
            print("NETWORK DEVICE MANAGER")
            print("1. Company")
            print("2. Router")
            print("3. Modem")
            print("4. Switch")
            print("5. Route")
            print("6. Consultas")
            print("0. Exit")
            option = input("Choose an option: ").strip()

            if option == "1":
                self.company_menu()
            elif option == "2":
                self.router_menu()
            elif option == "3":
                self.modem_menu()
            elif option == "4":
                self.switch_menu()
            elif option == "5":
                self.route_menu()
            elif option == "6":
                self.run_analytical_queries()
            elif option == "0":
                print("Goodbye.")
                break
            else:
                print("Invalid option.")

    def company_menu(self) -> None:
        print_separator()
        print("COMPANY")
        print("1. Create")
        print("2. List")
        print("3. Update")
        print("4. Delete")
        option = input("Choose an option: ").strip()
        actions = {"1": self.create_company, "2": self.list_companies, "3": self.update_company, "4": self.delete_company}
        self.execute_action(actions, option)

    def router_menu(self) -> None:
        print_separator()
        print("ROUTER")
        print("1. Create")
        print("2. List")
        print("3. Update")
        print("4. Delete")
        option = input("Choose an option: ").strip()
        actions = {"1": self.create_router, "2": self.list_routers, "3": self.update_router, "4": self.delete_router}
        self.execute_action(actions, option)

    def modem_menu(self) -> None:
        print_separator()
        print("MODEM")
        print("1. Create")
        print("2. List")
        print("3. Update")
        print("4. Delete")
        option = input("Choose an option: ").strip()
        actions = {"1": self.create_modem, "2": self.list_modems, "3": self.update_modem, "4": self.delete_modem}
        self.execute_action(actions, option)

    def switch_menu(self) -> None:
        print_separator()
        print("SWITCH")
        print("1. Create")
        print("2. List")
        print("3. Update")
        print("4. Delete")
        option = input("Choose an option: ").strip()
        actions = {"1": self.create_switch, "2": self.list_switches, "3": self.update_switch, "4": self.delete_switch}
        self.execute_action(actions, option)

    def route_menu(self) -> None:
        print_separator()
        print("ROUTE")
        print("1. Create")
        print("2. List")
        print("3. Update")
        print("4. Delete")
        option = input("Choose an option: ").strip()
        actions = {"1": self.create_route, "2": self.list_routes, "3": self.update_route, "4": self.delete_route}
        self.execute_action(actions, option)

    def execute_action(self, actions: dict[str, callable], option: str) -> None:
        action = actions.get(option)
        if not action:
            print("Invalid option.")
            return
        try:
            action()
        except Exception as error:
            print(f"Operation failed: {error}")

    def create_company(self) -> None:
        company_id = self.company_dao.create(Company(name=input("Name: ").strip(), city=input("City: ").strip()))
        print(f"Company created with ID {company_id}.")

    def list_companies(self) -> None:
        companies = self.company_dao.get_all()
        if not companies:
            print("No companies found.")
            return
        for company in companies:
            print(company.print_company())

    def update_company(self) -> None:
        company_id = int(input("Company ID: ").strip())
        self.company_dao.update(company_id, input("New name: ").strip(), input("New city: ").strip())
        print("Company updated.")

    def delete_company(self) -> None:
        self.company_dao.delete(int(input("Company ID: ").strip()))
        print("Company deleted.")

    def create_router(self) -> None:
        router = Router(
            device_name=input("Name: ").strip(),
            manufacturer=input("Manufacturer: ").strip(),
            model=input("Model: ").strip(),
            company_id=int(input("Company ID: ").strip()),
            routing_protocol=input("Routing protocol: ").strip(),
        )
        router_id = self.router_dao.create(router)
        print(f"Router created with ID {router_id}.")

    def list_routers(self) -> None:
        routers = self.router_dao.get_all()
        if not routers:
            print("No routers found.")
            return
        for router in routers:
            print(router.detailed_summary())
            print(router.print_routing_table())

    def update_router(self) -> None:
        router_id = int(input("Router ID: ").strip())
        router = Router(
            device_name=input("New name: ").strip(),
            manufacturer=input("New manufacturer: ").strip(),
            model=input("New model: ").strip(),
            company_id=int(input("New company ID: ").strip()),
            routing_protocol=input("New routing protocol: ").strip(),
        )
        self.router_dao.update(router_id, router)
        print("Router updated.")

    def delete_router(self) -> None:
        self.router_dao.delete(int(input("Router ID: ").strip()))
        print("Router deleted.")

    def create_modem(self) -> None:
        modem = Modem(
            device_name=input("Name: ").strip(),
            manufacturer=input("Manufacturer: ").strip(),
            model=input("Model: ").strip(),
            company_id=int(input("Company ID: ").strip()),
            modulation_type=input("Modulation type: ").strip(),
            downstream_speed_mbps=int(input("Downstream Mbps: ").strip()),
            upstream_speed_mbps=int(input("Upstream Mbps: ").strip()),
        )
        modem_id = self.modem_dao.create(modem)
        print(f"Modem created with ID {modem_id}.")

    def list_modems(self) -> None:
        modems = self.modem_dao.get_all()
        if not modems:
            print("No modems found.")
            return
        for modem in modems:
            print(modem.detailed_summary())

    def update_modem(self) -> None:
        modem_id = int(input("Modem ID: ").strip())
        modem = Modem(
            device_name=input("New name: ").strip(),
            manufacturer=input("New manufacturer: ").strip(),
            model=input("New model: ").strip(),
            company_id=int(input("New company ID: ").strip()),
            modulation_type=input("New modulation type: ").strip(),
            downstream_speed_mbps=int(input("New downstream Mbps: ").strip()),
            upstream_speed_mbps=int(input("New upstream Mbps: ").strip()),
        )
        self.modem_dao.update(modem_id, modem)
        print("Modem updated.")

    def delete_modem(self) -> None:
        self.modem_dao.delete(int(input("Modem ID: ").strip()))
        print("Modem deleted.")

    def create_switch(self) -> None:
        switch = Switch(
            device_name=input("Name: ").strip(),
            manufacturer=input("Manufacturer: ").strip(),
            model=input("Model: ").strip(),
            company_id=int(input("Company ID: ").strip()),
            number_of_ports=int(input("Ports: ").strip()),
            managed=input("Managed? (y/n): ").strip().lower() == "y",
            switching_capacity_gbps=float(input("Capacity Gbps: ").strip()),
        )
        switch_id = self.switch_dao.create(switch)
        print(f"Switch created with ID {switch_id}.")

    def list_switches(self) -> None:
        switches = self.switch_dao.get_all()
        if not switches:
            print("No switches found.")
            return
        for switch in switches:
            print(switch.detailed_summary())

    def update_switch(self) -> None:
        switch_id = int(input("Switch ID: ").strip())
        switch = Switch(
            device_name=input("New name: ").strip(),
            manufacturer=input("New manufacturer: ").strip(),
            model=input("New model: ").strip(),
            company_id=int(input("New company ID: ").strip()),
            number_of_ports=int(input("New ports: ").strip()),
            managed=input("Managed? (y/n): ").strip().lower() == "y",
            switching_capacity_gbps=float(input("New capacity Gbps: ").strip()),
        )
        self.switch_dao.update(switch_id, switch)
        print("Switch updated.")

    def delete_switch(self) -> None:
        self.switch_dao.delete(int(input("Switch ID: ").strip()))
        print("Switch deleted.")

    def create_route(self) -> None:
        router_id = int(input("Router ID: ").strip())
        route = Route(
            destination_address=input("Destination: ").strip(),
            next_hop=input("Next hop: ").strip(),
            metric=int(input("Metric: ").strip()),
            interface=input("Interface: ").strip(),
        )
        route_id = self.route_dao.create(router_id, route)
        print(f"Route created with ID {route_id}.")

    def list_routes(self) -> None:
        routes = self.route_dao.get_all()
        if not routes:
            print("No routes found.")
            return
        for route in routes:
            print(route.display_info())

    def update_route(self) -> None:
        route_id = int(input("Route ID: ").strip())
        route = Route(
            destination_address=input("New destination: ").strip(),
            next_hop=input("New next hop: ").strip(),
            metric=int(input("New metric: ").strip()),
            interface=input("New interface: ").strip(),
        )
        self.route_dao.update(route_id, route)
        print("Route updated.")

    def delete_route(self) -> None:
        self.route_dao.delete(int(input("Route ID: ").strip()))
        print("Route deleted.")

    def run_analytical_queries(self) -> None:
        consultas = [
            ("A. All devices with company", self.query_dao.get_all_devices_with_company_names),
            ("B. Routes with router details", self.query_dao.get_routes_with_router_details),
            ("C. Companies without routers", self.query_dao.get_companies_without_routers),
            ("D. Devices per company", self.query_dao.count_devices_per_company),
            ("E. Most used interface", self.query_dao.find_most_used_interface),
            ("F. Mean hops by router", self.query_dao.mean_hops_used_in_each_router),
            ("G. Devices by type and company", self.query_dao.get_devices_by_type_and_company),
            ("H. Highest metric route per router", self.query_dao.get_highest_metric_route_per_router),
        ]
        for titulo, funcion in consultas:
            print_separator()
            print(titulo)
            for row in funcion():
                print(row)


if __name__ == "__main__":
    App().start()
