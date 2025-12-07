# Database Structure

Unified data structure reference for Smartgement (Go Backend + Python AI Services).

## MySQL Database: `smartgement`

Connection: `mysql://root:@localhost:3306/smartgement`

---

### Table: `users`

Stores merchant/user accounts. Each user is a "merchant" who owns products.

| Column     | Type         | Constraints                    |
|------------|--------------|--------------------------------|
| id         | INT          | PRIMARY KEY, AUTO_INCREMENT    |
| username   | VARCHAR(255) | UNIQUE, NOT NULL               |
| password   | VARCHAR(255) | NOT NULL                       |
| created_at | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP      |
| updated_at | TIMESTAMP    | ON UPDATE CURRENT_TIMESTAMP    |

---

### Table: `products`

Products owned by merchants.

| Column          | Type         | Constraints                         |
|-----------------|--------------|-------------------------------------|
| id              | INT          | PRIMARY KEY, AUTO_INCREMENT         |
| merchant_id     | INT          | NOT NULL, FK -> users.id            |
| name            | VARCHAR(255) | NOT NULL                            |
| description     | TEXT         |                                     |
| stock           | INT          | DEFAULT 0                           |
| price           | DECIMAL(10,2)| NOT NULL                            |
| ingredients     | TEXT         | (optional, for food products)       |
| expiration_date | DATETIME     | (optional)                          |
| category        | VARCHAR(100) | (optional)                          |
| created_at      | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP           |
| updated_at      | TIMESTAMP    | ON UPDATE CURRENT_TIMESTAMP         |

**Index:** `idx_products_merchant_id` on `merchant_id`

---

### Table: `automation_logs`

Logs of chatbot automation commands for auditing and undo.

| Column      | Type         | Constraints                      |
|-------------|--------------|----------------------------------|
| id          | INT          | PRIMARY KEY, AUTO_INCREMENT      |
| merchant_id | INT          | NOT NULL, FK -> users.id         |
| action      | TEXT         | NOT NULL (command executed)      |
| result      | TEXT         | (JSON result of the action)      |
| created_at  | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP        |

---

### Table: `product_trends` (AI Services only)

Tracks daily sales/popularity data for trend analysis.

| Column           | Type         | Constraints                      |
|------------------|--------------|----------------------------------|
| id               | INT          | PRIMARY KEY, AUTO_INCREMENT      |
| product_id       | INT          | NOT NULL, FK -> products.id      |
| date             | DATE         | NOT NULL                         |
| quantity_sold    | INT          | DEFAULT 0                        |
| revenue          | DECIMAL(10,2)| DEFAULT 0                        |
| views            | INT          | DEFAULT 0                        |
| popularity_score | FLOAT        | DEFAULT 0                        |
| meta_data        | JSON         | (optional extra context)         |
| created_at       | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP        |

---

### Table: `product_risks` (AI Services only)

Risk assessments calculated by AI.

| Column         | Type         | Constraints                      |
|----------------|--------------|----------------------------------|
| id             | INT          | PRIMARY KEY, AUTO_INCREMENT      |
| product_id     | INT          | NOT NULL, FK -> products.id      |
| risk_type      | VARCHAR(50)  | NOT NULL                         |
| risk_level     | VARCHAR(20)  | NOT NULL (low/medium/high/critical) |
| risk_score     | FLOAT        | DEFAULT 0                        |
| reason         | TEXT         |                                  |
| recommendation | TEXT         |                                  |
| calculated_at  | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP        |

---

### Table: `automation_history` (AI Services only)

Detailed undo support for automation operations.

| Column               | Type         | Constraints                      |
|----------------------|--------------|----------------------------------|
| id                   | INT          | PRIMARY KEY, AUTO_INCREMENT      |
| merchant_id          | VARCHAR(50)  | NOT NULL                         |
| operation_type       | VARCHAR(50)  | NOT NULL                         |
| command              | TEXT         |                                  |
| affected_product_ids | JSON         |                                  |
| previous_state       | JSON         | (for undo)                       |
| executed_at          | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP        |
| executed_by          | VARCHAR(50)  | DEFAULT 'chatbot'                |

---

## Multi-Tenant Isolation

- **MySQL**: Products are isolated by `merchant_id` foreign key
- **Chatbot**: Uses `merchant_id` from request to query correct products

This ensures each merchant only sees and manages their own products.
