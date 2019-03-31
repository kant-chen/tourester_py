CREATE TABLE OrderList(OrderId	text NOT NULL	,
OrderSeq	serial	PRIMARY KEY	,
ProductId	text		,
UnitPrice	numeric		,
Quantity	numeric		,
Amount	numeric		,
Tax	numeric		,
Status	text
                       );

CREATE TABLE SendMail(SendId	text	PRIMARY KEY,
ToAddress	text		,
CcAddress	text		,
SecretCcAddress	text		,
Title	text		,
Article	text		,
Status	text
);

CREATE TABLE Orderd(OrderId	text	PRIMARY KEY	,
OrderTime	timestamp		,
CustomerID	text		,
Status	text
);

CREATE TABLE Product(ProductId	text	PRIMARY KEY	,
ProductName1	text		,
ProductName2	text		,
UnitPrice	numeric		,
StockQty	numeric		,
Status	text
);

CREATE TABLE Customer(CustomerId	text	PRIMARY KEY	,
CustomerName	text		,
Email	text		,
Status	text
);

GRANT ALL ON TABLE public.customer TO kivy;
GRANT ALL ON TABLE public.orderd TO kivy;
GRANT ALL ON TABLE public.orderlist TO kivy;
GRANT ALL ON TABLE public.product TO kivy;
GRANT ALL ON TABLE public.sendmail TO kivy;

ALTER TABLE orderlist
ADD CONSTRAINT orderlist_fk1
FOREIGN KEY (orderid)
REFERENCES orderd(orderid)
ON DELETE CASCADE;

schema = {
'Product': [{'Description': None, 'Col_Name': 'ProductId', 'Type': 'text', 'Primary_Key': 'YES'},
             {'Description': None, 'Col_Name': 'ProductName1', 'Type': 'text', 'Primary_Key': None},
             {'Description': None, 'Col_Name': 'ProductName2', 'Type': 'text', 'Primary_Key': None},
             {'Description': None, 'Col_Name': 'UnitPrice', 'Type': 'numeric', 'Primary_Key': None},
             {'Description': None, 'Col_Name': 'StockQty', 'Type': 'numeric', 'Primary_Key': None},
             {'Description': None, 'Col_Name': 'Status', 'Type': 'text', 'Primary_Key': None}],
'Customer': [{'Description': None, 'Col_Name': 'CustomerId', 'Type': 'text', 'Primary_Key': 'YES'},
             {'Description': None, 'Col_Name': 'CustomerName', 'Type': 'text', 'Primary_Key': None},
             {'Description': None, 'Col_Name': 'E-mail', 'Type': 'text', 'Primary_Key': None},
             {'Description': None, 'Col_Name': 'Status', 'Type': 'text', 'Primary_Key': None}],
'SendMail': [{'Description': None, 'Col_Name': 'SendId', 'Type': 'text', 'Primary_Key': 'YES'},
             {'Description': None, 'Col_Name': 'ToAddress', 'Type': 'text', 'Primary_Key': None},
             {'Description': None, 'Col_Name': 'CcAddress', 'Type': 'text', 'Primary_Key': None},
             {'Description': None, 'Col_Name': 'SecretCcAddress', 'Type': 'text', 'Primary_Key': None},
             {'Description': None, 'Col_Name': 'Title', 'Type': 'text', 'Primary_Key': None},
             {'Description': None, 'Col_Name': 'Article', 'Type': 'text', 'Primary_Key': None},
             {'Description': None, 'Col_Name': 'Status', 'Type': 'text', 'Primary_Key': None}],
'Order': [{'Description': None, 'Col_Name': 'OrderId', 'Type': 'text', 'Primary_Key': 'YES'},
              {'Description': None, 'Col_Name': 'OrderTime', 'Type': 'timestamp', 'Primary_Key': None},
              {'Description': None, 'Col_Name': 'CustomerID', 'Type': 'text', 'Primary_Key': None},
              {'Description': None, 'Col_Name': 'Status', 'Type': 'text', 'Primary_Key': None}],
'OrderList': [{'Description': None, 'Col_Name': 'OrderId', 'Type': 'text', 'Primary_Key': 'YES'},
              {'Description': None, 'Col_Name': 'OrderSeq', 'Type': 'integer', 'Primary_Key': 'YES'},
              {'Description': None, 'Col_Name': 'ProductId', 'Type': 'text', 'Primary_Key': None},
              {'Description': None, 'Col_Name': 'UnitPrice', 'Type': 'numeric', 'Primary_Key': None},
              {'Description': None, 'Col_Name': 'Quantity', 'Type': 'numeric', 'Primary_Key': None},
              {'Description': None, 'Col_Name': 'Amount', 'Type': 'numeric', 'Primary_Key': None},
              {'Description': None, 'Col_Name': 'Tax', 'Type': 'numeric', 'Primary_Key': None},
              {'Description': None, 'Col_Name': 'Status', 'Type': 'text', 'Primary_Key': None}]
}
