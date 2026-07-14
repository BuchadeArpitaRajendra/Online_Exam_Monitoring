from faker import Faker
import csv
import random

# Create Faker object
fake = Faker()

# List of exam subjects
subjects = [
    "Python",
    "Java",
    "C Programming",
    "Data Science",
    "Machine Learning",
    "Web Development",
    "Database Management",
    "Computer Networks"
]

# CSV file name
filename = "sample_candidates.csv"

# Open CSV file
with open(filename, mode="w", newline="") as file:

    writer = csv.writer(file)

    # Header
    writer.writerow([
        "Candidate ID",
        "Name",
        "Email",
        "Age",
        "Exam Subject"
    ])

    # Generate 20 records
    for i in range(1, 21):

        candidate_id = f"C{i:03}"

        name = fake.name()

        email = fake.email()

        age = random.randint(18, 30)

        subject = random.choice(subjects)

        writer.writerow([
            candidate_id,
            name,
            email,
            age,
            subject
        ])

print("20 Sample Candidate Records Generated Successfully!")
print("File saved as sample_candidates.csv")