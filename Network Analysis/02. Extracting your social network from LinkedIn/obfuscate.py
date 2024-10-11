import random
import pandas as pd


# most popular names and surnames
names = ['Kai', 'Olivia', 'Liam', 'Amelia', 'Noah', 'Mia', 'Rowan', 'Eliana', 'James', 'Asher', 'Ava', 'Emma', 'Charlotte', 'Mila', 'Aria', 'Luna', 'Luca', 'Evelyn', 'Sophia', 'Maeve', 'Nova', 'Ezra', 'Oliver', 'Hazel', 'Jayden', 'Quinn', 'Avery', 'Isla', 'Theo', 'Aurora', 'Riley', 'Ivy', 'Nora', 'Harper', 'Benjamin', 'Remi', 'Theodore', 'Aiden', 'Levi', 'Leo', 'Amara', 'Henry', 'Elijah', 'Ethan', 'Ella', 'Arlo', 'Chloe', 'Finn', 'Alexander', 'Jack', 'William', 'Wren', 'Willow', 'Lucas', 'Atlas', 'Owen', 'Sebastian', 'Amaya', 'Lily', 'Penelope', 'Anya', 'Elias', 'Elizabeth', 'Miles', 'Isabella', 'Royal', 'Zoe', 'Maya', 'Emily', 'Scarlett', 'Ellie', 'Charlie', 'Apollo', 'Hudson', 'Naomi', 'Grace', 'Daniel', 'Everett', 'Mateo', 'River', 'Eleanor', 'Sienna', 'Ayla', 'Milo', 'Eloise', 'Ari', 'Joseph', 'Parker', 'Logan', 'Lucy', 'Atticus', 'Violet', 'Kayden', 'Aurelia', 'Aaliyah', 'Zion', 'Shiloh', 'John', 'Samuel', 'Alex', 'Arthur', 'Alice', 'Silas', 'Emerson', 'Freya', 'Stella', 'Jude', 'Amari', 'Finley', 'David', 'Axel', 'Sage', 'Andrew', 'Micah', 'Michael', 'Abigail', 'Enzo', 'Dylan', 'Kian', 'Maverick', 'Hannah', 'Xavier', 'Julian', 'Aaron', 'Noa', 'Molly', 'Alina', 'Mira', 'Jasper', 'Gianna', 'Sadie', 'Ryan', 'Rhys', 'Nolan', 'Caleb', 'Blake', 'Elliot', 'Jordan', 'Adeline', 'Anthony', 'Elena', 'Anaya', 'Evan', 'Wyatt', 'Lola', 'Lyra', 'Sarah', 'Mae', 'Kira', 'Ophelia', 'Kaia', 'Myra', 'Kieran', 'Layla', 'Iris', 'Zoey', 'Audrey', 'Elodie', 'Claire', 'Sloane', 'Zara', 'Cora', 'Orion', 'Carter', 'Grayson', 'Rory', 'Emery', 'Esther', 'Declan', 'Christian', 'Everly', 'Josiah', 'Sofia', 'Elise', 'Anna', 'Kaiden', 'Matthew', 'Emilia', 'Jade', 'Ruby', 'Beau', 'Nathan', 'Ivan', 'Maria', 'Ronan', 'Thomas', 'Cecilia', 'Jesse', 'Millie', 'Thea', 'Lyla', 'Lilith', 'Kiara', 'Talia', 'Samantha', 'Mary', 'Rachel', 'Clara', 'Rhea', 'Felix', 'Skylar', 'Isaac', 'Remy', 'Arya', 'Ariana', 'Eva', 'Jackson', 'Hailey', 'Malachi', 'Wesley', 'Adrian', 'Raya', 'Sawyer', 'Rose', 'Margot', 'Genevieve', 'Ariella', 'Kyle', 'Ira', 'Isaiah', 'Madeline', 'Callum', 'Brian', 'Bella', 'Jennifer', 'Ezekiel', 'Eli', 'Lydia', 'Christopher', 'Laura', 'Elora', 'Amira', 'Joshua', 'Evie', 'Elliott', 'Marcus', 'Vivian', 'Jason', 'Elsie', 'Kevin', 'Ian', 'Rebecca', 'Emmett', 'Aubrey', 'Brooks', 'Vanessa', 'Atharv', 'Lila', 'Simon', 'Josephine', 'Leon', 'Oscar', 'Cameron', 'Vera', 'Callan', 'Alora', 'Luke', 'Celeste', 'Peter', 'Vincent', 'Akira', 'Mason', 'Dante', 'Leah', 'Delilah', 'Nico', 'Sophie', 'Sharon', 'Ryker', 'Ashley', 'Athena', 'Taylor', 'Cyrus', 'August', 'Phoenix', 'Brandon', 'Morgan', 'Sasha', 'Savannah', 'Lisa', 'Ellis', 'Archer', 'Alma', 'Esme', 'Bennett', 'Fatima', 'Joel', 'Julia', 'Eden', 'Poppy', 'Daisy', 'Azariah', 'Anastasia', 'Max', 'Ariel', 'Rohan', 'Lena', 'Mara', 'Hayden', 'Damian', 'Santiago', 'Gabriel', 'Austin', 'Adam', 'Michelle', 'Mika', 'Naya', 'Alyssa', 'Teagan', 'Amir', 'Tyler', 'Gideon', 'Avyaan', 'Nevaeh', 'Lauren', 'Isabelle', 'Rome', 'Matilda', 'Daphne', 'Cooper', 'Nyla', 'Astrid', 'Caroline', 'Bailey', 'June', 'Kash', 'Maisie', 'Natalie', 'Nathaniel', 'Brielle', 'Kayla', 'Jonathan', 'Archie', 'Lucian', 'Robert', 'Asa', 'Andrea', 'Isha', 'Gavin', 'Jamie', 'Tristan', 'Ada', 'Israel', 'Harlow', 'Victoria', 'Margaret', 'Nina', 'Salem', 'Camila', 'Skye', 'Sean', 'Jace', 'Alana', 'Lincoln', 'Lucia', 'Lachlan', 'Madison', 'Serena', 'Caspian', 'Deborah', 'Priscilla', 'Lennox', 'Muhammad', 'Callie', 'Paul', 'Siobhan', 'Mina', 'Eliza', 'Rae', 'Lilah', 'Damien', 'Kinsley', 'Claudia', 'Reese', 'Avi', 'Luka', 'Killian', 'Ares', 'Jessica', 'Connor', 'Hallie', 'Arden', 'Aisha', 'Pricilla', 'Roman', 'Xander', 'Mabel', 'Leilani', 'Erin', 'Azriel', 'Beckett', 'Fiona', 'Charles', 'Valerie', 'Otto', 'Marie', 'George', 'Amber', 'Mya', 'Nia', 'Blair', 'Alaina', 'Camille', 'Ayesha', 'Elian', 'Aditya', 'Emmanuel', 'Alexandra', 'Justin', 'Arianna', 'Hunter', 'Florence', 'Adriel', 'Kennedy', 'Tara', 'Nicholas', 'Gemma', 'Brianna', 'Keira', 'Lana', 'Soren', 'Sara', 'Cynthia', 'Cole', 'Eric', 'Lennon', 'Rayne', 'Zane', 'Robin', 'Skyler', 'Ali', 'Ren', 'Raiden', 'Patrick', 'Seth', 'Piper', 'Jonah', 'Ishaan', 'Lara', 'Cillian', 'Evangeline', 'Cassius', 'Rich', 'Dominic', 'Lia', 'Linda', 'Bryan', 'Natasha', 'Sydney', 'Rayna', 'Martin', 'Giovanni', 'Louis', 'Louise', 'Flynn', 'Zachary', 'Nick', 'Jeremiah', 'Cleo', 'Peyton', 'Aster', 'Cassandra', 'Gia', 'Sierra', 'Faye', 'Dean', 'Harrison', 'Phoebe', 'Edward', 'Myles', 'Francis', 'Mackenzie', 'Queen', 'Adira', 'Ace', 'Adonis', 'Inayah', 'Sylvia', 'Elio', 'Alexis', 'Yara', 'Saoirse', 'Kit', 'Imogen', 'Judah', 'Seraphina', 'Amy', 'Calvin', 'Raelynn', 'Abel', 'Zainab', 'Elle', 'Jasmine', 'Aidan', 'Jedidiah', 'Callen', 'Scott', 'Hadassah', 'Vihaan', 'Jean']
surnames = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Miller', 'Davis', 'Garcia', 'Rodriguez', 'Wilson', 'Martinez', 'Anderson', 'Taylor', 'Thomas', 'Hernandez', 'Moore', 'Martin', 'Jackson', 'Thompson', 'White', 'Lopez', 'Lee', 'Gonzalez', 'Harris', 'Clark', 'Lewis', 'Robinson', 'Walker', 'Perez', 'Hall', 'Young', 'Allen', 'Sanchez', 'Wright', 'King', 'Scott', 'Green', 'Baker', 'Adams', 'Nelson', 'Hill', 'Ramirez', 'Campbell', 'Mitchell', 'Roberts', 'Carter', 'Phillips', 'Evans', 'Turner', 'Torres', 'Parker', 'Collins', 'Edwards', 'Stewart', 'Flores', 'Morris', 'Nguyen', 'Murphy', 'Rivera', 'Cook', 'Rogers', 'Morgan', 'Peterson', 'Cooper', 'Reed', 'Bailey', 'Bell', 'Gomez', 'Kelly', 'Howard', 'Ward', 'Cox', 'Diaz', 'Richardson', 'Wood', 'Watson', 'Brooks', 'Bennett', 'Gray', 'James', 'Reyes', 'Cruz', 'Hughes', 'Price', 'Myers', 'Long', 'Foster', 'Sanders', 'Ross', 'Morales', 'Powell', 'Sullivan', 'Russell', 'Ortiz', 'Jenkins', 'Gutierrez', 'Perry', 'Butler', 'Barnes', 'Fisher']


# read existing edges
df = pd.read_csv('network_edges.csv')
unique_people = set([*df['Person A'].unique(), *df['Person B'].unique()])


# check if its possible
assert len(unique_people) <= len(names) * len(surnames), \
    f'Not enough names ({len(names)}) and surnames ({len(surnames)}) defined to generate {len(unique_people)} unique people'


# generate new names
new_people = set()
for name in names:
    for surname in surnames:
        new_people.add(f'{name} {surname}')


# shuffle generated names
new_people = list(new_people)
random.shuffle(new_people)


# pair old and new names
mapping = {old: new for old, new in zip(unique_people, new_people)}
mapping['me'] = 'me'


# save to new file
df['Person A'] = df['Person A'].map(mapping)
df['Person B'] = df['Person B'].map(mapping)
df.to_csv('network_edges_new.csv', index=False)
pd.DataFrame(list(mapping.items()), columns=['From', 'To']).to_csv('mapping.csv', index=False)
