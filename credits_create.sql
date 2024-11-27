use test

CREATE TABLE UL (
    INN INT PRIMARY KEY NOT NULL,
    NAME NVARCHAR(50),
    ADDRESS NVARCHAR(100),
    FIELDOKAD INT,
    STATUS BIT,
    CREATEDATE DATE
);

INSERT INTO UL (INN, NAME, ADDRESS, FIELDOKAD, STATUS, CREATEDATE) VALUES
(1122, 'Company J', '109 Cedar Avenue', 561, 1, '2022-05-15'),
(2233, 'Company K', '332 Maple Avenue', 45640, 1, '2021-07-20'),
(3344, 'Company L', '555 Elm Road', 78500, 1, '2020-11-30'),
(4455, 'Company M', '778 Oak Road', 45640, 0, '2019-03-10'),
(4567, 'Company D', '321 Pine Street', 45640, 1, '2018-09-25'),
(5678, 'Company E', '654 Cedar Street', 3341, 1, '2017-12-12'),
(6789, 'Company F', '987 Maple Street', 561, 1, '2016-08-07'),
(7890, 'Company G', '210 Elm Avenue', 561, 0, '2015-02-18'),
(8901, 'Company H', '543 Oak Avenue', 78500, 1, '2014-06-29'),
(9012, 'Company I', '876 Pine Avenue', 78500, 1, '2013-10-03');

CREATE TABLE CREDIT (
    CREDITID int PRIMARY KEY NOT NULL IDENTITY,
    INN int,
    CREDIT_SUM money,
    CREDIT_PERCENT int,
    LOAN_DATE date,
    TERM int,
    CURRENCY nvarchar(3),
    STATUS bit,
    FOREIGN KEY (INN) REFERENCES UL(INN)
);

INSERT INTO CREDIT (INN, CREDIT_SUM, CREDIT_PERCENT, LOAN_DATE, TERM, CURRENCY, STATUS)
VALUES
(4567, 25000, 15, '2024-05-20', 36, 'EUR', 0),
(5678, 18000, 12, '2023-10-20', 24, 'USD', 0),
(6789, 30000, 18, '2023-03-16', 48, 'EUR', 1),
(7890, 22000, 10, '2024-09-30', 12, 'USD', 0),
(8901, 35000, 20, '2024-09-25', 60, 'EUR', 1),
(9012, 28000, 16, '2023-06-11', 40, 'USD', 1),
(1122, 20000, 12, '2024-08-23', 24, 'USD', 1),
(2233, 32000, 18, '2024-01-24', 48, 'EUR', 1),
(3344, 27000, 14, '2023-06-14', 36, 'USD', 1),
(4455, 19000, 10, '2021-11-19', 18, 'EUR', 0);

CREATE TABLE FINE (
    ID int PRIMARY KEY NOT NULL IDENTITY,
    CREDITID int,
    FINE_DATE date,
    FINE_SUM money,
    PAID bit,
    PAYMENT_METHOD nvarchar(50),
    FOREIGN KEY (CREDITID) REFERENCES CREDIT(CREDITID)
);

INSERT INTO FINE (CREDITID, FINE_DATE, FINE_SUM, PAID, PAYMENT_METHOD) VALUES
(3, '2023-04-15', 120, 1, 'cash'),
(4, '2024-09-22', 80, 0, 'cash'),
(3, '2023-05-15', 50, 1, 'card'),
(5, '2024-10-14', 100, 0, 'transfer'),
(7, '2024-10-14', 200, 0, 'card');
