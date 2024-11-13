-- Create Pet Owner table (enhanced with additional fields from ER diagram)
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address TEXT,
    contact_number VARCHAR(15),
    email VARCHAR(100) NOT NULL UNIQUE,
    aadhar_no VARCHAR(12) UNIQUE,  -- Added from original as it's important for authentication
    passwords VARCHAR(100),
    
);

-- Create Pets table (base from your schema with added fields)
CREATE TABLE pets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    species VARCHAR(30) NOT NULL,
    breed VARCHAR(50),
    gender ENUM('Male', 'Female') NOT NULL,
    date_of_birth DATE,
    color VARCHAR(30),
    reg_date DATE,  -- Added from original as registration date is important
    owner_id INT,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create Veterinarians table (combined best fields from both)
CREATE TABLE veterinarians (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    clinic_name VARCHAR(100),
    specialization VARCHAR(100),
    contact_number VARCHAR(15),
    license_number VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE
);

-- Create Medical Records table (enhanced with follow-up date)
CREATE TABLE medical_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pet_id INT NOT NULL,
    visit_date DATE NOT NULL,
    diagnosis TEXT,
    treatment TEXT,
    follow_up_date DATE,  -- Added from original as it's important for treatment tracking
    veterinarian_id INT,
    FOREIGN KEY (pet_id) REFERENCES pets(id) ON DELETE CASCADE,
    FOREIGN KEY (veterinarian_id) REFERENCES veterinarians(id)
);

-- Create Vaccinations table (kept your structure as it's more comprehensive)
CREATE TABLE vaccinations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pet_id INT NOT NULL,
    vaccine_name VARCHAR(100) NOT NULL,
    vaccination_date DATE NOT NULL,
    next_due_date DATE,
    veterinarian_id INT,
    FOREIGN KEY (pet_id) REFERENCES pets(id) ON DELETE CASCADE,
    FOREIGN KEY (veterinarian_id) REFERENCES veterinarians(id)
);

-- Create Insurance table (kept your structure with policy_id as primary key)
CREATE TABLE insurance (
    policy_id INT AUTO_INCREMENT PRIMARY KEY,
    pet_id INT NOT NULL,
    insurance_provider VARCHAR(100) NOT NULL,
    policy_number VARCHAR(50) NOT NULL UNIQUE,
    coverage_details TEXT,
    premium_amount DECIMAL(10, 2) NOT NULL,
    policy_start_date DATE NOT NULL,
    policy_end_date DATE NOT NULL,
    FOREIGN KEY (pet_id) REFERENCES pets(id) ON DELETE CASCADE
);

-- Create Pet Activity Log table (kept your structure with time duration)
CREATE TABLE pet_activity_log (
    activity_id INT AUTO_INCREMENT PRIMARY KEY,
    pet_id INT NOT NULL,
    activity_type VARCHAR(50) NOT NULL,
    duration TIME NOT NULL,
    activity_date DATE NOT NULL,
    FOREIGN KEY (pet_id) REFERENCES pets(id) ON DELETE CASCADE
);


-- Insert sample users
INSERT INTO users (name, address, contact_number, email, aadhar_no, passwords, user_role) VALUES
('John Smith', '123 Main St, Springfield', '555-0101', 'john.smith@email.com', '123456789012', 'hashed_password1', 'standard'),
('Emma Wilson', '456 Oak Ave, Rivertown', '555-0102', 'emma.w@email.com', '123456789013', 'hashed_password2', 'standard'),
('Maria Garcia', '789 Pine Rd, Lakeside', '555-0103', 'maria.g@email.com', '123456789014', 'hashed_password3', 'admin'),
('James Brown', '321 Elm St, Highland', '555-0104', 'james.b@email.com', '123456789015', 'hashed_password4', 'standard'),
('Sarah Davis', '654 Maple Dr, Westend', '555-0105', 'sarah.d@email.com', '123456789016', 'hashed_password5', 'standard');

-- Insert sample veterinarians
INSERT INTO veterinarians (name, clinic_name, specialization, contact_number, license_number, email) VALUES
('Dr. Alice Johnson', 'PawsCare Clinic', 'General Practice', '555-1001', 'VET001', 'dr.alice@pawscare.com'),
('Dr. Robert Lee', 'VetHealth Center', 'Surgery', '555-1002', 'VET002', 'dr.lee@vethealth.com'),
('Dr. Emily White', 'Pet Wellness Clinic', 'Dermatology', '555-1003', 'VET003', 'dr.white@petwellness.com'),
('Dr. Michael Chen', 'Animal Care Plus', 'Cardiology', '555-1004', 'VET004', 'dr.chen@animalcare.com');

