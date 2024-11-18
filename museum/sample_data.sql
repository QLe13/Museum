INSERT INTO museum_app_person (id, name, email, phone, role) VALUES
(1, 'Sannvah', 'san30', '1231234545', 'employee'),
(2, 'Quang', 'quang','1234567890', 'visitor'),
(3, 'David', 'david', '4567891234', 'visitor'),
(4, 'test', 'test', '4564564567', 'visitor'),
(5, 'Jacob','jacob1','1231231234', 'author'),
(6, 'Jack','jack23','5678901234','visitor'),
(7, 'Alex', 'Alex45', '1232334567', 'visitor'),
(8, 'Belle','bellIntheair','1233334444','visitor'),
(9, 'ren', 'kyloBen', '1111111111', 'author'),
(10, 'Jonas', 'jonas234', '2221112222', 'visitor'),
(11, 'Emma Stone', 'emma.stone@example.com', '555-123-4567', 'visitor'),
(12, 'Liam Johnson', 'liam.johnson@example.com', '555-234-5678', 'visitor'),
(13, 'Olivia Brown', 'olivia.brown@example.com', '555-345-6789', 'author'),
(14, 'Noah Davis', 'noah.davis@example.com', '555-456-7890', 'employee'),
(15, 'Ava Wilson', 'ava.wilson@example.com', '555-567-8901', 'visitor'),
(16, 'William Martinez', 'william.martinez@example.com', '555-678-9012', 'visitor'),
(17, 'Sophia Garcia', 'sophia.garcia@example.com', '555-789-0123', 'visitor'),
(18, 'James Anderson', 'james.anderson@example.com', '555-890-1234', 'author'),
(19, 'Isabella Thomas', 'isabella.thomas@example.com', '555-901-2345', 'visitor'),
(20, 'Benjamin Taylor', 'benjamin.taylor@example.com', '555-012-3456', 'visitor');

Insert into museum_app_person(id, name, email, phone, role) VALUES
(98, 'Thing-A-bob','thingaBob','3131223333',' visitor');

INSERT INTO museum_app_exhibit(id, name,description,start_date,end_date,current_ticket_price) VALUES
(1, '1800 paintings','painting created during the 1800s','2024-9-23','2025-9-23',10),
(2, 'Cats sculptures', 'sculptures of cats', '2024-10-07', '2025-12-31',5),
(3, 'Collection of used toothbrushes', 'It a collection of used toothbrushes', '2023-12-25','2024-12-25', 10),
(4, 'Modern Art Collection', 'A selection of contemporary art pieces.', '2024-01-01', '2024-12-31', 15),
(5, 'Ancient Egyptian Artifacts', 'Artifacts from ancient Egypt.', '2024-03-15', '2025-03-14', 12),
(6, 'Renaissance Sculptures', 'Sculptures from the Renaissance period.', '2024-05-01', '2024-11-01', 10),
(7, 'Space Exploration', 'Exhibits related to the history of space travel.', '2024-07-20', '2025-07-20', 18),
(8, 'Medieval Weapons', 'Collection of weapons from the medieval era.', '2024-09-01', '2025-02-28', 8);

INSERT INTO museum_app_visit(id, person_id, exhibit_id, visit_date,ticket_price) VALUES
(1,8, 2, '2024-11-1', 5),
(2,1, 1, '2024-10-31', 10),
(3,5, 2, '2024-11-1', 5),
(4,2, 1, '2024-10-31', 10),
(5,10,3, '2024-8-30',10),
(6,9,3,'2024-7-10',10),
(7,3,1,'2024-11-1',10),
(8,4,2,'2024-8-29',5),
(9,7,1,'2024-8-27',10),
(10,6,2,'2024-11-2',5),
(11,11, 4, '2024-02-10', 15),
(12,12, 5, '2024-04-01', 12),
(13,13, 4, '2024-02-15', 15),
(14,14, 6, '2024-06-05', 10),
(15,15, 7, '2024-08-25', 18),
(16,16, 8, '2024-10-10', 8),
(17,17, 5, '2024-04-15', 12),
(18,18, 6, '2024-07-20', 10),
(19,19, 7, '2024-08-30', 18),
(20,20, 8, '2024-11-15', 8),
(21,2, 4, '2024-02-20', 15),
(22,3, 5, '2024-04-20', 12),
(23,4, 6, '2024-06-15', 10),
(24, 5, 7, '2024-09-01', 18),
(25, 6, 8, '2024-11-20', 8);



