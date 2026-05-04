// ===========================
// SKILL HOVER TOOLTIP
// ===========================
const skills = document.querySelectorAll('.skill');

skills.forEach(skill => {
  skill.addEventListener('mouseenter', () => {
    skill.style.transform = 'translateY(-3px)';
  });
  skill.addEventListener('mouseleave', () => {
    skill.style.transform = 'translateY(0)';
  });
});

// ===========================
// PROJECT CARD INTERACTION
// ===========================
const projects = document.querySelectorAll('.project-item');

projects.forEach(project => {
  project.addEventListener('mouseenter', () => {
    project.style.borderColor = 'rgba(0,0,0,0.15)';
  });
  project.addEventListener('mouseleave', () => {
    project.style.borderColor = '';
  });
});

// ===========================
// SCROLL REVEAL (for cards below fold)
// ===========================
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.animationPlayState = 'running';
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.card, .hero').forEach(el => {
  observer.observe(el);
});

// ===========================
// AVATAR CLICK EASTER EGG
// ===========================
const avatar = document.querySelector('.avatar');
let clickCount = 0;

avatar.addEventListener('click', () => {
  clickCount++;
  if (clickCount === 3) {
    avatar.style.background = '#185FA5';
    avatar.style.transition = 'background 0.4s ease';
    setTimeout(() => {
      avatar.style.background = '#1a1a1a';
      clickCount = 0;
    }, 1200);
  }
});

// ===========================
// SOCIAL LINK CONFIRMATION
// ===========================
document.querySelectorAll('.social-btn').forEach(btn => {
  btn.addEventListener('click', (e) => {
    const href = btn.getAttribute('href');
    // Replace placeholder URLs with actual ones before deploying
    if (href.includes('abhishekbachchan')) {
      // URLs are placeholder - update them with your real profiles
      console.log('Update your social links in index.html');
    }
  });
});
