from datetime import date

from faker import Faker

from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models

from .validators import valid_email_domains, ValidEmailDomain

VALID_DOMAIN_LIST = ('@gmail.com', '@yahoo.com', '@test.com')


class Student(models.Model):
    first_name = models.CharField(
        max_length=100,
        verbose_name='first name',
        # db_column='first_name_column',
        validators=[MinLengthValidator(2, '"first_name" field value less than two symbols')]
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name='last name',
        # db_column='last_name_column',
        validators=[MinLengthValidator(2)],
        error_messages={'min_length': '"last_name" field value less than two symbols'}
    )
    birthday = models.DateField(default=date.today, null=True, blank=True)
    # birthday = models.DateField(null=True, blank=True)
    # email = models.EmailField(validators=[valid_email_domains])
    email = models.EmailField(validators=[ValidEmailDomain(*VALID_DOMAIN_LIST)])

    def __str__(self):
        return f'{self.pk} {self.first_name} {self.last_name}'

    class Meta:
        db_table = 'students'

    @classmethod
    def generate_fake_data(cls, cnt):
        f = Faker()

        for _ in range(cnt):
            first_name = f.first_name()
            last_name = f.last_name()
            email = f'{first_name}.{last_name}{f.random.choice(VALID_DOMAIN_LIST)}'
            birthday = f.date()
            st = cls(first_name=first_name, last_name=last_name, birthday=birthday, email=email)
            try:
                st.full_clean()
                st.save()
            except ValidationError:
                print(f'Incorrect data {first_name}, {last_name}, {email}, {birthday}')

