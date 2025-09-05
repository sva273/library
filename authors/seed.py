import random
from faker import Faker
from .models.books import Author, Library

faker = Faker('en_US')
def create_autors(count=100):
    for _ in range(count):
        Author.objects.create(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            date_of_birth=faker.date_of_birth(minimum_age=18, maximum_age=100),
            profile=faker.url(),
            rating=random.randint(1, 10),
            is_deleted=random.choice([True, False]),
        )

    print("Autors created")

def create_library(count=20):
    for _ in range(count):
        Library.objects.create(
            title=faker.company(),
            location=faker.address(),
            site=faker.url(),

        )
    print("Library created")