INSERT INTO museum_app_Item(id, item_name,item_description, category, price, quantity,exhibit_id, owner_id) VALUES
(1,'Geoge washington toothbrush','Geroge washington toothbrush', 'personal item', '10000.00',1,3,98),
(2,'Starry Night',"The Famous van Gogh Painting",'Art','9.00',1,1,98),
(3,'Queen Elizabeth toothbrush',"toothbrush of queen elizabeth",'history','1000.00',1,3,98),
(4,'Tabby Cats',"A sculpure of two tabby cats",'sculpture','678.00',2,2,98),
(5,'calico cat',"28 ins size sculpure of cat",'scuplture','1780.00',1,2,98),
(6,'Toilet',"The famous urinal",'Art','800000.00',1,2,98),
(7,'van gogh portiat',"the famous portiat of van gogh",'Art','100000.00',1,1,98),
(8,'Oldest cat sculpure',"the oldest cat sculpure",'scupluture','10.00',1,2,98),
(9,'Abstract Painting #1', 'An abstract painting with vibrant colors.', 'Art', 5000.00, 1, 4, 98),
(10,'Pharaoh', 'An ancient Egyptian pharaoh burial mask.', 'Artifact', 25000.00, 1, 5, 98),
(11,'Marble Statue', 'A marble statue from the Renaissance period.', 'Sculpture', 12000.00, 1, 6, 98),
(12,'Apollo Lunar Module Replica', 'A detailed replica of the Apollo Lunar Module.', 'Space', 15000.00, 1, 7, 98),
(13,'Medieval Sword', 'A sword used in medieval battles.', 'Weapon', 8000.00, 1, 8, 98),
(14,'Modern Sculpture', 'A contemporary sculpture made of metal.', 'Art', 7000.00, 1, 4, 98),
(15,'Ancient Scroll', 'An ancient scroll with hieroglyphics.', 'Artifact', 18000.00, 1, 5, 98),
(16,'Bronze Bust', 'A bronze bust of a historical figure.', 'Sculpture', 9000.00, 1, 6, 98),
(17, 'Space Suit', 'An astronaut space suit', 'Space', 22000.00, 1, 7, 98),
(18,'Crossbow', 'A crossbow from the medieval era.', 'Weapon', 6000.00, 1, 8, 98);




INSERT INTO museum_app_Transaction(id, transaction_date, total_amount,buyer_id,seller_id) VALUES
(1,'2024-11-06','10.00',98,5),
(2,'2024-11-01','1800.00',98,5),
(3,'2024-03-01', 5000.00, 11, 98),  
(4,'2024-04-16', 25000.00, 12, 98), 
(5,'2024-05-10', 12000.00, 13, 98), 
(6,'2024-08-26', 15000.00, 15, 98), 
(7,'2024-11-16', 8000.00, 20, 98); 

INSERT INTO museum_app_TransactionItem(id, transaction_id,item_id,quantity,price) VALUES
(1, 1, 1, 1, '10.00'),     
(2, 2, 2, 1, '1780.00'),   
(3, 3, 9, 1, '5000.00'),   
(4, 4, 10, 1, '25000.00'), 
(5, 5, 11, 1, '12000.00'), 
(6, 6, 12, 1, '15000.00'), 
(7, 7, 13, 1, '8000.00'); 
