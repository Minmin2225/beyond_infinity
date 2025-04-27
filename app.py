from flask import Flask, render_template, session, redirect, url_for, flash, request, jsonify
from supabase import create_client, Client
import auth  # Import authentication functions
import os   
from datetime import datetime

# Supabase Configuration
SUPABASE_URL = "https://crccujnpdndpturklluu.supabase.co"  # Replace with your Supabase URL
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNyY2N1am5wZG5kcHR1cmtsbHV1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ3MTQ4NjEsImV4cCI6MjA2MDI5MDg2MX0.T5S3MlekwzmN6vZHUtIRq-UJnHOd3QComFBf-cT3Ae4"  # Replace with your Supabase API Key
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)
app.secret_key = "Secret"  # Replace with a strong, unique secret key
BUCKET_NAME = "logo"

# ---------------- Home Route ----------------
@app.route('/')
def index():
    try:
        company_profile = supabase.table('company_profile').select('*').eq('id', '5854aecf-3be0-42a9-8ada-f8254c193a26').single().execute()
        response = supabase.table("services").select("*").order("package_name").execute()
        testimonials_response = supabase.table("testimonials").select("*").order("created_at", desc=True).limit(5).execute()
        logo_url = None
        if company_profile.data:
            logo_url = company_profile.data['logo_url']
            services = response.data if response.data else []
            testimonials = testimonials_response.data if testimonials_response.data else []
            return render_template('index.html', logged_in=session.get('logged_in', False), services=services, logo_url=logo_url, company_profile=company_profile.data, testimonials=testimonials)
    except Exception as e:
        print(f"Error fetching services: {e}")
        flash("Error loading services", "danger")
        return render_template('index.html', logged_in=session.get('logged_in', False), services=[])

# ---------------- Static Pages ----------------
@app.route('/about')
def about():
    company_profile = supabase.table('company_profile').select('*').eq('id', '5854aecf-3be0-42a9-8ada-f8254c193a26').single().execute()
    logo_url = None
    if company_profile.data:   
            logo_url = company_profile.data['logo_url']
    return render_template('about.html',
                        logged_in=session.get('logged_in', False),
                        logo_url=logo_url,
                        company_profile=company_profile.data)

@app.route('/property-list')
def property_list():
    company_profile = supabase.table('company_profile').select('*').eq('id', '5854aecf-3be0-42a9-8ada-f8254c193a26').single().execute()
    logo_url = None
    if company_profile.data:   
            logo_url = company_profile.data['logo_url']
    return render_template('property_list.html', logged_in=session.get('logged_in', False),logo_url=logo_url,
                        company_profile=company_profile.data)

@app.route('/property-type')
def property_type():
    company_profile = supabase.table('company_profile').select('*').eq('id', '5854aecf-3be0-42a9-8ada-f8254c193a26').single().execute()
    logo_url = None
    if company_profile.data:   
            logo_url = company_profile.data['logo_url']
    return render_template('property_type.html', logged_in=session.get('logged_in', False),logo_url=logo_url,
                        company_profile=company_profile.data)

@app.route('/contact')
def contact():
    company_profile = supabase.table('company_profile').select('*').eq('id', '5854aecf-3be0-42a9-8ada-f8254c193a26').single().execute()
    logo_url = None
    if company_profile.data:   
            logo_url = company_profile.data['logo_url']
    return render_template('contact.html', logged_in=session.get('logged_in', False),logo_url=logo_url,
                        company_profile=company_profile.data)

# ---------------- Register/Login Routes ----------------
@app.route('/register')
def register():
    company_profile = supabase.table('company_profile').select('*').eq('id', '5854aecf-3be0-42a9-8ada-f8254c193a26').single().execute()
    logo_url = None
    if company_profile.data:   
            logo_url = company_profile.data['logo_url']
    return render_template('register.html', logged_in=False, logo_url=logo_url,
                        company_profile=company_profile.data)

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        flash("Please log in first.", "warning")
        return redirect(url_for('register'))
    
    try:
        # Fetch bookings for the current user from Supabase
        response = supabase.table("bookings")\
                         .select("*")\
                         .eq("email", session['email'])\
                         .execute()
        
        bookings = response.data if response.data else []
        # Fetch testimonials for the current user from Supabase
        testimonials_response = supabase.table("testimonials")\
                                       .select("*")\
                                       .order("created_at", desc=True)\
                                       .limit(5)\
                                       .execute()
        testimonials = testimonials_response.data if testimonials_response.data else []
        return render_template('dashboard.html', 
                            logged_in=True,
                            bookings=bookings,
                            testimonials=testimonials)
    except Exception as e:
        print(f"Error fetching bookings: {e}")
        flash("Error loading bookings", "danger")
        return render_template('dashboard.html', 
                            logged_in=True,
                            bookings=[],
                            testimonials=[])