-- Insert sample pets
INSERT INTO pets (name, species, breed, gender, date_of_birth, color, reg_date, owner_id) VALUES
('Max', 'Dog', 'Golden Retriever', 'Male', '2020-03-15', 'Golden', '2020-05-01', 1),
('Luna', 'Cat', 'Siamese', 'Female', '2021-06-20', 'Cream', '2021-08-01', 2),
('Rocky', 'Dog', 'German Shepherd', 'Male', '2019-12-10', 'Black and Tan', '2020-01-15', 3),
('Bella', 'Cat', 'Persian', 'Female', '2022-02-14', 'White', '2022-04-01', 4),
('Charlie', 'Dog', 'Poodle', 'Male', '2021-09-30', 'Brown', '2021-11-15', 5);

-- Insert sample medical records
INSERT INTO medical_records (pet_id, visit_date, diagnosis, treatment, follow_up_date, veterinarian_id) VALUES
(1, '2023-01-15', 'Annual checkup', 'Routine vaccination', '2024-01-15', 1),
(2, '2023-02-20', 'Mild fever', 'Prescribed antibiotics', '2023-02-27', 2),
(3, '2023-03-10', 'Sprain in left paw', 'Rest and anti-inflammatory medication', '2023-03-24', 3),
(4, '2023-04-05', 'Dental cleaning', 'Professional teeth cleaning', '2023-10-05', 4),
(5, '2023-05-12', 'Skin allergy', 'Prescribed antihistamines', '2023-05-26', 1);

-- Insert sample vaccinations
INSERT INTO vaccinations (pet_id, vaccine_name, vaccination_date, next_due_date, veterinarian_id) VALUES
(1, 'Rabies', '2023-01-15', '2024-01-15', 1),
(2, 'FVRCP', '2023-02-20', '2024-02-20', 2),
(3, 'DHPP', '2023-03-10', '2024-03-10', 3),
(4, 'Rabies', '2023-04-05', '2024-04-05', 4),
(5, 'Bordetella', '2023-05-12', '2023-11-12', 1);

-- Insert sample insurance policies
INSERT INTO insurance (pet_id, insurance_provider, policy_number, coverage_details, premium_amount, policy_start_date, policy_end_date) VALUES
(1, 'PetSure', 'POL001', 'Comprehensive coverage including accidents and illness', 500.00, '2023-01-01', '2023-12-31'),
(2, 'AnimalCare Insurance', 'POL002', 'Basic coverage with dental', 300.00, '2023-02-01', '2024-01-31'),
(3, 'PetProtect', 'POL003', 'Premium coverage with rehabilitation', 750.00, '2023-03-01', '2024-02-29'),
(4, 'VetGuard', 'POL004', 'Standard coverage', 400.00, '2023-04-01', '2024-03-31');

-- Insert sample activity logs
INSERT INTO pet_activity_log (pet_id, activity_type, duration, activity_date) VALUES
(1, 'Walk', '00:30:00', '2023-06-01'),
(2, 'Play', '00:15:00', '2023-06-01'),
(3, 'Training', '00:45:00', '2023-06-01'),
(4, 'Grooming', '01:00:00', '2023-06-01'),
(5, 'Vet Visit', '00:30:00', '2023-06-01');

ALTER TABLE users ADD COLUMN user_role ENUM('admin', 'standard') DEFAULT 'standard';

ALTER TABLE pets
ADD COLUMN vet_id INT,
ADD CONSTRAINT fk_veterinarian
FOREIGN KEY (vet_id) REFERENCES veterinarians(id);

UPDATE 'paws_schema'.'pets' SET 'vet_id' = '1' WHERE ('id' = '1');
UPDATE 'paws_schema'.'pets' SET 'vet_id' = '2' WHERE ('id' = '2');
UPDATE 'paws_schema'.'pets' SET 'vet_id' = '3' WHERE ('id' = '3');
UPDATE 'paws_schema'.'pets' SET 'vet_id' = '4' WHERE ('id' = '4');
UPDATE 'paws_schema'.'pets' SET 'vet_id' = '3' WHERE ('id' = '5');

INSERT INTO pets (name, species, breed, gender, date_of_birth, color, reg_date, owner_id, vet_id) VALUES
("Ann", "Dog", "Pomerian", "Female", "2022-11-20", "White", "2022-11-22", 2, 3),
("Tiger", "Dog", "Labrador", "Male", "2021-1-25", "White and Golden", "2021-1-31", 1, 4),
("Hailey", "Cat", "Ragdoll", "Female", "2023-6-12", "White", "2023-6-15", 1, 2),
("Pinky", "Dog", "Labrador", "Female", "2024-7-23", "White", "2024-7-25", 3, 1),
("Cooper", "Dog", "Samoyed", "Male", "2023-9-04", "Black and Tan", "2023-10-11", 4, 3);