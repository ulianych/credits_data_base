# Database Description

This project contains a relational database designed for managing information about legal entities, their credits, and fines. The database consists of three main tables: `UL` (Legal Entities), `CREDIT` (Credits), and `FINE` (Fines). Below is a detailed description of each table and its purpose.

---

## Tables

### 1. **UL (Legal Entities)**
This table stores information about legal entities, including their identification number, name, address, industry code, etc.

#### Schema:
- `INN` (INT, Primary Key, NOT NULL): Unique identification number for the legal entity.
- `NAME` (NVARCHAR(50)): Name of the legal entity.
- `ADDRESS` (NVARCHAR(100)): Address of the legal entity.
- `FIELDOKAD` (INT): Industry or field code.
- `STATUS` (BIT): Current operational status of the entity (1 = active, 0 = inactive).
- `CREATEDATE` (DATE): The date the legal entity was created.

#### Example Data:
| INN   | NAME         | ADDRESS              | FIELDOKAD | STATUS | CREATEDATE  |
|-------|--------------|----------------------|-----------|--------|-------------|
| 1122  | Company J    | 109 Cedar Avenue     | 561       | 1      | 2022-05-15  |
| 2233  | Company K    | 332 Maple Avenue     | 45640     | 1      | 2021-07-20  |
| 3344  | Company L    | 555 Elm Road         | 78500     | 1      | 2020-11-30  |

---

### 2. **CREDIT (Credits)**
This table contains information about loans/credits issued to legal entities. It maintains details such as loan amount, interest rate, loan term, and status.

#### Schema:
- `CREDITID` (INT, Primary Key, NOT NULL, Auto-Increment): Unique identifier for each credit.
- `INN` (INT, Foreign Key): Reference to the `INN` field in the `UL` table, indicating the legal entity that took the loan.
- `CREDIT_SUM` (MONEY): Total loan amount.
- `CREDIT_PERCENT` (INT): Interest rate percentage for the loan.
- `LOAN_DATE` (DATE): The date the loan was issued.
- `TERM` (INT): Loan term in months.
- `CURRENCY` (NVARCHAR(3)): Currency of the loan (e.g., USD, EUR).
- `STATUS` (BIT): Loan status (1 = active, 0 = closed).

#### Relationships:
- **Foreign Key**: `INN` references `UL.INN`.

#### Example Data:
| CREDITID | INN   | CREDIT_SUM | CREDIT_PERCENT | LOAN_DATE  | TERM | CURRENCY | STATUS |
|----------|-------|------------|----------------|------------|------|----------|--------|
| 1        | 4567  | 25000.00   | 15             | 2024-05-20 | 36   | EUR      | 0      |
| 2        | 5678  | 18000.00   | 12             | 2023-10-20 | 24   | USD      | 0      |
| 3        | 6789  | 30000.00   | 18             | 2023-03-16 | 48   | EUR      | 1      |

---

### 3. **FINE (Fines)**
This table tracks fines associated with credits. Each fine is linked to a credit and includes details about the fine amount, payment status, and payment method.

#### Schema:
- `ID` (INT, Primary Key, NOT NULL): Unique identifier for each fine.
- `CREDITID` (INT, Foreign Key): Reference to the `CREDITID` field in the `CREDIT` table, indicating the credit associated with the fine.
- `FINE_DATE` (DATE): The date the fine was issued.
- `FINE_SUM` (MONEY): The amount of the fine.
- `PAID` (BIT): Payment status of the fine (1 = paid, 0 = unpaid).
- `PAYMENT_METHOD` (NVARCHAR(50)): Method of payment (e.g., cash, card, transfer).

#### Relationships:
- **Foreign Key**: `CREDITID` references `CREDIT.CREDITID`.

#### Example Data:
| ID  | CREDITID | FINE_DATE  | FINE_SUM | PAID | PAYMENT_METHOD |
|-----|----------|------------|----------|------|----------------|
| 1   | 3        | 2023-04-15 | 120.00   | 1    | cash           |
| 2   | 4        | 2024-09-22 | 80.00    | 0    | cash           |
| 3   | 3        | 2023-05-15 | 50.00    | 1    | card           |

---

## Relationships Between Tables

1. **`UL` → `CREDIT`**:
   - A legal entity (`UL.INN`) can have multiple credits (`CREDIT.INN`).

2. **`CREDIT` → `FINE`**:
   - A credit (`CREDIT.CREDITID`) can have multiple fines (`FINE.CREDITID`).

---

## Usage

This database can be used for:
- Tracking legal entities and their operational status.
- Managing loans issued to legal entities, including details on amounts, terms, and currencies.
- Monitoring fines imposed on loans and their payment status.

---

## Author
Ihnatchyk Ulyana Sergeevna
3 course, 11 group
2024

---
## Example Queries

1. **Retrieve all active credits for a specific legal entity:**
   ```sql
   SELECT * 
   FROM CREDIT 
   WHERE INN = 1122 AND STATUS = 1;
