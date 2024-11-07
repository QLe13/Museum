INSERT INTO Person (name, email, phone, role) VALUES
('Sannvah', 'san30', '1231234545', 'employee'),
('Quang', 'quang','1234567890', 'visitor'),
('David', 'david', '4567891234', 'visitor'),
('test', 'test', '4564564567', 'visitor'),
('Jacob','jacob1','1231231234', 'author'),
('Jack','jack23','5678901234','visitor'),
('Alex', 'Alex45', '1232334567', 'visitor'),
('Belle','bellIntheair','1233334444','visitor'),
('ren', 'kyloBen', '1111111111', 'author'),
('Jonas', 'jonas234', '2221112222', 'visitor'),
(98,'Thing-A-bob','thingaBob','3131223333','visitor');

INSERT INTO Exhibit(name,description,start_date,end_date,current_ticket_price) VALUES
('1800 paintings','painting created during the 1800s','2024-9-23','2025-9-23',10),
('Cats sculptures', 'sculptures of cats', '2024-10-07', '2025-12-31',5),
('Collection of used toothbrushes', 'It a collection of used toothbrushes', '2023-12-25','2024-12-25', 10);

INSERT INTO Visit(person_id, exhibit_id, visit_date,ticket_price) VALUES 
(8, 2, '2024-11-1', 5),
(1, 1, '2024-10-31', 10),
(5, 2, '2024-11-1', 5),
(2, 1, '2024-10-31', 10),
(10,3, '2024-8-30',10),
(9,3,'2024-7-10',10),
(3,1,'2024-11-1',10),
(4,2,'2024-8-29',5),
(7,1,'2024-8-27',10),
(6,2,'2024-11-2',5);


INSERT INTO Item(item_name,item_description, category, price, quantity,exhibit_id, owner_id) VALUES
('Geoge washington toothbrush',’Geroge washington toothbrush’','10000.00',1,3,98),
('Starry Night',"The Famous van Gogh Painting",'Art','9.00',1,1,98),
('Queen Elizabeth toothbrush',"toothbrush of queen elizabeth",'history','1000.00',1,3,98),
('Tabby Cats',"A sculpure of two tabby cats”,'sculpture’,'678.00',2,2,98),
('calico cat',"28 ins size sculpure of cat",'scuplture','1780.00',1,2,98),
('Toilet',"The famous urinal",'Art','800000.00',1,2,98),
('van gogh portiat',"the famous portiat of van gogh",'Art','100000.00',1,1,98),
('Oldest cat sculpure',"the oldest cat sculpure",'scupluture','10.00',1,2,98);


INSERT INTO Transaction(transaction_date, total_amount,buyer_id,seller_id) VALUES
('2024-11-06','10.00',98,5),
('2024-11-01','1800.00',98,5);

INSERT INTO Transaction_Item(transaction_id,item_id,quantity,price) VALUES
(1,66,'1',10.00),
(2,62,'1',1780.00);

