# BP Tech Inventory Management System

A web-based inventory management system and customer-facing product catalogue for **BP Tech**, a computer shop specialising in new and used PC components, computer accessories, and custom PC building services.

## 1. Project Overview

BP Tech currently manages its product inventory using Google Docs. While this provides a simple way to record product information, manually maintaining stock quantities and product details can become inconvenient as the business grows.

This project aims to develop a centralised inventory management system that allows BP Tech to manage its products and stock records more efficiently while providing customers with an accessible online product catalogue.

The system will synchronise product information between the internal inventory database and the public-facing website, allowing customers to view updated product listings, prices, conditions, and availability.

Customers will also be provided with a direct WhatsApp contact link for further enquiries, custom PC building requests, and booking arrangements.

## 2. Project Objectives

- Replace manual Google Docs inventory records with a structured relational database.
- Allow administrators to add, edit, delete, and manage product listings.
- Maintain accurate stock quantities and product availability.
- Provide customers with an online catalogue of available PC components and accessories.
- Distinguish between new and used products.
- Synchronise product information between the database and customer-facing website.
- Provide direct communication with BP Tech through WhatsApp.

## 3. Main System Modules

### 3.1 Inventory Management Module
- Add new products and product categories.
- Update product descriptions, prices, and stock quantities.
- Manage new and used product conditions.
- Monitor available stock.
- Record stock additions, removals, and adjustments.
- Identify products with low stock levels.

### 3.2 Customer Product Catalogue Module
- Display products retrieved from the database.
- Show product images, names, descriptions, prices, and conditions.
- Display current stock availability.
- Allow customers to browse and filter products by category.
- Hide or label unavailable and discontinued products appropriately.

### 3.3 WhatsApp Enquiry Module
- Provide a WhatsApp contact link at the bottom of the customer-facing website.
- Allow customers to enquire about products, availability, prices, and custom PC building services.
- Open a direct WhatsApp conversation with BP Tech.
- Optionally include a pre-filled message containing the selected product name.

### 3.4 Backend and Database Module
- Handle requests between the frontend and database.
- Provide REST API endpoints for product and inventory operations.
- Validate incoming data.
- Execute database queries and transactions.
- Ensure stock updates are reflected in the customer-facing catalogue.

### 3.5 Authentication and Security Module
- Provide administrator login.
- Restrict inventory management operations to authorised administrators.
- Securely handle passwords using hashing.
- Validate incoming requests and prevent unauthorised modifications.

## 4. Proposed Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| Frontend | HTML | Website structure |
| Styling | CSS | Website design and layout |
| Client-side | JavaScript | Fetching and displaying API data |
| Backend | Python + FastAPI | Business logic and REST API |
| Database | PostgreSQL | Relational data storage |
| ORM | SQLAlchemy | Database interaction |
| API Testing | Postman / Swagger UI | Testing API endpoints |
| Version Control | Git + GitHub | Collaboration and source control |

**Data synchronisation:** The frontend will retrieve product information through API requests. For the initial implementation, JavaScript Fetch API can retrieve updated information whenever the catalogue loads or refreshes. WebSocket communication may be implemented as an additional feature for real-time updates without manual refreshing.

## 5. Database Design – Five Inventory Entities and Admin Authentication

The database uses five core inventory entities to organise product information, suppliers, inventory records, and stock movements. It also has an `Admin` entity for administrator authentication.

### Entity 1: Category

Stores the categories used to organise products.

| Attribute | Data Type | Description |
|---|---|---|
| category_id (PK) | SERIAL | Unique category identifier |
| category_name | VARCHAR(100) | Category name |
| description | TEXT | Category description |

Examples:
- GPU
- CPU
- Motherboard
- RAM
- SSD
- HDD
- PSU
- Case
- CPU Cooler
- Monitor
- Fan
- Keyboard
- Mouse
- Headset
- Speaker
- Controller
- Accessories

### Entity 2: Supplier

Stores information about suppliers providing products to BP Tech.

| Attribute | Data Type | Description |
|---|---|---|
| supplier_id (PK) | SERIAL | Unique supplier identifier |
| supplier_name | VARCHAR(150) | Supplier or company name |
| contact_number | VARCHAR(20), nullable | Supplier contact number |
| email | VARCHAR(150), nullable | Supplier email |
| address | TEXT, nullable | Supplier address |

