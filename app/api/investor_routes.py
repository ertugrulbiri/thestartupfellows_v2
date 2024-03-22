from datetime import datetime, timedelta

from werkzeug.security import generate_password_hash

from app import db
from app.api import bp
from app.decorator.auth_decorator import token_required_v2
from app.model.user_models import StartupUser, PartnerUser, AdminUser, Slot


@bp.route('/setup/generateDumyData', methods=['GET'])
def create_dummy_users():
    # Create dummy StartupUsers
    for i in range(1, 6):  # Adjust the range as needed
        startup_user = StartupUser(
            email=f'startupuser{i}@example.com',
            password_hash=generate_password_hash('password'),
            name=f'StartupName{i}',
            surname=f'StartupSurname{i}',
            telephone=f'555-010{i}',
            age=20+i,
            gender='Other' if i % 2 == 0 else 'Male',
            birthday=datetime.utcnow() - timedelta(days=365*25),
            university_name='Tech University',
            major='Computer Science',
            student_level='Undergraduate',
            role='Founder',
            country='TechLand',
            is_consent_given=True,
            are_terms_accepted=True,
            is_agreed_to_rules=True
        )
        db.session.add(startup_user)

    # Create dummy PartnerUsers
    for i in range(1, 14):  # Adjust the range as needed
        partner_type = 'Mentor' if i % 2 == 0 else 'Investor'
        partner_user = PartnerUser(
            email=f'partneruser{i}@example.com',
            password_hash=generate_password_hash('password'),
            name=f'PartnerName{i}',
            surname=f'PartnerSurname{i}',
            profession=f'{partner_type} Profession',
            company_name=f'{partner_type} Company',
            type=partner_type
        )
        db.session.add(partner_user)

    # Create dummy AdminUsers
    for i in range(1, 3):  # Adjust the range as needed
        admin_user = AdminUser(
            email=f'adminuser{i}@example.com',
            password_hash=generate_password_hash('password'),
            telephone=f'555-020{i}',
            job=f'AdminJob{i}',
            img_url=f'https://example.com/adminuser{i}.png'
        )
        db.session.add(admin_user)

    # Commit the session to save these objects to the database
    db.session.commit()

    print("Dummy users created successfully.")


from random import randint
from datetime import datetime, timedelta


def create_random_slots_for_partners(n_slots=5):
    # Retrieve all PartnerUsers (Mentors and Investors)
    partner_users = PartnerUser.query.filter(PartnerUser.type.in_(['Mentor', 'Investor'])).all()

    for partner in partner_users:
        for _ in range(n_slots):
            # Generate a random start date within the next 30 days
            random_days = randint(1, 30)
            random_hour = randint(8, 16)  # Assuming slots are between 08:00 and 17:00
            start_time = datetime.now() + timedelta(days=random_days, hours=random_hour, minutes=0)

            # Create a new Slot
            new_slot = Slot(
                user_id=partner.id,
                start_time=start_time,
                # end_time will be automatically set to start_time + 45 minutes by the Slot model
            )
            db.session.add(new_slot)

    # Commit the session to save these slots to the database
    db.session.commit()

    print(f"Random slots created successfully for {len(partner_users)} partner users.")
