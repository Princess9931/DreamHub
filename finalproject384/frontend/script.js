let currentMode = 'login';

function switchAuth(mode) {
  currentMode = mode;
  document.getElementById('tab-login').classList.toggle('active', mode === 'login');
  document.getElementById('tab-register').classList.toggle('active', mode === 'register');
  document.getElementById('confirm-row').classList.toggle('hidden', mode !== 'register');
  document.querySelector('.auth-submit').innerText = mode === 'login' ? 'Login करें' : 'Register करें';
  setMessage('');
}

function setMessage(text, success = true) {
  const msg = document.getElementById('auth-message');
  msg.textContent = text;
  msg.style.color = success ? '#2f855a' : '#c53030';
}

async function submitAuth(event) {
  event.preventDefault();

  const email = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value;
  const confirmPassword = document.getElementById('confirmPassword').value;

  if (!email || !password) {
    setMessage('❌ Email और Password दोनों भरें।', false);
    return;
  }

  if (currentMode === 'register' && password !== confirmPassword) {
    setMessage('❌ Password और Confirm Password match नहीं करते।', false);
    return;
  }

  if (currentMode === 'register' && password.length < 6) {
    setMessage('❌ Password कम से कम 6 characters का होना चाहिए।', false);
    return;
  }

  const endpoint = currentMode === 'login' ? '/login' : '/register';
  const baseUrl = window.location.protocol === 'file:' ? 'http://localhost:5000' : window.location.origin;
  const payload = { username: email, password };

  // Button disable during request
  const btn = document.querySelector('.auth-submit');
  btn.disabled = true;
  btn.textContent = 'Please wait...';

  try {
    const response = await fetch(`${baseUrl}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const result = await response.json();

    if (response.ok) {
      if (currentMode === 'register') {
        setMessage('✅ Registration सफल! अब Login करें।', true);
        setTimeout(() => {
          switchAuth('login');
          setMessage('✅ Register हो गए। अब Login करें।', true);
        }, 1000);
      } else {
        // Login success
        localStorage.setItem('dreamhubUser', email);
        setMessage('✅ Login सफल! Portal खुल रहा है...', true);
        setTimeout(() => {
          window.location.href = '/index.html';
        }, 900);
      }
    } else {
      // Show backend error message (e.g., "User already exists ❌")
      setMessage('❌ ' + (result.msg || 'कुछ गड़बड़ हुई, फिर से कोशिश करें।'), false);
    }
  } catch (err) {
    setMessage('❌ Server से connect नहीं हो पाया। Backend चालू है?', false);
  } finally {
    btn.disabled = false;
    btn.textContent = currentMode === 'login' ? 'Login करें' : 'Register करें';
  }
}
