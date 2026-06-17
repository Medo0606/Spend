# Spende: Personal Finance & Expense Tracker

#### Video Demo: <URL HERE>

## 📌 Project Overview
**Spende** is a comprehensive, secure web-based financial management application built with **Python**, **Flask**, and **SQLite**. The core goal of this project is to empower users to seamlessly track their personal cash flows, monitor income sources, and control their spending habits through descriptive, categorized transaction logs.

---

## 📊 Key Financial Framework & Features

### 1. Unified Ledger (Main Dashboard)
* Dynamically aggregates all past financial data to present a clear summary of **Total Balance**, **Cumulative Income**, and **Total Expenses**.
* Renders a real-time ledger component showcasing transactional history with granular metadata (amounts, methods, notes, and dates).

### 2. Multi-Asset Account Tracking
Monitors exactly where funds are moving by mapping inputs to active accounts:
* 💵 Cash
* 🏦 Bank Account
* 💳 Card

### 3. Granular Cash Flow Categorization
To control data distribution and maximize structural control, transactions are bound to immutable, predefined categorizations protected against input manipulation:
* **Income Stream Nodes:** 💰 Allowance, 💼 Salary, 💵 Petty Cash, 🎁 Bonus.
* **Expense Allocation Nodes:** 🍔 Food, 🎉 Social Life, 🐾 Pets, 🚌 Transport, 🏠 Household, 💊 Health, 💅 Beauty, 📚 Education, 🎁 Gift.

---

## 🛠️ Technical Architecture & Security Features

The application incorporates strict defensive programming constraints to enforce database integrity and prevent injection or data corruption:

* **Authentication & Cryptography:** Leverages `werkzeug.security` to securely hash user passwords using standard PBKDF2 algorithms before entry into the `users` relational database.
* **Session Management:** Utilizes a secure, file-system-backed server session layer (`flask_session`) rather than basic signed cookies to store user IDs, maintaining a non-cacheable data loop for maximum privacy.
* **Input Validation & Security Defense:** * Implements strict check constraints via Python logical loops ensuring financial inputs (`amount`) cannot be negative or null.
  * Cross-verifies input requests directly against static programmatic lists (`category_income`, `category_expense`, `accounts`) to mitigate structural tampering or arbitrary server injections.
* **Data Concurrency:** Leverages `cs50.SQL` object mappers to execute synchronized transactional operations (atomic `INSERT`, `SELECT`, and `DELETE` queries tied specifically to isolated `user_id` scopes).

---

## 🔧 Core Functional Architecture

* `index()`: Serves as the central analytical engine; fetches past user entries, parses absolute values, and dynamically maps the floating balance via continuous iterative evaluation loops.
* `income()` & `expense()`: Handlers that validate client-side forms, pass error flashes via Jinja templates upon anomaly detection, and execute serialized row write-ins back into the relational schema.
* `delete()`: Safeguards user partitions by restricting data-wiping actions (`DELETE`) strictly to records containing matching `user_id` ownership flags.
* `change_password()`: Allows authenticated updates to stored credentials by re-hashing the target profile parameters securely.

---

## 🚀 Future Roadmap
* Integrating automated visualization dashboards (Pie charts for categorical expense distributions using Chart.js).
* Implementing month-over-month budgeting thresholds and predictive deficit alerts.
