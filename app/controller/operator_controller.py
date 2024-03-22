from datetime import datetime, timedelta

from flask import jsonify

from app import db
from app.errors import bad_request
from app.model.user_models import StartupCompany, Meeting, User, MeetingNote, Slot, PartnerUser


def get_current_client_controller(user):
    if user.type == "StartUp":
        user = user.get_start_up()
    elif user.type == "AdminUser":
        user = user.admin_user()
    elif user.type == "PartnerUser":
        user = user.partner_user()
    if user:
        return jsonify(user.to_dict())
    return bad_request("User Type Not Found")


def get_all_startups_controller(user):
    startups = db.session.query(StartupCompany).all()
    startup_list = [startup.to_dict() for startup in startups]

    return startup_list


def add_partner_controller(user, request):
    data = request.get_json()

    return None


def set_meeting_controller(user, request):
    data = request.get_json()
    user_list = data.get('user_list')
    start_date_str = data.get('start_date')
    purpose = data.get('purpose')
    slot_id = data.get('slot_id')

    # Parse the start_date string into a datetime object
    start_date = datetime.strptime(start_date_str, '%d-%m-%Y %H:%M:%S')
    # Calculate the end_date based on a 45-minute duration
    end_date = start_date + timedelta(minutes=45)

    # Create a new Meeting instance
    meeting = Meeting(start_date=start_date, end_date=end_date, purpose=purpose)
    db.session.add(meeting)

    for user_id in user_list:
        user = User.query.get(user_id)
        if user:
            # Check for an existing slot that matches the meeting time
            slot = Slot.query.filter_by(user_id=user.id, slot_id=slot_id).first()
            if slot and not slot.is_booked:
                slot.is_booked = True
            meeting.attendees.append(user)
    db.session.commit()

    # Return a success response
    return jsonify({'message': 'Meeting set successfully', 'meeting_id': meeting.id}), 200

# Don't forget to register this controller with a route in your Flask app
def get_all_users_controller(user):
    users = db.session.query(User).all()
    user_list = [user.to_dict() for user in users]

    return jsonify(user_list)


def get_all_meetings_of_users(user):
    meetings_data = []
    # Access the user's meetings directly through the 'meetings' relationship
    for meeting in user.meetings:
        meeting_info = {
            'meeting_id': meeting.id,
            'start_date': meeting.start_date.strftime('%Y-%m-%d %H:%M:%S'),
            'end_date': meeting.end_date.strftime('%Y-%m-%d %H:%M:%S'),
            'purpose': meeting.purpose,
            'location': meeting.location,
            'attendees': [],
            'notes': []
        }

        # Include information about other attendees
        for attendee in meeting.attendees:
            if attendee.id != user.id:  # Optionally, exclude the current user from the list
                attendee_info = {
                    'user_id': attendee.id,
                    'email': attendee.email,
                    # Add other relevant user details here
                }
                meeting_info['attendees'].append(attendee_info)

        # Include notes associated with the meeting
        for note in meeting.notes:
            note_info = {
                'note_id': note.id,
                'content': note.content,
                'created_at': note.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                # Assuming you want to show who authored the note
                'user_id': note.authors[0].id,
                'email': note.authors[0].email
            }
            meeting_info['notes'].append(note_info)

        meetings_data.append(meeting_info)

    return jsonify(meetings_data), 200


def add_note_to_meeting(user, request):
    # Retrieve the meeting and user from the database
    data = request.get_json()
    if "meeting_id" not in data or "content" not in data:
        return bad_request('missing meeting_id or content')

    meeting = Meeting.query.get(data['meeting_id'])
    # Extract note content from the request
    note_content = data.get('content')

    # Create the new note
    new_note = MeetingNote(content=note_content, meeting_id=meeting.id)
    # Assume each note can have multiple authors, but for this example, we're just adding the current user
    new_note.authors.append(user)

    # Add the note to the database and commit the changes
    db.session.add(new_note)
    db.session.commit()

    return jsonify({'message': 'Note added successfully', 'note_id': new_note.id}), 200


def add_meeting_slot_controller(user, request):
    data = request.get_json()
    start_time_str = data.get('start_time')

    # Convert start_time_str to a datetime object
    start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')

    # Create the new Slot instance
    new_slot = Slot(user_id=user.id, start_time=start_time)

    # Add the new slot to the session and commit
    db.session.add(new_slot)
    db.session.commit()

    return jsonify({'message': 'Slot created successfully', 'slot': new_slot.to_dict()}), 200


def get_all_partners_controller(user):
    partners = db.session.query(PartnerUser).all()
    partner_list = [partner.to_dict() for partner in partners]
    return jsonify(partner_list)