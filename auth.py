from flask import Flask, render_template, request, session, redirect, url_for, flash
from supabase import create_client, Client

# Supabase Configuration
SUPABASE_URL = "https://crccujnpdndpturklluu.supabase.co"  # Replace with your Supabase URL
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNyY2N1am5wZG5kcHR1cmtsbHV1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ3MTQ4NjEsImV4cCI6MjA2MDI5MDg2MX0.T5S3MlekwzmN6vZHUtIRq-UJnHOd3QComFBf-cT3Ae4"  # Replace with your Supabase API Key

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------- Login Route ----------------
def login():
    data = request.form
    email = data['email']
    password = data['password']

    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})

        if response.user:
            session['logged_in'] = True
            session['email'] = email  
            # Retrieve user profile information
            user_profile = supabase.table("users").select("first_name, last_name, phone, role").eq("email", email).execute()
            if user_profile.data:
                session['first_name'] = user_profile.data[0]['first_name']
                session['last_name'] = user_profile.data[0]['last_name']
                session['user_role'] = user_profile.data[0]['role']
                session['phone'] = user_profile.data[0]['phone']
                if session['user_role'] == 'Admin':
                    flash("Login successful!", "success")            
                    return redirect(url_for('admin_dashboard'))
                elif session['user_role'] == 'Staff':
                    flash("Login successful!", "success")            
                    return redirect(url_for('staff_dashboard'))
                else:
                    flash("Login Admin successful!", "success")            
                    return redirect(url_for('index'))

        else:
            if session['user_role'] != 'Admin':
                flash("Invalid password. Please try again.", "danger")
                return redirect(url_for('register'))
            else:
                flash("Invalid password. Please try again.", "danger")
                return redirect(url_for('admin_login'))

    except Exception as e:
        flash("An error occurred: " + str(e), "danger")
        return redirect(url_for('register'))


# ---------------- Signup Route ----------------
def signup():
    data = request.form
    email = data['email']
    password = data['password']
    role = data.get('role', 'Client')
    first_name = data.get('first_name', '')
    last_name = data.get('last_name', '')
    phone = data.get('phone', '')  # Added phone number retrieval


    try:
        # Register the user in Supabase Auth
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

        # Check if signup was successful
        if response and response.user:
            user_id = response.user.id  # Corrected way to get user ID

            # Insert user details into 'users' table
            profile_data = {
                "id": user_id,  # Ensure your table uses 'id' as the primary key
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "phone": phone,  # Added phone number to profile data
                "role": role
            }

            # Execute the insert query properly
            insert_response = supabase.table("users").insert(profile_data).execute()

            # Check if insertion was successful
            if insert_response.data:
                if session['user_role'] == 'Admin':
                    flash("User Successfully Created", "success")
                    return redirect('users_management')
                flash("Signup successful! Please check your email to verify your account.", "success")
                return redirect(url_for('register'))
            else:
                flash("Failed to create profile. Please try again.", "danger")
                return redirect(url_for('register'))

        else:
            flash("Signup failed. The email address is already registered.", "danger")

            return redirect(url_for('register'))

    except Exception as e:
        flash("An error occurred: " + str(e), "danger")
        return redirect(url_for('register'))


# ---------------- Update Profile Route ----------------
def update_profile():
    data = request.form
    first_name = data['first_name']
    last_name = data['last_name']
    phone = data['phone']
    email = session['email']  # Assuming the email is stored in the session

    try:
        # Update the user's profile in the 'users' table
        profile_data = {
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone
        }

        update_response = supabase.table("users").update(profile_data).eq("email", email).execute()

        if update_response.data:            
            # Update session variables with new profile information
            session['first_name'] = first_name
            session['last_name'] = last_name
            session['phone'] = phone

            flash("Profile updated successfully!", "success")
        else:
            flash("Failed to update profile. Please try again.", "danger")

        return redirect(url_for('dashboard'))

    except Exception as e:
        flash("An error occurred: " + str(e), "danger")
        return redirect(url_for('dashboard'))

def logout():
    session.clear()
    flash("Logged out successfully!", "info")
    return redirect(url_for('index'))


def Compute():
    # 1. Get all completed bookings
    completed_bookings = supabase.table('bookings').select('package_name').eq('status', 'Completed').execute()
    # 2. Extract package names from bookings
    package_names = [booking['package_name'] for booking in completed_bookings.data]
    # 3. Fetch all services (to get their prices)
    services_data = supabase.table('services').select('package_name, price').in_('package_name', package_names).execute()
    # 4. Create a dictionary: package_name -> price
    package_prices = {service['package_name']: service['price'] for service in services_data.data}
    # 5. Calculate total revenue
    total_revenue = sum(package_prices.get(pkg, 0) for pkg in package_names)
    formatted_revenue = f"{total_revenue:,.2f}"

    return formatted_revenue