@app.route('/book_event', methods=['POST'])
def book_event():
    if 'email' not in session:
        flash("You must be logged in to book an event.", "warning")
        return redirect(url_for('dashboard'))

    try:
        target_date = request.form['target_date']
        venue = request.form['venue']
        event_type = request.form['event_type'].strip()
        service_package = request.form['service_package'].strip()
        contact_number = request.form['phone']
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        email = session['email']

        # ✅ Validate that service_package is one of the allowed options
        allowed_packages = ["Package A", "Package B", "Package C", "Package D", "Package E", "Package F", "Package G"]
        if service_package not in allowed_packages:
            flash("Invalid service package selected.", "danger")
            return redirect(url_for('dashboard'))

        # ✅ Validate that event_type is one of the allowed options
        allowed_event_types = ["Wedding", "Birthday", "Christening", "Corporate", "Social", "Other"]
        if event_type not in allowed_event_types:
            flash("Invalid event type selected.", "danger")
            return redirect(url_for('dashboard'))

        # ✅ Insert data into Supabase
        response = supabase.table("bookings").insert({
            "email": email,
            "event_date": target_date,
            "location": venue,
            "event_type": event_type,
            "package_name": service_package,
            "contact_number": contact_number,
            "start_time": start_time,
            "end_time": end_time
        }).execute()

        if response.data:
            flash("Booking request submitted successfully!", "success")
        else:
            flash(f"Failed to submit booking. Error: {response.error}", "danger")

    except Exception as e:
        flash(f"An error occurred: {e}", "danger")
        print("❌ Exception:", str(e))

    return redirect(url_for('dashboard'))

# New route to handle testimonial submission from dashboard
@app.route('/submit_testimonial', methods=['POST'])
def submit_testimonial():
    if 'email' not in session:
        flash("You must be logged in to submit a testimonial.", "warning")
        return redirect(url_for('dashboard'))

    try:
        user_name = request.form.get('user_name')
        testimonial_text = request.form.get('testimonial_text')
        profession = request.form.get('profession')
        rating = request.form.get('rating')
        email = session['email']

        # Validate required fields
        if not testimonial_text or not rating:
            flash("Please provide testimonial text and rating.", "danger")
            return redirect(url_for('dashboard'))

        # Insert testimonial into Supabase
        response = supabase.table("testimonials").insert({
            "client_name": user_name,
            "testimonial_text": testimonial_text,
            "profession": profession,
            "rating": int(rating),
            "email": email
        }).execute()

        if response.data:
            flash("Thank you for your feedback!", "success")
        else:
            flash(f"Failed to submit testimonial. Error: {response.error}", "danger")

    except Exception as e:
        flash(f"An error occurred: {e}", "danger")
        print("❌ Exception:", str(e))

    return redirect(url_for('dashboard'))

@app.route('/edit_event', methods=['POST'])
def edit_event():
    try:
        event_id = request.form['event_id']
        updated_data = {
            "email": request.form['email'],
            "event_type": request.form['event_type'],
            "event_date": request.form['event_date'],
            "location": request.form['location'],
            "start_time": request.form['start_time'],
            "end_time": request.form['end_time'],
            "package_name": request.form['package_name'],
            "status": request.form['status']
        }

        response = supabase.table("bookings").update(updated_data).eq("id", event_id).execute()

        if response.data:
            flash("Event updated successfully!", "success")
        else:
            flash("Failed to update event.", "danger")

    except Exception as e:
        flash(f"An error occurred while updating: {e}", "danger")

    return redirect(url_for('events_management'))

