function getLoggedInUser() {
  return localStorage.getItem('dreamhubUser');
}

function updateDashboard() {
  const user = getLoggedInUser();
  const welcome = document.getElementById('dashboard-welcome');
  if (user) {
    welcome.textContent = `Hello, ${user}! Ready to continue your career path?`;
  } else {
    welcome.textContent = 'You are not logged in. Please login first.';
    document.getElementById('btn-continue').disabled = true;
  }
}

function logout() {
  localStorage.removeItem('dreamhubUser');
  window.location.href = './login.html';
}

function goHome() {
  window.location.href = '../index.html';
}

document.addEventListener('DOMContentLoaded', updateDashboard);
