// Career Guidance Portal - script.js

/**
 * showStep() - Ek step ko active karta hai aur baaki ko hide karta hai
 * @param {number} index - Step number (0 se 5 tak)
 */
function showStep(index) {
  // Sabhi step sections ko toggle karo
  const sections = document.querySelectorAll('.step-section');
  sections.forEach(function (section, i) {
    section.classList.toggle('active', i === index);
  });

  // Navigation buttons ko toggle karo
  const buttons = document.querySelectorAll('.nav-btn');
  buttons.forEach(function (btn, i) {
    btn.classList.toggle('active', i === index);
  });

  // Page ko top par scroll karo
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * Page load hone par pehla step active karo
 */
document.addEventListener('DOMContentLoaded', function () {
  showStep(0);
});