@app.route('/delete_event', methods=['POST'])
def delete_event():
    event_id = request.form['event_id']
    response = supabase.table("bookings").delete().eq("id", event_id).execute()
    if response.data:
        flash("Event deleted successfully!", "success")
    else:
        flash("Error occurred while trying to delete the event.", "danger")
    return redirect(url_for('events_management'))

@app.route('/login', methods=['POST'])
def login():
    return auth.login()

@app.route('/signup', methods=['POST'])
def signup():
    return auth.signup()


@app.route('/update_profile_combined', methods=['POST'])
def update_profile_combined():
    if 'email' not in session:
        flash("You must be logged in to update your profile.", "warning")
        return redirect(url_for('login'))

    try:
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        availability = request.form.get('availability_status')
        user_email = session['email']

        # Split full_name into first_name and last_name
        if full_name:
            name_parts = full_name.strip().rsplit(' ', 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ''
        else:
            first_name = ''
            last_name = ''

        # Update user information in the database
        update_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "availability": availability
        }

        response = supabase.table("users").update(update_data).eq("email", user_email).execute()

        if response.data:
            # Update session email if changed
            if email != user_email:
                session['email'] = email
            flash("Profile updated successfully!", "success")
        else:
            flash("Failed to update profile.", "danger")

    except Exception as e:
        flash(f"An error occurred: {e}", "danger")
        print("❌ Exception:", str(e))

    return redirect(url_for('staff_profile'))


@app.route('/logout')  # Restored logout route
def logout():
    return auth.logout()


# ---------------- ADMIN ROUTING AND FUNCTION ----------------
@app.route('/admin_login')  # Restored logout route
def admin_login():
    return render_template('admin/admin_login.html')

@app.route('/update_user', methods=['POST'])
def update_user():
    if 'user_role' not in session or session['user_role'] != 'Admin':
        flash("Unauthorized access.", "danger")
        return redirect(url_for('dashboard'))

    try:
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone')
        role = request.form.get('role')

        if not email:
            flash("User email is required.", "danger")
            return redirect(url_for('users_management'))

        update_data = {
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "role": role
        }

        response = supabase.table('users').update(update_data).eq('email', email).execute()

        if response.data:
            flash("User updated successfully!", "success")
        else:
            flash("Failed to update user.", "danger")

    except Exception as e:
        flash(f"An error occurred while updating user: {e}", "danger")

    return redirect(url_for('users_management'))

@app.route('/staff_scheduling')  
def staff_scheduling():
    if 'user_role' not in session or session['user_role'] != 'Admin':
        return redirect(url_for('dashboard'))
    
    # Fetch approved bookings
    bookings_response = supabase.table('bookings').select('*').eq('status', 'Approved').execute()
    approved_bookings = bookings_response.data if bookings_response.data else []
    
    # Fetch all staff users
    staff_response = supabase.table('users').select('*').eq('role', 'Staff').execute()
    staff_users = staff_response.data if staff_response.data else []

    # Fetch staff assignments
    assignments_response = supabase.table('staff_assignments').select('*').execute()
    assignments = assignments_response.data if assignments_response.data else []

    # Fetch staff tasks with related staff_email and booking_id from assignments
    tasks_response = supabase.table('staff_tasks')\
        .select('*, staff_assignments!inner(staff_email, booking_id)')\
        .execute()
    tasks_raw = tasks_response.data if tasks_response.data else []

    # Flatten tasks to include staff_email and booking_id at top level for template
    tasks = []
    for task in tasks_raw:
        task_flat = dict(task)
        assignment = task.get('staff_assignments')
        if assignment:
            task_flat['staff_email'] = assignment.get('staff_email')
            task_flat['booking_id'] = assignment.get('booking_id')
        else:
            task_flat['staff_email'] = None
            task_flat['booking_id'] = None
        tasks.append(task_flat)
    
    return render_template('admin/staff_scheduling.html', 
                           staff_users=staff_users, 
                           approved_bookings=approved_bookings,
                           assignments=assignments,
                           tasks=tasks)


