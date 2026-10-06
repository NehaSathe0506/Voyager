USE Voyager;
INSERT INTO attractions
(destination_id, name, category, latitude, longitude, duration_hours, cost, outdoor)
VALUES
-- Munnar
((SELECT id FROM destinations WHERE name='Munnar'),'Eravikulam National Park','nature',10.1925,77.0603,3,200,TRUE),
((SELECT id FROM destinations WHERE name='Munnar'),'Mattupetty Dam','nature',10.1058,77.1236,1.5,100,TRUE),
((SELECT id FROM destinations WHERE name='Munnar'),'Tea Museum','culture',10.0899,77.0610,1.5,150,FALSE),
((SELECT id FROM destinations WHERE name='Munnar'),'Top Station','nature',10.1170,77.2330,2,50,TRUE),
((SELECT id FROM destinations WHERE name='Munnar'),'Echo Point','relaxation',10.1304,77.1792,1,0,TRUE),
((SELECT id FROM destinations WHERE name='Munnar'),'Attukad Waterfalls','nature',10.0360,77.0100,1.5,50,TRUE),
((SELECT id FROM destinations WHERE name='Munnar'),'Kolukkumalai Jeep Safari','adventure',10.0642,77.2075,4,600,TRUE),
((SELECT id FROM destinations WHERE name='Munnar'),'Munnar Market Walk','culture',10.0889,77.0595,1.5,0,FALSE),
-- Coorg
((SELECT id FROM destinations WHERE name='Coorg'),'Abbey Falls','nature',12.4547,75.7170,1.5,50,TRUE),
((SELECT id FROM destinations WHERE name='Coorg'),'Raja''s Seat','relaxation',12.4189,75.7389,1,30,TRUE),
((SELECT id FROM destinations WHERE name='Coorg'),'Dubare Elephant Camp','adventure',12.3947,75.9161,3,400,TRUE),
((SELECT id FROM destinations WHERE name='Coorg'),'Omkareshwara Temple','culture',12.4249,75.7403,1,0,FALSE),
((SELECT id FROM destinations WHERE name='Coorg'),'Talacauvery','nature',12.3836,75.4964,2,0,TRUE),
((SELECT id FROM destinations WHERE name='Coorg'),'Madikeri Fort','culture',12.4244,75.7382,1.5,20,FALSE),
-- Udaipur
((SELECT id FROM destinations WHERE name='Udaipur'),'City Palace','culture',24.5764,73.6835,2.5,300,FALSE),
((SELECT id FROM destinations WHERE name='Udaipur'),'Lake Pichola Boat Ride','relaxation',24.5714,73.6797,1.5,400,TRUE),
((SELECT id FROM destinations WHERE name='Udaipur'),'Jagdish Temple','culture',24.5801,73.6836,1,0,FALSE),
((SELECT id FROM destinations WHERE name='Udaipur'),'Saheliyon Ki Bari','nature',24.5984,73.6930,1.5,50,TRUE),
((SELECT id FROM destinations WHERE name='Udaipur'),'Sajjangarh Monsoon Palace','nature',24.5961,73.6460,2,300,TRUE),
((SELECT id FROM destinations WHERE name='Udaipur'),'Bagore Ki Haveli','culture',24.5794,73.6803,1.5,100,FALSE),
-- Goa
((SELECT id FROM destinations WHERE name='Goa'),'Baga Beach','nightlife',15.5553,73.7517,3,0,TRUE),
((SELECT id FROM destinations WHERE name='Goa'),'Fort Aguada','culture',15.4925,73.7737,1.5,0,TRUE),
((SELECT id FROM destinations WHERE name='Goa'),'Basilica of Bom Jesus','culture',15.5009,73.9116,1,0,FALSE),
((SELECT id FROM destinations WHERE name='Goa'),'Dudhsagar Falls','adventure',15.3144,74.3143,5,800,TRUE),
((SELECT id FROM destinations WHERE name='Goa'),'Palolem Beach','relaxation',15.0100,74.0232,3,0,TRUE),
((SELECT id FROM destinations WHERE name='Goa'),'Titos Lane','nightlife',15.5568,73.7546,2,500,FALSE);

Use your real database name on the first line. Paste the whole file into the MySQL Command Line Client and press Enter. You should see Query OK, 26 rows affected. Run it once only. The coordinates are approximate, so check them on Google Maps if you want real accuracy.

This seeds Munnar, Coorg, Udaipur and Goa. The other destinations from Step 13 return "no attractions yet" until you add some.

Step 30: Add the request schema

Open backend/schemas.py and add this at the bottom, as its own class at the left margin:

python
class ItineraryRequest(BaseModel):
    destination_id: int
    days: int = Field(ge=1, le=14)
    interests: List[str] = []
    travelers: int = Field(default=1, ge=1, le=20)