### Entity 3: Product

Stores the details of individual products sold by BP Tech.

| Attribute | Data Type | Description |
|---|---|---|
| product_id (PK) | SERIAL | Unique product identifier |
| category_id (FK) | INTEGER | References Category |
| supplier_id (FK) | INTEGER, nullable | References Supplier; optional primary supplier |
| product_name | VARCHAR(150) | Product name |
| sku | VARCHAR(50), unique | Unique stock-keeping unit |
| description | TEXT | Product specifications and details |
| condition | VARCHAR(20) | New or Used |
| selling_price | DECIMAL(10,2) | Product selling price |
| image_url | TEXT | Product image location |
| product_status | VARCHAR(20) | Active or Discontinued |

Examples:
- AMD Ryzen 5 5600 (New)
- RTX 3060 12GB (Used)
- Kingston 16GB DDR4 RAM (New)

### Entity 4: Inventory

Stores the current stock information for each product.

| Attribute | Data Type | Description |
|---|---|---|
| inventory_id (PK) | SERIAL | Unique inventory identifier |
| product_id (FK) | INTEGER | References Product |
| quantity_available | INTEGER | Current stock quantity |
| reorder_level | INTEGER | Minimum desired stock quantity |
| last_updated | TIMESTAMP | Last inventory update |

Each product will have one inventory record. This separates product descriptions and pricing from stock management.

### Entity 5: Stock_Movement

Records changes made to product inventory quantities.

| Attribute | Data Type | Description |
|---|---|---|
| movement_id (PK) | SERIAL | Unique movement identifier |
| product_id (FK) | INTEGER | References Product |
| movement_type | VARCHAR(20) | IN, OUT or ADJUSTMENT |
| quantity | INTEGER | Quantity involved |
| movement_date | TIMESTAMP | Date and time of movement |
| remarks | TEXT | Reason for stock movement |

Examples:
- IN: 10 units received from supplier.
- OUT: 2 units sold to customers.
- ADJUSTMENT: Stock corrected after a physical inventory check.

Stock movements provide a history of inventory changes instead of simply overwriting stock quantities.

### Additional Entity: Admin (Authentication)

Stores administrator accounts used to access protected inventory-management operations.

| Attribute | Data Type | Description |
|---|---|---|
| admin_id (PK) | SERIAL | Unique administrator identifier |
| username | VARCHAR(50), unique | Administrator login name |
| hashed_password | VARCHAR(255) | Hashed administrator password |
| email | VARCHAR(150), unique | Administrator email address |
| created_at | TIMESTAMP | Account creation time |

## 6. Entity Relationships and ERD Planning

The following relationships should be used when creating the Entity Relationship Diagram (ERD).

| Relationship | Cardinality | Explanation |
|---|---|---|
| Category → Product | 1:M | One category can contain multiple products, but each product belongs to one category. |
| Supplier → Product | 1:M | One supplier can supply multiple products; a product may have one primary supplier or none. |
| Product → Inventory | 1:1 | Each product has one inventory record, and each inventory record belongs to one product. |
| Product → Stock_Movement | 1:M | One product can have multiple stock movement records, but each movement belongs to one product. |

### ERD Relationship Overview

Category (1) ───── (M) Product

Supplier (1) ───── (M) Product

Product (1) ───── (1) Inventory

Product (1) ───── (M) Stock_Movement

### Important Database Constraints

- Every entity must have a primary key.
- Foreign keys must reference existing records.
- Product SKU identifiers are unique.
- Product prices cannot be negative.
- Inventory quantities cannot be negative.
- Stock movement quantities must be positive.
- Product condition must be restricted to New or Used.
- Inventory records should be created automatically when a new product is registered.
- The current model cascades product deletion to its inventory and stock-movement records. If movement history must be retained for auditing, restrict product deletion and use the discontinued status instead.

**Design consideration:** This model assumes each product has one primary supplier. If BP Tech needs to record multiple suppliers for the same product, a separate junction entity can be introduced in a future version.