@app.route('/assign_staff', methods=['POST'])
def assign_staff():
    if 'user_role' not in session or session['user_role'] != 'Admin':
        return redirect(url_for('dashboard'))

    staff_email = request.form['staff_email']
    booking_id = request.form['booking_id']  # Changed to event_id to match JS
    assigned_date = request.form['assigned_date']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    role = request.form['role']

    # Check if staff is already assigned on the same date and time
    conflict_query = supabase.table('staff_assignments').select('*').eq('staff_email', staff_email).eq('assigned_date', assigned_date).execute()

    conflicts = conflict_query.data if conflict_query.data else []

    for conflict in conflicts:
        # Check time overlaps
        conflict_start = conflict['start_time']
        conflict_end = conflict['end_time']

        if not (end_time <= conflict_start or start_time >= conflict_end):
            return jsonify({'success': False, 'message': 'Staff already assigned at that time!'}), 400

    # No conflict, insert assignment
    new_assignment = {
        'staff_email': staff_email,
        'booking_id': booking_id,
        'assigned_date': assigned_date,
        'start_time': start_time,
        'end_time': end_time,
        'role': role
    }

    supabase.table('staff_assignments').insert(new_assignment).execute()

    return redirect(staff_scheduling)

@app.route('/users_management')
def users_management():
    if 'user_role' not in session or session['user_role'] != 'Admin':
        return redirect(url_for('dashboard'))
    
    users_response = supabase.table('users').select('*').execute()
    users = users_response.data
    return render_template('admin/user_management.html', logged_in=session.get('logged_in', False), users=users)


@app.route('/admin_settings')
def admin_settings():
    # Fetch the first company profile row
    response = supabase.table('company_profile').select('logo_url').eq('id', '5854aecf-3be0-42a9-8ada-f8254c193a26').single().execute()


    logo_url = None
    if response.data:
        logo_url = response.data['logo_url']

    return render_template('admin/admin_settings.html', logo_url=logo_url)

@app.route('/upload_logo', methods=['POST'])
def upload_logo():
    file = request.files.get('logo')
    print(file)
    if file:
        filename = "company_logo.jpg"
        try:
            file_content = file.read()

            supabase.storage.from_(BUCKET_NAME).update(  # <-- use update for upsert behavior
                path=filename,
                file=file_content,
                file_options={"content-type": file.content_type}
            )

            public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(filename)

            supabase.table('company_profile').update({
                "logo_url": public_url
            }).eq('id', '5854aecf-3be0-42a9-8ada-f8254c193a26').execute()

            return jsonify(success=True, new_logo_url=public_url)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify(success=False)
    else:
        return jsonify(success=False)



@app.route('/save_profile', methods=['POST'])
def save_profile():
    data = request.json
    try:
        supabase.table('company_profile').update({
            "company_name": data.get('companyName'),
            "contact_name": data.get('contactName'),
            "email": data.get('email'),
            "phone": data.get('phone'),
            "street_address": data.get('streetAddress'),
            "city": data.get('city'),
            "state": data.get('state'),
            "zip_code": data.get('zipCode'),
            "tax_id": data.get('taxId'),
            "website": data.get('website')
        }).eq('id', '5854aecf-3be0-42a9-8ada-f8254c193a26').execute()

        return jsonify(success=True)
    except Exception as e:
        print(e)
        return jsonify(success=False)

@app.route('/events_management')
def events_management():
    if 'user_role' not in session or session['user_role'] != 'Admin':
        return redirect(url_for('dashboard'))
    
    view_type = request.args.get('view', 'list')

    bookings = supabase.table('bookings').select('*').execute()
    events = bookings.data

    # Fetch prices for each package in events
    package_names = list(set(e['package_name'] for e in events if 'package_name' in e))
    services_data = supabase.table('services').select('package_name, price').in_('package_name', package_names).execute()
    package_prices = {service['package_name']: service['price'] for service in services_data.data}
    # Add price to each event
    for e in events:
        e['price'] = package_prices.get(e.get('package_name'), 0)

    calendar_events = [
        {
            'email': e['email'],
            'event_type': e['event_type'],
            'event_date': e['event_date'],
            'location': e['location'],
            'status': e['status'],
            'package': e['package_name'],
            'start_time': e['start_time'],
            'end_time': e['end_time']
        }
        for e in events if e.get('event_date')
    ]

    # Get total revenue
    total_revenue = Compute()

    return render_template('admin/event_management.html',
                           events=events,
                           calendar_events=calendar_events,
                           view_type=view_type,
                           total_revenue=total_revenue)

