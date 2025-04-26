// static/js/script.js

document.addEventListener('DOMContentLoaded', function () {
    // Initialize event calendar if it exists
   
    // Initialize dashboard calendar if it exists
    const calendarEl = document.getElementById('calendar');
    if (calendarEl) {
        initDashboardCalendar(calendarEl);
    }

    // Initialize action buttons
    // initActionButtons();

    // Initialize search functionality
    initSearch();
});



document.addEventListener('DOMContentLoaded', function () {
    const calendarEl = document.getElementById('calendar');

    // Events will be inserted dynamically by your template
    const events = window.calendarEvents || [];

    const formattedEvents = events.map(e => ({
        title: `${e.email}\n${e.event_type}`, // line break with \n (for now)
        start: e.event_date
    }));// format events to be used by calendar library

    initDashboardCalendar(calendarEl, formattedEvents);
});
function initDashboardCalendar(calendarEl, events = []) {
    if (!calendarEl) return;
    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,listWeek'
        },
        events: events,
        eventContent: function(arg) {
            const [email, type] = arg.event.title.split('\n');

            // Return custom HTML content for the event
            return {
                html: `<strong>${email}</strong><br><small>${type}</small>`
            };
        }
    });

    calendar.render();
}

// function initActionButtons() {
//     // Add click event to all action buttons
//     const actionButtons = document.querySelectorAll('.action-btn');
//     actionButtons.forEach(button => {
//         button.addEventListener('click', function (e) {
//             e.preventDefault();

//             // Create dropdown menu
//             const dropdown = document.createElement('div');
//             dropdown.className = 'action-dropdown';
//             dropdown.innerHTML = `
//                 <ul>
//                     <li><a href="#">Edit</a></li>
//                     <li><a href="#">Delete</a></li>
//                     <li><a href="#">View Details</a></li>
//                 </ul>
//             `;

//             // Position dropdown
//             const rect = button.getBoundingClientRect();
//             dropdown.style.position = 'absolute';
//             dropdown.style.top = `${rect.bottom + window.scrollY}px`;
//             dropdown.style.left = `${rect.left + window.scrollX - 100}px`;
//             dropdown.style.minWidth = '120px';
//             dropdown.style.backgroundColor = 'white';
//             dropdown.style.boxShadow = '0 2px 5px rgba(0,0,0,0.2)';
//             dropdown.style.borderRadius = '4px';
//             dropdown.style.zIndex = '1000';

//             // Style dropdown items
//             const style = document.createElement('style');
//             style.textContent = `
//                 .action-dropdown ul {
//                     list-style: none;
//                     padding: 0;
//                     margin: 0;
//                 }
//                 .action-dropdown li {
//                     padding: 0;
//                 }
//                 .action-dropdown a {
//                     display: block;
//                     padding: 8px 12px;
//                     color: #333;
//                     text-decoration: none;
//                     font-size: 14px;
//                 }
//                 .action-dropdown a:hover {
//                     background-color: #f0f5ff;
//                 }
//             `;

//             document.head.appendChild(style);
//             document.body.appendChild(dropdown);

//             // Close dropdown when clicking outside
//             const closeDropdown = function (e) {
//                 if (!dropdown.contains(e.target) && e.target !== button) {
//                     document.body.removeChild(dropdown);
//                     document.removeEventListener('click', closeDropdown);
//                 }
//             };

//             // Add delay to prevent immediate closing
//             setTimeout(() => {
//                 document.addEventListener('click', closeDropdown);
//             }, 100);
//         });
//     });
// }

function initSearch() {
    // Search functionality for tables
    const searchInputs = document.querySelectorAll('.search-box input, .search-bar input');
    searchInputs.forEach(input => {
        input.addEventListener('input', function (e) {
            const searchTerm = e.target.value.toLowerCase();
            let table;

            // Find the closest table to search in
            if (input.closest('.section-header')) {
                table = input.closest('.section-header').nextElementSibling;
            } else if (document.querySelector('.data-table')) {
                table = document.querySelector('.data-table');
            }

            if (table && table.tagName === 'TABLE') {
                const rows = table.querySelectorAll('tbody tr');

                rows.forEach(row => {
                    const text = row.textContent.toLowerCase();
                    if (text.includes(searchTerm)) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                });
            }
        });
    });
}

// Add form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;

    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            field.classList.add('error');

            // Add error message if not exists
            let errorMsg = field.nextElementSibling;
            if (!errorMsg || !errorMsg.classList.contains('error-text')) {
                errorMsg = document.createElement('div');
                errorMsg.className = 'error-text';
                errorMsg.style.color = '#ef4444';
                errorMsg.style.fontSize = '12px';
                errorMsg.style.marginTop = '4px';
                errorMsg.textContent = 'This field is required';
                field.parentNode.insertBefore(errorMsg, field.nextSibling);
            }
        } else {
            field.classList.remove('error');

            // Remove error message if exists
            const errorMsg = field.nextElementSibling;
            if (errorMsg && errorMsg.classList.contains('error-text')) {
                errorMsg.parentNode.removeChild(errorMsg);
            }
        }
    });

    return isValid;
}

// Example of form submission with validation
document.addEventListener('submit', function (e) {
    const form = e.target;

    if (form.id === 'loginForm' || form.id === 'createEventForm' || form.id === 'addUserForm') {
        if (!validateForm(form.id)) {
            e.preventDefault();
        }
    }
});

// Implement notification system
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
            <span>${message}</span>
        </div>
        <button class="close-btn">
            <i class="fas fa-times"></i>
        </button>
    `;

    // Style notification
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.backgroundColor = type === 'success' ? '#10b981' : '#ef4444';
    notification.style.color = 'white';
    notification.style.padding = '12px 16px';
    notification.style.borderRadius = '6px';
    notification.style.boxShadow = '0 2px 5px rgba(0,0,0,0.2)';
    notification.style.display = 'flex';
    notification.style.alignItems = 'center';
    notification.style.justifyContent = 'space-between';
    notification.style.minWidth = '300px';
    notification.style.zIndex = '9999';

    // Style close button
    const closeBtn = notification.querySelector('.close-btn');
    closeBtn.style.background = 'none';
    closeBtn.style.border = 'none';
    closeBtn.style.color = 'white';
    closeBtn.style.cursor = 'pointer';

    // Style notification content
    const content = notification.querySelector('.notification-content');
    content.style.display = 'flex';
    content.style.alignItems = 'center';
    content.style.gap = '8px';

    document.body.appendChild(notification);

    // Close notification on click
    closeBtn.addEventListener('click', function () {
        document.body.removeChild(notification);
    });

    // Auto-close after 5 seconds
    setTimeout(() => {
        if (document.body.contains(notification)) {
            document.body.removeChild(notification);
        }
    }, 5000);
}

// Example function to create a new event
function createEvent(eventData) {
    // This would be replaced with a real API call
    console.log('Creating event:', eventData);

    // Show success notification
    showNotification('Event created successfully!');

    // Redirect to events page
    window.location.href = '/events';
}

// Example function to add a new user
function addUser(userData) {
    // This would be replaced with a real API call
    console.log('Adding user:', userData);

    // Show success notification
    showNotification('User added successfully!');

    // Redirect to users page
    window.location.href = '/users';
}