## 7. Proposed System Workflow

### Administrator Workflow

1. Administrator logs into the inventory management system.
2. Administrator accesses the inventory dashboard.
3. Administrator adds a new product or selects an existing product.
4. Product details, pricing, category, and condition are entered or updated.
5. Stock quantities are updated.
6. The system records the stock movement.
7. The database stores the latest product and inventory information.
8. The customer-facing catalogue retrieves the updated information through the API.

### Customer Workflow

1. Customer visits the BP Tech website.
2. Customer browses available PC components and accessories.
3. Customer views product details, conditions, prices, and stock availability.
4. Customer selects a product they are interested in.
5. Customer clicks the WhatsApp enquiry link.
6. WhatsApp opens a conversation with BP Tech.
7. Customer discusses availability, purchases, or custom PC building arrangements directly with the business.

## 8. Proposed API Endpoints

The backend will expose REST API endpoints to allow the frontend to communicate with the database.

| HTTP Method | Endpoint | Function |
|---|---|---|
| GET | `/api/products` | Retrieve all active products |
| GET | `/api/products/{id}` | Retrieve a specific product |
| POST | `/api/products` | Add a new product |
| PUT | `/api/products/{id}` | Update product details |
| DELETE | `/api/products/{id}` | Remove or discontinue a product |
| GET | `/api/categories` | Retrieve product categories |
| GET | `/api/inventory` | Retrieve inventory records |
| PUT | `/api/inventory/{id}` | Update inventory information |
| GET | `/api/stock-movements` | Retrieve stock movement history |
| POST | `/api/stock-movements` | Record a stock movement |

Administrator-only endpoints must require authentication.

## 9. Team Division and Responsibilities

The project will be developed by three team members, with each member responsible for a different part of the system.

### Member 1 – Backend and Database Developer

**Main responsibility:** Backend development and database implementation.

Tasks:
- Design and implement the PostgreSQL database.
- Create all five database entities and their relationships.
- Implement SQLAlchemy models.
- Configure database connections.
- Develop REST API endpoints using Python and FastAPI.
- Implement product and inventory management logic.
- Implement stock movement transactions.
- Develop administrator authentication.
- Test API functionality using Postman or Swagger UI.

Deliverables:
- PostgreSQL database.
- Database models and relationships.
- FastAPI backend.
- Functional API endpoints.

### Member 2 – Frontend Developer

**Main responsibility:** Website structure, layout, and visual design.

Tasks:
- Design the customer-facing product catalogue.
- Develop the administrator dashboard layout.
- Create product cards and product detail sections.
- Design inventory management interfaces.
- Implement responsive layouts using HTML and CSS.
- Create the WhatsApp contact and enquiry section.
- Ensure the website is usable on desktop and mobile devices.

Deliverables:
- Customer-facing website interface.
- Administrator dashboard interface.
- HTML and CSS files.
- Product display components.

### Member 3 – JavaScript and Frontend Integration Developer

**Main responsibility:** Client-side functionality and API integration.

Tasks:
- Implement JavaScript Fetch API requests.
- Retrieve product information from FastAPI endpoints.
- Dynamically render products in the customer catalogue.
- Implement category filtering, search, and condition toggles.
- Handle administrator authentication, login tokens, and session persistence.
- Manage admin dashboard inventory operations and stock movement form submissions.
- Generate pre-filled WhatsApp enquiry links with product details and custom PC building requests.

Deliverables:
- JavaScript API service layer (`frontend/js/api.js`).
- Dynamic catalogue rendering and filter module (`frontend/js/catalogue.js`).
- Administrator inventory management scripts (`frontend/js/admin.js`).
- Authentication and session handling (`frontend/js/auth.js`).
- WhatsApp link generator (`frontend/js/whatsapp.js`).

## 10. Project Directory Structure & Team File Ownership

To make collaboration smooth among the 3 team members, the repository is structured with clear file ownership:

