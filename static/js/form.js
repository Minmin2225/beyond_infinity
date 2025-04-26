$(document).ready(function () {
  // Handle input field interactions
  $('.form input, .form textarea').on('keyup blur focus', function (e) {
      var $this = $(this);
      var label = $this.siblings('label'); // Use siblings instead of prev()

      if (e.type === 'keyup') {
          if ($this.val() === '') {
              label.removeClass('active highlight');
          } else {
              label.addClass('active highlight');
          }
      } else if (e.type === 'blur') {
          if ($this.val() === '') {
              label.removeClass('active highlight');
          } else {
              label.removeClass('highlight');
          }
      } else if (e.type === 'focus') {
          if ($this.val() !== '') {
              label.addClass('highlight');
          }
      }
  });

  // Tab switching for login & register forms
  $('.tab a').on('click', function (e) {
      e.preventDefault();

      $(this).parent().addClass('active');
      $(this).parent().siblings().removeClass('active');

      var target = $(this).attr('href');

      $('.tab-content > div').not(target).hide();
      $(target).fadeIn(600);
  });

  // Show/Hide Password
  $('.toggle-password').on('click', function () {
      var passwordField = $(this).siblings('input');
      var type = passwordField.attr('type') === 'password' ? 'text' : 'password';
      passwordField.attr('type', type);

      // Change eye icon
      $(this).toggleClass('fa-eye fa-eye-slash');
  });
});

// Log form submission
document.querySelector("form").addEventListener("submit", function(event) {
  console.log("Form submitted");
});

// Save scroll position on scroll
window.addEventListener('scroll', function() {
    sessionStorage.setItem('scrollPosition', window.scrollY);
});

// Restore scroll position on page load
window.addEventListener('load', function() {
    const scrollPosition = sessionStorage.getItem('scrollPosition');
    if (scrollPosition) {
        window.scrollTo(0, parseInt(scrollPosition));
    }
});
