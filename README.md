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

> Recommended folder in your GitHub repository: `docs/images/`

### Application screenshot

![Application Menu](docs/images/app-menu.png)

### Database structure screenshot

![Database Structure](docs/images/database-structure.png)

### UML / database diagram screenshot

![UML Diagram](docs/images/uml-diagram.png)

## Example SQL relationships

The system uses foreign keys to preserve integrity across the tables:

- `NetworkDevice.company_id -> Company.id`
- `Router.id -> NetworkDevice.id`
- `Modem.id -> NetworkDevice.id`
- `SwitchDevice.id -> NetworkDevice.id`
- `Route.router_id -> Router.id`

## How to run the project

### 1. Start MySQL from XAMPP
Open XAMPP and start the MySQL service.

### 2. Create the database manually
Use the MySQL console from XAMPP and run your SQL script to create:

- `Company`
- `NetworkDevice`
- `Router`
- `Modem`
- `SwitchDevice`
- `Route`

### 3. Install dependency

```bash
pip install mysql-connector-python
```

### 4. Run the application

```bash
python Main.py
```

## Main menu modules

The console application is organized into these sections:

- Company
- Router
- Modem
- Switch
- Route
- Queries

## Sample analytical queries supported

- Devices with their company
- Route details by router
- Companies without routers
- Device count by company
- Most used interface
- Average route metric by router
- Device count by company and device type
- Maximum route metric per router

## Notes

- The database creation is performed manually in MySQL/MariaDB through XAMPP
- The Python application focuses on connection handling, CRUD operations, and queries
- The design follows an object-oriented model plus a DAO-based persistence layer

## Author

Add your name here.
