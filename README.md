# Network Devices Management System

A console-based Python application for managing network infrastructure data using **MySQL/MariaDB**.  
The system supports CRUD operations for **Company**, **Router**, **Modem**, **Switch**, and **Route**, and includes analytical SQL queries to inspect the network environment.

## Overview

This project models a small network inventory and routing management system with an object-oriented design in Python and a relational database in MySQL/MariaDB.

### Main capabilities

- Manage companies that own network devices
- Manage specialized network devices:
  - Routers
  - Modems
  - Switches
- Manage routing entries associated with routers
- Run analytical queries directly from the Python application
- Work with a normalized relational database using foreign keys

## Tech stack

- **Language:** Python 3
- **Database:** MySQL / MariaDB
- **Environment:** XAMPP
- **Connector:** `mysql-connector-python`


## Relationships

- One **Company** can own many **NetworkDevice** records
- One **NetworkDevice** can specialize into:
  - one **Router**
  - one **Modem**
  - one **SwitchDevice**
- One **Router** can have many **Route** records

## UML class diagram

```mermaid
classDiagram
    class Company {
        +int id
        +string name
        +string city
    }

    class NetworkDevice {
        +int id
        +string device_name
        +string manufacturer
        +string model
        +int company_id
        +string device_type
    }

    class Router {
        +string routing_protocol
    }

    class Modem {
        +string modulation_type
        +int downstream_speed_mbps
        +int upstream_speed_mbps
    }

    class Switch {
        +int number_of_ports
        +bool managed
        +float switching_capacity_gbps
    }

    class Route {
        +int id
        +int router_id
        +string destination_address
        +string next_hop
        +int metric
        +string interface
    }

    NetworkDevice <|-- Router
    NetworkDevice <|-- Modem
    NetworkDevice <|-- Switch

    Company "1" --> "0..*" NetworkDevice : owns
    Router "1" --> "0..*" Route : has
```

## Database diagram

```mermaid
erDiagram
    Company {
        INT id PK
        VARCHAR name
        VARCHAR city
    }

    NetworkDevice {
        INT id PK
        VARCHAR device_name
        VARCHAR manufacturer
        VARCHAR model
        INT company_id FK
        VARCHAR device_type
    }

    Router {
        INT id PK, FK
        VARCHAR routing_protocol
    }

    Modem {
        INT id PK, FK
        VARCHAR modulation_type
        INT downstream_speed_mbps
        INT upstream_speed_mbps
    }

    SwitchDevice {
        INT id PK, FK
        INT number_of_ports
        BOOLEAN managed
        DECIMAL switching_capacity_gbps
    }

    Route {
        INT id PK
        INT router_id FK
        VARCHAR destination_address
        VARCHAR next_hop
        INT metric
        VARCHAR interface
    }

    Company ||--o{ NetworkDevice : owns
    NetworkDevice ||--|| Router : specializes
    NetworkDevice ||--|| Modem : specializes
    NetworkDevice ||--|| SwitchDevice : specializes
    Router ||--o{ Route : has
```

## Screenshots
assets/screenshots/menu.png
### Menu
![Application Menu](assets/screenshots/menu.png)

## Queries
![Application Queries](assets/screenshots/queries.png)

## Tablas y dispositivos 
![Application Tablas](assets/screenshots/tablas_e_instancias.png)

### Menu and Companies


## Authors

- `Aurelio Muñoz`
- `Victor Chavarro`
