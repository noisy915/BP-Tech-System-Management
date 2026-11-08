# BP Tech Inventory Management System — Team Roles & File Structure

This document defines the clear division of responsibilities, file ownership, and collaboration workflow for the **3 team members** developing the BP Tech Inventory Management System.

---

## 1. Project Directory & File Ownership Map

Each folder and file in this repository is explicitly assigned to a team member:

```
database/
├── README.md                                  # [Shared] Project overview & specifications
├── TEAM_ROLES.md                              # [Shared] Member assignments & workflow guide
├── index.html                                 # Root launcher redirecting to frontend/
├── .gitignore                                 # [Shared] Git ignore configuration
│
├── backend/                                   # ========================================
│   │                                          # [MEMBER 1: Backend & Database Developer]
│   │                                          # ========================================
│   ├── app/
│   │   ├── __init__.py                        # Python package declaration
│   │   ├── main.py                            # FastAPI app, CORS, routes & lifespan
│   │   ├── config.py                          # Environment variables & DB settings
│   │   ├── database.py                        # SQLAlchemy engine & session factory
│   │   ├── auth_utils.py                      # Bcrypt password hashing & JWT token validation
│   │   ├── seed_data.py                       # Automated database seeder script
│   │   ├── models/                            # SQLAlchemy ORM Models (5 Entities + Admin)
│   │   │   ├── __init__.py
│   │   │   ├── category.py                    # Entity 1: Category
│   │   │   ├── supplier.py                    # Entity 2: Supplier
│   │   │   ├── product.py                     # Entity 3: Product
│   │   │   ├── inventory.py                   # Entity 4: Inventory (1:1 with Product)
│   │   │   ├── stock_movement.py              # Entity 5: Stock_Movement (1:M with Product)
│   │   │   └── admin.py                       # Admin authentication entity
│   │   ├── schemas/                           # Pydantic Schemas for Validation
│   │   │   ├── __init__.py
│   │   │   ├── category.py                    # Category request / response schemas
│   │   │   ├── supplier.py                    # Supplier request / response schemas
│   │   │   ├── product.py                     # Product request / response schemas
│   │   │   ├── inventory.py                   # Inventory request / response schemas
│   │   │   ├── stock_movement.py              # Stock movement request / response schemas
│   │   │   └── auth.py                        # Login & JWT token schemas
│   │   └── routers/                           # REST API Endpoints
│   │       ├── __init__.py
│   │       ├── auth.py                        # POST /api/auth/login, GET /api/auth/me
│   │       ├── categories.py                  # CRUD /api/categories
│   │       ├── suppliers.py                   # CRUD /api/suppliers
│   │       ├── products.py                    # CRUD /api/products (filters, auto-inventory)
│   │       ├── inventory.py                   # GET /api/inventory, PUT /api/inventory/{id}
│   │       └── stock_movements.py             # GET /api/stock-movements, POST movement
│   ├── sql/                                   # PostgreSQL DDL Scripts
│   │   ├── schema.sql                         # Raw PostgreSQL table definitions & constraints
│   │   └── seed.sql                           # Raw PostgreSQL sample data inserts
│   ├── requirements.txt                       # Python dependencies (FastAPI, SQLAlchemy, etc.)
│   ├── .env.example                           # Environment configuration template
│   ├── main.py                                # Convenience proxy (uvicorn main:app --reload)
│   ├── config.py                              # Proxy import for app.config
│   └── database.py                            # Proxy import for app.database
│
└── frontend/                                  # ========================================
    │                                          # [MEMBERS 2 & 3: Frontend Team]
    │                                          # ========================================
    ├── index.html                             # [MEMBER 2] Customer catalogue & WhatsApp UI
    ├── product-detail.html                    # [MEMBER 2] Detailed component view layout
    ├── admin-login.html                       # [MEMBER 2] Administrator login page layout
    ├── admin-dashboard.html                   # [MEMBER 2] Admin inventory & movement dashboard
    │
    ├── css/                                   # [MEMBER 2: Frontend Developer - Styles]
    │   ├── styles.css                         # Customer catalogue & cyber-tech theme
    │   ├── admin.css                          # Dashboard, tables, modals & stat cards
    │   └── responsive.css                     # Mobile and tablet media queries
    │
    └── js/                                    # [MEMBER 3: JS & Integration Developer]
        ├── config.js                          # API base URL & WhatsApp phone number settings
        ├── api.js                             # Fetch API client helper for all REST endpoints
        ├── auth.js                            # JWT token storage, login/logout, page protection
        ├── catalogue.js                       # Category pills, product grid, filters, search
        ├── admin.js                           # Inventory table, product modals, stock movements
        └── whatsapp.js                        # Pre-filled WhatsApp message & URL generator
```

---

## 2. Team Member Responsibilities & Tasks

### 👤 Member 1 — Backend & Database Developer
**Files Owned:** Entire `backend/` directory (`app/`, `sql/`, `requirements.txt`, `.env.example`).

**Main Tasks:**
1. **Database Schema:**
   - Manage the PostgreSQL schema in `backend/sql/schema.sql` and SQLAlchemy models in `backend/app/models/`.
   - Maintain the 5 core relational entities: `Category`, `Supplier`, `Product`, `Inventory`, `Stock_Movement`, and `Admin`.
   - Ensure constraints: non-negative prices/quantities, unique SKU, condition (`New`/`Used`), and 1:1 inventory relationship.
