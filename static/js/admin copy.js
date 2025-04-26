// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
  // Initialize calendar
  initCalendar();
  
  // Initialize website content
  initWebsiteContent();
  
  // Add event listeners
  addEventListeners();
});

// Initialize the calendar
function initCalendar() {
  const calendarContainer = document.getElementById('calendar');
  const currentDate = new Date();
  const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  
  // Create simple calendar view
  const calendarHTML = `
      <div class="calendar-header">
          <h3>${monthNames[currentDate.getMonth()]} ${currentDate.getFullYear()}</h3>
      </div>
      <div class="calendar-body">
          <p>Select a date to view bookings</p>
          <p class="calendar-info">No bookings for today</p>
      </div>
  `;
  
  calendarContainer.innerHTML = calendarHTML;
}

// Initialize website content
function initWebsiteContent() {
  const contentPlaceholder = document.querySelector('.content-placeholder');
  
  // Create simple content stats
  const contentHTML = `
      <div class="content-stats">
          <div class="stat-item">
              <h4>Total Pages</h4>
              <p>24</p>
          </div>
          <div class="stat-item">
              <h4>Published</h4>
              <p>18</p>
          </div>
          <div class="stat-item">
              <h4>Drafts</h4>
              <p>6</p>
          </div>
      </div>
      <div class="content-actions">
          <button class="action-btn">Add New Page</button>
          <button class="action-btn">View All Pages</button>
      </div>
  `;
  
  contentPlaceholder.innerHTML = contentHTML;
  
  // Add styles for the content stats
  const style = document.createElement('style');
  style.textContent = `
      .content-stats {
          display: flex;
          justify-content: space-around;
          margin-bottom: 20px;
      }
      
      .stat-item {
          text-align: center;
      }
      
      .stat-item h4 {
          font-size: 14px;
          color: #666;
          margin-bottom: 8px;
      }
      
      .stat-item p {
          font-size: 20px;
          font-weight: bold;
          color: #333;
      }
      
      .content-actions {
          display: flex;
          justify-content: center;
          gap: 10px;
      }
      
      .action-btn {
          padding: 8px 16px;
          background-color: #3f51b5;
          color: white;
          border: none;
          border-radius: 4px;
          cursor: pointer;
          font-size: 14px;
      }
      
      .action-btn:hover {
          background-color: #303f9f;
      }
      
      .calendar-header {
          text-align: center;
          margin-bottom: 10px;
      }
      
      .calendar-body {
          text-align: center;
      }
      
      .calendar-info {
          margin-top: 10px;
          font-style: italic;
          color: #999;
      }
  `;
  
  document.head.appendChild(style);
}

// Add event listeners
function addEventListeners() {
  // Staff availability toggle functionality
  const staffItems = document.querySelectorAll('.staff-item');
  
  staffItems.forEach(item => {
      item.addEventListener('click', function() {
          const availability = this.querySelector('.availability');
          
          if (availability.classList.contains('available')) {
              availability.classList.remove('available');
              availability.classList.add('booked');
              availability.textContent = 'Booked';
          } else if (availability.classList.contains('booked')) {
              availability.classList.remove('booked');
              availability.classList.add('lunch');
              availability.textContent = 'On Lunch';
          } else {
              availability.classList.remove('lunch');
              availability.classList.add('available');
              availability.textContent = 'Available';
          }
      });
  });
  
  // Settings button functionality
  const settingsBtn = document.querySelector('.settings-btn');
  
  settingsBtn.addEventListener('click', function() {
      alert('Settings panel would open here');