def Compute():
    return auth.Compute()

@app.route('/admin_dashboard')  # Restored logout route
def admin_dashboard():
    if 'user_role' not in session or session['user_role'] != 'Admin':
        return redirect(url_for('dashboard'))

    
    # Get stats for dashboard
    upcoming_events = supabase.table('bookings').select('id', count='exact').eq('status','Approved').execute()
    event_data = supabase.table('bookings').select('event_type, event_date, email').eq('status', 'Approved').execute()
    events = event_data.data
    total_clients = supabase.table('users').select('id', count='exact').eq('role', 'Client').execute()
    staff_members = supabase.table('users').select('id', count='exact').eq('role', 'Staff').execute()
    
    # Calculate monthly revenue (simplified)
    revenue = Compute()
    
    # Get recent bookings
    recent_bookings = supabase.table('bookings').select('*').order('created_at', desc=True).limit(5).execute()
    
    # Get staff availability
    staff_availability = supabase.table('users').select('*').eq('role', 'Staff').execute()
    
    return render_template('admin/admin_dashboard.html', 
                          upcoming_events=upcoming_events.count,
                          total_clients=total_clients.count,
                          staff_members=staff_members.count,
                          monthly_revenue=revenue,
                          recent_bookings=recent_bookings.data if recent_bookings.data else 0,
                          staff_availability=staff_availability.data,
                          calendar_events=events,
                          logged_in=session.get('logged_in', False))

# ---------------- Staff Routing ----------------
@app.route('/staff_dashboard')  
def staff_dashboard():
    if 'user_role' not in session or session['user_role'] != 'Staff':
        return redirect(url_for('dashboard'))
    
    staff_email = session.get('email')
    if not staff_email:
        flash("User email not found in session.", "danger")
        return redirect(url_for('dashboard'))
    
    # Fetch staff user info for name display and availability
    user_response = supabase.table('users').select('first_name, last_name, availability').eq('email', staff_email).single().execute()
    staff_name = ""
    availability = None
    if user_response.data:
        first_name = user_response.data.get('first_name', '')
        last_name = user_response.data.get('last_name', '')
        availability = user_response.data.get('availability', None)
        staff_name = f"{first_name} {last_name}".strip()
    
    # Fetch staff assignments joined with bookings for event details
    assignments_response = supabase.table('staff_assignments').select('*, bookings:booking_id(id,email, package_name, event_type, event_date, start_time, end_time, location)').eq('staff_email', staff_email).execute()
    assignments = assignments_response.data if assignments_response.data else []
    
    # Fetch staff tasks joined with assignments and bookings for event details
    tasks_response = supabase.table('staff_tasks').select('*, staff_assignments!inner(staff_email, booking_id, bookings(id, event_type))').eq('staff_assignments.staff_email', staff_email).execute()
    tasks_raw = tasks_response.data if tasks_response.data else []
    
    # Flatten tasks to include event_type and status for template
    tasks = []
    completed_count = 0
    for task in tasks_raw:
        task_flat = dict(task)
        assignment = task.get('staff_assignments')
        if assignment:
            task_flat['event_type'] = None
            bookings = assignment.get('bookings')
            if bookings:
                task_flat['event_type'] = bookings.get('event_type')
        else:
            task_flat['event_type'] = None
        tasks.append(task_flat)
        if task_flat.get('status', '').lower() == 'completed':
            completed_count += 1
    
    total_tasks = len(tasks)
    completion_percentage = 0
    if total_tasks > 0:
        completion_percentage = int((completed_count / total_tasks) * 100)
    
    return render_template('staff/staff_dashboard.html', 
                           assignments=assignments,
                           tasks=tasks,
                           completion_percentage=completion_percentage,
                           staff_name=staff_name,
                           availability=availability)

# ---------------- Add Property (Placeholder) ----------------

@app.route('/add-property')
def add_property():
    return "Add Property Page - Coming Soon"
from flask import request, jsonify