2. **FastAPI Endpoints:**
   - Develop and test REST endpoints in `backend/app/routers/` for products, categories, suppliers, inventory, and stock movements.
   - Enforce that creating a product automatically initializes its 1:1 inventory record.
   - Enforce that recording a stock movement (`IN`, `OUT`, `ADJUSTMENT`) transactionally updates the product's available inventory quantity.
3. **Authentication & Security:**
   - Implement password hashing using bcrypt (`backend/app/auth_utils.py`).
   - Secure admin routes using OAuth2 Bearer JWT tokens.
4. **Testing & Seeding:**
   - Maintain seed data in `backend/app/seed_data.py`.
   - Test endpoints using Swagger UI at `http://127.0.0.1:8000/docs`.

---

### 👤 Member 2 — Frontend Developer (HTML/CSS & UI/UX)
**Files Owned:** `frontend/*.html` and `frontend/css/*`.

**Main Tasks:**
1. **Customer Catalogue (`frontend/index.html`):**
   - Design modern, high-tech dark theme suitable for BP Tech computer shop.
   - Build responsive hero banner, category pills, search input, condition switchers, and product grid.
   - Design product cards showing image, SKU, condition badge (New/Used), price, and live stock indicator.
   - Integrate WhatsApp call-to-action buttons and floating chat bubble.
2. **Administrator Dashboard (`frontend/admin-dashboard.html`):**
   - Create clean admin dashboard layout with navigation tabs.
   - Design statistic metric cards (Total Products, Units in Stock, Low Stock Alerts, Total Movements).
   - Design data tables with action buttons (Edit, Movement, Discontinue).
   - Build accessible modal dialogs for adding/editing products and recording stock movements.
3. **Admin Login Page (`frontend/admin-login.html`):**
   - Style a secure, focused login interface with feedback banners.
4. **Responsive Design (`frontend/css/responsive.css`):**
   - Ensure optimal display across mobile phones, tablets, and desktop displays.

---

### 👤 Member 3 — JavaScript & Frontend Integration Developer
**Files Owned:** Entire `frontend/js/` directory (`config.js`, `api.js`, `catalogue.js`, `admin.js`, `auth.js`, `whatsapp.js`).

**Main Tasks:**
1. **Fetch API Client (`frontend/js/api.js`):**
   - Implement clean asynchronous fetch requests to communicate with Member 1's FastAPI backend.
   - Attach JWT Bearer authorization headers to admin API requests.
2. **Customer Catalogue Integration (`frontend/js/catalogue.js`):**
   - Fetch active products and categories from `/api/products` and `/api/categories`.
   - Dynamically render product cards with live stock availability states.
   - Handle client-side search filtering by keyword, category, and condition (New/Used).
3. **WhatsApp Enquiry Generation (`frontend/js/whatsapp.js`):**
   - Generate dynamic `https://wa.me/<phone>?text=...` links containing pre-filled product details, price, condition, or custom PC build specifications.
4. **Admin Dashboard Integration (`frontend/js/admin.js`):**
   - Fetch and display live inventory data in the admin table.
   - Handle form submissions for adding/editing products.
   - Handle stock movement submissions (IN, OUT, ADJUSTMENT) and immediately refresh inventory counts.
   - Calculate low-stock warnings when `quantity_available <= reorder_level`.
5. **Authentication Handling (`frontend/js/auth.js`):**
   - Handle login form submit, store JWT token in `localStorage`, and redirect to the dashboard.
   - Protect `admin-dashboard.html` from unauthorized access.

---

## 3. How to Run the Project Locally

### Step 1: Start Backend (Member 1)
```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment (if not already done)
python -m venv .venv
# Windows:
.venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Run the database seeder to populate sample data and default admin
python -m app.seed_data

# Start FastAPI development server
uvicorn main:app --reload
```
- API Base URL: `http://127.0.0.1:8000`
- Swagger Interactive Documentation: `http://127.0.0.1:8000/docs`
- Default Admin Credentials: Username: `admin` | Password: `admin123`

### Step 2: Open Frontend (Members 2 & 3)
- Simply open `index.html` or `frontend/index.html` in any browser or with VS Code **Live Server** (e.g. `http://127.0.0.1:5500`).
- The frontend will automatically connect to `http://127.0.0.1:8000/api`.
- When backend is offline, the customer catalogue automatically displays sample preview components.

---

## 4. Git Collaboration Workflow (Avoiding Conflicts)

To work smoothly across 3 people:
1. **Branching Strategy:**
   - `main`: Production-ready code.
   - Member 1 works on: `feature/backend-api`
   - Member 2 works on: `feature/frontend-ui`
   - Member 3 works on: `feature/js-integration`
2. **Strict File Isolation:**
   - Member 1 only modifies `backend/`.
   - Member 2 only modifies `frontend/*.html` and `frontend/css/`.
   - Member 3 only modifies `frontend/js/`.
   - This zero-overlap structure ensures merge conflicts are virtually eliminated!