```
database/
├── README.md                                  # [Shared] Main project documentation
├── TEAM_ROLES.md                              # [Shared] Detailed role breakdown & guide
├── index.html                                 # [Member 2] Root entrypoint redirecting to frontend/
├── .gitignore                                 # [Shared] Git ignore rules
│
├── backend/                                   # [MEMBER 1: Backend & Database Developer]
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                            # FastAPI application entry point
│   │   ├── config.py                          # Environment and database settings
│   │   ├── database.py                        # SQLAlchemy connection & sessionmaker
│   │   ├── auth_utils.py                      # Bcrypt password hashing & JWT tokens
│   │   ├── seed_data.py                       # Automated database seeder script
│   │   ├── models/                            # SQLAlchemy ORM models (5 entities + admin)
│   │   │   ├── __init__.py
│   │   │   ├── category.py                    # Entity 1: Category
│   │   │   ├── supplier.py                    # Entity 2: Supplier
│   │   │   ├── product.py                     # Entity 3: Product
│   │   │   ├── inventory.py                   # Entity 4: Inventory (1:1 with Product)
│   │   │   ├── stock_movement.py              # Entity 5: Stock_Movement (1:M with Product)
│   │   │   └── admin.py                       # Administrator entity
│   │   ├── schemas/                           # Pydantic validation schemas
│   │   │   ├── __init__.py
│   │   │   ├── category.py
│   │   │   ├── supplier.py
│   │   │   ├── product.py
│   │   │   ├── inventory.py
│   │   │   ├── stock_movement.py
│   │   │   └── auth.py
│   │   └── routers/                           # REST API endpoint routers
│   │       ├── __init__.py
│   │       ├── auth.py                        # /api/auth endpoints
│   │       ├── categories.py                  # /api/categories endpoints
│   │       ├── suppliers.py                   # /api/suppliers endpoints
│   │       ├── products.py                    # /api/products endpoints
│   │       ├── inventory.py                   # /api/inventory endpoints
│   │       └── stock_movements.py             # /api/stock-movements endpoints
│   ├── sql/                                   # PostgreSQL DDL and seeds
│   │   ├── schema.sql                         # PostgreSQL table creation script
│   │   └── seed.sql                           # PostgreSQL sample insert statements
│   ├── requirements.txt                       # Python dependencies
│   ├── .env.example                           # Environment configuration template
│   ├── main.py                                # Convenience proxy
│   ├── config.py                              # Convenience proxy
│   └── database.py                            # Convenience proxy
│
└── frontend/                                  # [MEMBERS 2 & 3: Frontend Team]
    ├── index.html                             # [Member 2] Customer catalogue & WhatsApp section
    ├── product-detail.html                    # [Member 2] Product detail page
    ├── admin-login.html                       # [Member 2] Administrator login page
    ├── admin-dashboard.html                   # [Member 2] Admin inventory & movements dashboard
    ├── css/                                   # [Member 2: Frontend Developer - Styles]
    │   ├── styles.css                         # Customer catalogue styles (dark tech theme)
    │   ├── admin.css                          # Admin dashboard styles & modals
    │   └── responsive.css                     # Responsive mobile & tablet styles
    └── js/                                    # [Member 3: JS & Frontend Integration Developer]
        ├── config.js                          # API base URL & WhatsApp settings
        ├── api.js                             # Fetch API client helper
        ├── auth.js                            # Admin token management & route protection
        ├── catalogue.js                       # Dynamic catalogue rendering & filtering
        ├── admin.js                           # Admin inventory CRUD & stock movements
        └── whatsapp.js                        # WhatsApp enquiry link generator
```

## 11. Quick Start Guide

### 1. Backend Setup (Member 1)
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate       # On Windows (.venv/bin/activate on macOS/Linux)
pip install -r requirements.txt
python -m app.seed_data      # Seeds tables and sample BP Tech components
uvicorn main:app --reload
```
- API Base URL: `http://127.0.0.1:8000`
- Interactive Swagger UI: `http://127.0.0.1:8000/docs`
- Default Admin Account: Username `admin`, Password `admin123`

### 2. Frontend Setup (Members 2 & 3)
- Open `frontend/index.html` in your browser or with VS Code Live Server (`http://127.0.0.1:5500`).
- The frontend connects automatically to the FastAPI backend API at `http://127.0.0.1:8000/api`.
- When the backend is not running, the customer catalogue displays built-in preview products so frontend work can continue uninterrupted.