# Route to add a task to an assignment
@app.route('/add_task', methods=['POST'])
def add_task():
    if 'user_role' not in session or session['user_role'] != 'Admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    assignment_id = request.form.get('assignment_id')
    task_title = request.form.get('task_title')
    task_description = request.form.get('task_description')
    due_date = request.form.get('due_date')
    
    if not assignment_id or not task_description or not due_date:
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400
    
    try:
        new_task = {
            'assignment_id': assignment_id,
            'task_title': task_title,
            'task_description': task_description,
            'due_date': due_date,
            'status': 'Pending'
        }
        response = supabase.table('staff_tasks').insert(new_task).execute()
        if response.data:
            flash("Task Added Successfully", "success")
            return redirect(url_for('staff_scheduling'))
        else:
            return jsonify({'success': False, 'message': 'Failed to add task'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Route to delete an assignment
@app.route('/delete_assignment/<int:assignment_id>', methods=['DELETE'])
def delete_assignment(assignment_id):
    if 'user_role' not in session or session['user_role'] != 'Admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        response = supabase.table('staff_assignments').delete().eq('id', assignment_id).execute()
        if response.data:
            return jsonify({'success': True, 'message': 'Assignment deleted'})
        else:
            return jsonify({'success': False, 'message': 'Failed to delete assignment'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/update_staff_availability', methods=['POST'])
def update_staff_availability():
    """
    Flask route to update the availability status of a staff member.
    Expects form data with 'staff_id' and 'availability_status'.
    """
    staff_id = request.form.get('staff_id')
    availability_status = request.form.get('availability_status')

    if not staff_id or not availability_status:
        flash("Missing staff ID or availability status.", "danger")
        return redirect(url_for('staff_scheduling'))

    try:
        response = supabase.table('users').update({"availability": availability_status}).eq("id", staff_id).execute()

        if response.data:
            flash("Availability updated successfully!", "success")
        else:
            flash("Failed to update availability.", "danger")

    except Exception as e:
        flash(f"Error updating availability: {e}", "danger")

    return redirect(url_for('staff_scheduling'))

@app.route('/edit_task', methods=['POST'])
def edit_task():
    if 'user_role' not in session or session['user_role'] != 'Admin':
        flash("Unauthorized access.", "danger")
        return redirect(url_for('staff_scheduling'))

    try:
        task_id = request.form.get('task_id')
        task_title = request.form.get('task_title')
        task_description = request.form.get('task_description')
        due_date = request.form.get('due_date')
        status = request.form.get('status')

        if not task_id or not task_title or not task_description or not due_date or not status:
            flash("All fields are required.", "danger")
            return redirect(url_for('staff_scheduling'))

        update_data = {
            'task_title': task_title,
            'task_description': task_description,
            'due_date': due_date,
            'status': status
        }

        response = supabase.table('staff_tasks').update(update_data).eq('id', task_id).execute()

        if response.data:
            flash("Task updated successfully!", "success")
        else:
            flash("Failed to update task.", "danger")

    except Exception as e:
        flash(f"An error occurred while updating task: {e}", "danger")

    return redirect(url_for('staff_scheduling'))

@app.route('/update_task_status', methods=['POST'])
def update_task_status():
    if 'user_role' not in session or session['user_role'] != 'Staff':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    data = request.json
    task_id = data.get('task_id')
    new_status = data.get('status')

    if not task_id or new_status not in ['Completed', 'Pending']:
        return jsonify({'success': False, 'message': 'Invalid data'}), 400

    try:
        response = supabase.table('staff_tasks').update({'status': new_status}).eq('id', task_id).execute()
        if response.data:
            return jsonify({'success': True, 'message': 'Task status updated'})
        else:
            return jsonify({'success': False, 'message': 'Failed to update task status'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/staff_profile')
def staff_profile():
    if 'email' not in session:
        flash("Please log in to view your profile.", "warning")
        return redirect(url_for('login'))
    user_email = session['email']
    try:
        user_response = supabase.table('users').select('*').eq('email', user_email).single().execute()
        user = user_response.data if user_response.data else {}
    except Exception as e:
        flash(f"Error loading profile: {e}", "danger")
        user = {}
    return render_template('staff/staff_profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
