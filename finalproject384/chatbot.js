
let chatHistory = [];

// ─── Local keyword-based fallback answers ──────────────────────────────────
const LOCAL_ANSWERS = [
  {
    keywords: ['10th', 'दसवीं', '10वीं', 'matric', 'ssc', 'board'],
    answer: '10वीं के बाद आपके पास कई विकल्प हैं:<br><br>🔬 <b>Science (11th-12th)</b> → JEE/NEET → Engineering/Medical<br>📊 <b>Commerce</b> → CA, CS, MBA, Banking<br>📚 <b>Arts</b> → UPSC, Law, Teaching<br>🔧 <b>ITI (1-2 साल)</b> → जल्दी नौकरी<br>⚙️ <b>Polytechnic Diploma (3 साल)</b> → Technical jobs<br><br>अपनी रुचि के अनुसार चुनें! 🎯'
  },
  {
    keywords: ['engineering', 'इंजीनियरिंग', 'btech', 'b.tech', 'jee', 'iit'],
    answer: 'Engineering करने के लिए:<br><br>1️⃣ 11th-12th में <b>Physics, Chemistry, Math</b> पढ़ें<br>2️⃣ <b>JEE Main</b> (NIT/IIIT) या <b>JEE Advanced</b> (IIT) exam दें<br>3️⃣ या State CET दें (State Engineering Colleges)<br>4️⃣ B.Tech <b>4 साल</b> का course है<br><br>💡 Popular branches: CSE, Mechanical, Civil, Electrical'
  },
  {
    keywords: ['medical', 'mbbs', 'doctor', 'डॉक्टर', 'neet', 'biology'],
    answer: 'Medical/MBBS के लिए:<br><br>1️⃣ 11th-12th में <b>Physics, Chemistry, Biology</b> पढ़ें<br>2️⃣ <b>NEET-UG</b> exam दें (हर साल May में)<br>3️⃣ Government Medical College में <b>MBBS 5.5 साल</b><br><br>💡 NEET बहुत competitive है — 1 साल पहले से तैयारी शुरू करें'
  },
  {
    keywords: ['government', 'govt', 'सरकारी', 'naukri', 'नौकरी', 'job'],
    answer: 'सरकारी नौकरी के लिए education के अनुसार:<br><br>🎓 <b>10वीं बाद:</b> Army GD, RRB Group D, SSC MTS<br>🎓 <b>12वीं बाद:</b> SSC CHSL, IBPS Clerk, Air Force<br>🎓 <b>Graduation बाद:</b> SSC CGL, IBPS PO, Sub-Inspector<br>🎓 <b>Post Graduation:</b> UPSC IAS/IPS, RBI Grade B<br><br>📌 Current Affairs + Math/Reasoning strong करें!'
  },
  {
    keywords: ['upsc', 'ias', 'ips', 'civil service', 'collector'],
    answer: 'UPSC Civil Services के बारे में:<br><br>✅ <b>Eligibility:</b> Any Graduation (min. 21 years)<br>✅ <b>Exam Pattern:</b> Prelims → Mains → Interview<br>✅ <b>Posts:</b> IAS (Collector), IPS (SP), IFS (Embassy)<br>✅ <b>Salary:</b> ₹56,100 – ₹2,50,000/माह + perks<br><br>💡 कम से कम <b>2-3 साल की</b> dedicated preparation चाहिए। NCERT से शुरू करें।'
  },
  {
    keywords: ['ssc', 'cgl', 'chsl', 'mts', 'staff selection'],
    answer: 'SSC (Staff Selection Commission) exams:<br><br>📋 <b>SSC MTS</b> → 10वीं बाद | ₹18,000-25,000/माह<br>📋 <b>SSC CHSL</b> → 12वीं बाद | ₹19,900-63,200/माह<br>📋 <b>SSC CGL</b> → Graduation बाद | ₹25,500-1,51,100/माह<br>📋 <b>SSC JE</b> → Diploma/Engineering | Technical posts<br><br>🌐 Official site: ssc.nic.in'
  },
  {
    keywords: ['bank', 'banking', 'ibps', 'sbi', 'बैंक', 'clerk', 'po'],
    answer: 'Banking Exams की जानकारी:<br><br>🏦 <b>IBPS Clerk</b> → 12वीं बाद | ₹11,765-31,540/माह<br>🏦 <b>IBPS PO</b> → Graduation | ₹52,000-95,000/माह<br>🏦 <b>SBI PO/Clerk</b> → Graduation | बड़ा package<br>🏦 <b>RBI Grade B</b> → Graduation 60%+ | ~₹1 Lakh CTC<br><br>🌐 Official: ibps.in | sbi.co.in'
  },
  {
    keywords: ['railway', 'rrb', 'रेलवे', 'ntpc', 'group d', 'alp'],
    answer: 'Railway (RRB) Exams:<br><br>🚂 <b>RRB Group D</b> → 10वीं बाद | ₹18,000-35,000/माह<br>🚂 <b>RRB NTPC</b> → 12वीं/Graduation | ₹19,900-35,400/माह<br>🚂 <b>RRB ALP</b> → ITI/Diploma | Loco Pilot<br>🚂 <b>RRB JE</b> → Diploma/Degree | ₹35,400/माह<br><br>🌐 Official: indianrailways.gov.in'
  },
  {
    keywords: ['iti', 'industrial training', 'electrician', 'fitter', 'welder'],
    answer: 'ITI (Industrial Training Institute) के बारे में:<br><br>⏱️ <b>Duration:</b> 6 महीने से 2 साल<br>📚 <b>Eligibility:</b> 8वीं / 10वीं पास<br><br>Popular Trades:<br>⚡ Electrician | 🔧 Fitter | 🔩 Turner | 💻 COPA<br>🔨 Welder | 🚗 Mechanic (MV) | 🪠 Plumber<br><br>✅ ITI के बाद RRB ALP, PSU Apprentice, Private jobs मिलती हैं'
  },
  {
    keywords: ['diploma', 'polytechnic', 'डिप्लोमा'],
    answer: 'Polytechnic Diploma के बारे में:<br><br>⏱️ <b>Duration:</b> 3 साल (10वीं के बाद)<br>📚 <b>Eligibility:</b> 10वीं Math & Science<br><br>Popular Branches: Civil, Mechanical, Electrical, CS, Electronics<br><br>💼 <b>Jobs:</b> RRB JE, PSU Technician, State PWD/JE<br>🎓 <b>Bonus:</b> Diploma के बाद <b>B.Tech 2nd year</b> में Lateral Entry!'
  },
  {
    keywords: ['commerce', 'कॉमर्स', 'ca', 'chartered', 'accountant', 'cs', 'mba'],
    answer: 'Commerce Stream के career options:<br><br>📊 <b>CA (Chartered Accountant)</b> → Finance, Tax, Audit<br>📋 <b>CS (Company Secretary)</b> → Corporate Law<br>💼 <b>MBA</b> → Management, Marketing, HR<br>🏦 <b>Banking</b> → IBPS PO/Clerk, SBI<br>📈 <b>Stock Market</b> → Financial Analyst<br><br>💡 B.Com या BBA के बाद MBA करना popular choice है'
  },
  {
    keywords: ['arts', 'humanities', 'आर्ट्स', 'ba', 'history', 'geography'],
    answer: 'Arts/Humanities stream के career options:<br><br>🎯 <b>UPSC/IAS</b> → Arts students को बड़ा फायदा<br>⚖️ <b>Law (LLB)</b> → Lawyer, Judge बनें<br>📖 <b>Teaching</b> → TET/CTET → Govt. Teacher<br>📰 <b>Journalism</b> → Media, News Channels<br>🌍 <b>Social Work</b> → NGO, Government Schemes<br><br>💡 Arts stream बहुत underrated है — UPSC में सबसे ज्यादा IAS Arts से!'
  },
  {
    keywords: ['science', 'साइंस', 'pcm', 'pcb', '11th', '12th'],
    answer: 'Science Stream (11th-12th) के बारे में:<br><br>🔬 <b>PCM (Physics+Chemistry+Math)</b><br>→ Engineering (JEE), Architecture (NATA), NDA<br><br>🧬 <b>PCB (Physics+Chemistry+Biology)</b><br>→ MBBS (NEET), Pharmacy, Nursing, BSc<br><br>🔭 <b>PCMB (सभी चारों)</b><br>→ सभी विकल्प खुले रहते हैं<br><br>💡 Science से Commerce/Arts में जा सकते हो, reverse नहीं!'
  },
  {
    keywords: ['nda', 'army', 'navy', 'air force', 'defence', 'military', 'soldier'],
    answer: 'Defence (Army/Navy/Air Force) में career:<br><br>🪖 <b>NDA</b> → 10वीं+12वीं Science | Officer बनें<br>🪖 <b>Army Soldier GD</b> → 10वीं बाद (17.5-21 साल)<br>✈️ <b>Airmen Group X/Y</b> → 12वीं बाद<br>⚓ <b>Navy Sailor</b> → 10वीं/12वीं बाद<br>🛡️ <b>CDS</b> → Graduation बाद | Commissioned Officer<br><br>Salary: ₹21,700 – ₹56,100+ (rank अनुसार)'
  },
  {
    keywords: ['gate', 'mtech', 'm.tech', 'psu', 'research'],
    answer: 'GATE & M.Tech के बारे में:<br><br>📝 <b>GATE</b> → B.Tech के बाद दें<br>🎓 <b>M.Tech/ME</b> → 2 साल | IIT/NIT में admission<br>🏭 <b>PSU Jobs</b> → GATE score से BHEL, NTPC, ONGC, GAIL में job<br>🔬 <b>Research</b> → DRDO, ISRO, CSIR में Scientist<br><br>💰 GATE से PSU salary: ₹50,000 – ₹1,00,000+/माह'
  },
  {
    keywords: ['hello', 'hi', 'hii', 'हेलो', 'नमस्ते', 'namaste', 'hey'],
    answer: 'नमस्ते! 👋 मैं <b>Career Guide AI</b> हूँ।<br><br>मैं आपकी मदद कर सकता हूँ:<br>📚 Education path चुनने में<br>🎯 Entrance exams की जानकारी में<br>💼 Government job preparation में<br>🏫 Stream selection में<br><br>कोई भी सवाल पूछें! जैसे: <i>"10th के बाद क्या करें?"</i>'
  },
  {
    keywords: ['salary', 'वेतन', 'पैसा', 'income', 'pay'],
    answer: 'अलग-अलग सरकारी jobs की salary:<br><br>💰 Army Soldier: ₹21,700/माह<br>💰 SSC MTS: ₹18,000-25,000/माह<br>💰 RRB Group D: ₹18,000-35,000/माह<br>💰 SSC CHSL: ₹19,900-63,200/माह<br>💰 IBPS PO: ₹52,000-95,000/माह<br>💰 SSC CGL: ₹25,500-1,51,100/माह<br>💰 IAS: ₹56,100-2,50,000/माह<br><br>+ DA, HRA, TA जैसे भत्ते अलग से!'
  }
];

function openChatbot() {
  // ── Login Guard: Chatbot ke liye login zaroori hai ──
  const loggedInUser = localStorage.getItem('dreamhubUser');
  if (!loggedInUser) {
    showLoginToast();
    return;
  }

  document.getElementById('chatbot-modal').classList.remove('hidden');
  document.getElementById('user-input').focus();

  if (chatHistory.length === 0) {
    addMessage('नमस्ते <b>' + loggedInUser + '</b>! 🎓 मैं <b>Career Guide AI</b> हूँ।<br>Education और career के बारे में कोई भी सवाल पूछें!<br><br>जैसे: <i>10th के बाद क्या करें, Engineering कैसे करें, UPSC क्या है...</i>', 'ai');
  }
}

function showLoginToast() {
  // Remove existing toast if any
  const existing = document.getElementById('login-toast');
  if (existing) existing.remove();

  const toast = document.createElement('div');
  toast.id = 'login-toast';
  toast.innerHTML = `
    <div style="
      position:fixed; top:50%; left:50%; transform:translate(-50%,-50%);
      background:white; border-radius:20px; padding:2rem 2.5rem;
      box-shadow:0 20px 60px rgba(0,0,0,0.3); z-index:99999;
      text-align:center; max-width:360px; width:90%;
      animation: toastPop 0.3s ease-out;
    ">
      <div style="font-size:3rem;margin-bottom:1rem;">🔐</div>
      <h3 style="color:#1a365d;margin:0 0 0.5rem;font-size:1.3rem;">Login Required</h3>
      <p style="color:#4a5568;margin:0 0 1.5rem;font-size:0.95rem;line-height:1.6;">
        Career Guide Chatbot use करने के लिए<br>पहले <b>Login</b> करना होगा।
      </p>
      <div style="display:flex;gap:0.8rem;justify-content:center;">
        <button onclick="window.location.href='/frontend/login.html'" style="
          background:linear-gradient(135deg,#667eea,#764ba2);color:white;
          border:none;padding:0.8rem 1.8rem;border-radius:999px;
          font-weight:700;cursor:pointer;font-size:0.95rem;
        ">Login / Register</button>
        <button onclick="document.getElementById('login-toast').remove()" style="
          background:#f7fafc;color:#4a5568;border:1px solid #e2e8f0;
          padding:0.8rem 1.4rem;border-radius:999px;
          font-weight:600;cursor:pointer;font-size:0.95rem;
        ">Cancel</button>
      </div>
    </div>
    <div onclick="document.getElementById('login-toast').remove()" style="
      position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:99998;
    "></div>
  `;
  document.body.appendChild(toast);
}


function closeChatbot() {
  document.getElementById('chatbot-modal').classList.add('hidden');
}

function addMessage(text, sender) {
  const messagesDiv = document.getElementById('chatbot-messages');
  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${sender}`;
  messageDiv.innerHTML = `<div class="message-bubble">${text}</div>`;
  messagesDiv.appendChild(messageDiv);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;

  chatHistory.push({ text, sender, timestamp: new Date() });
}

function removeLastMessage() {
  const messages = document.querySelectorAll('.message');
  if (messages.length > 0) {
    messages[messages.length - 1].remove();
    chatHistory.pop();
  }
}

// Search database Q&A via backend
async function searchDatabaseQA(query) {
  try {
    const response = await fetch('/search-qa', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query })
    });
    const data = await response.json();
    if (data.found && data.results.length > 0) {
      return data.results[0].answer;
    }
    return null;
  } catch (error) {
    return null; // Backend not running, skip silently
  }
}

// Smart local keyword matching
function searchLocalQA(query) {
  const q = query.toLowerCase();
  for (const item of LOCAL_ANSWERS) {
    if (item.keywords.some(kw => q.includes(kw.toLowerCase()))) {
      return item.answer;
    }
  }
  return null;
}

// Try Groq API (14,400 free requests/day)
async function askGemini(message) {
  try {
    const response = await fetch(GROQ_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${GROQ_API_KEY}`
      },
      body: JSON.stringify({
        model: 'llama-3.1-8b-instant',
        messages: [
          {
            role: 'system',
            content: 'You are a Career Guide AI for Indian students. Answer questions about education paths, government jobs, entrance exams, and career options. Be concise (2-3 sentences). Reply in Hindi or English based on user preference.'
          },
          {
            role: 'user',
            content: message
          }
        ],
        max_tokens: 250,
        temperature: 0.7
      })
    });
    const data = await response.json();
    if (data.choices && data.choices[0]) {
      return data.choices[0].message.content;
    }
    return null;
  } catch (e) {
    return null;
  }
}

async function sendMessage() {
  const input = document.getElementById('user-input');
  const message = input.value.trim();
  if (!message) return;

  addMessage(message, 'user');
  input.value = '';
  addMessage('सोच रहा हूँ... 💭', 'ai');

  // Step 1: Database Q&A (backend)
  const dbAnswer = await searchDatabaseQA(message);
  if (dbAnswer) {
    removeLastMessage();
    addMessage(dbAnswer, 'ai');
    saveChatToDatabase(message, dbAnswer);
    return;
  }

  // Step 2: Gemini API (if quota available)
  const geminiAnswer = await askGemini(message);
  if (geminiAnswer) {
    removeLastMessage();
    addMessage(geminiAnswer, 'ai');
    saveChatToDatabase(message, geminiAnswer);
    return;
  }

  // Step 3: Local smart keyword matching
  const localAnswer = searchLocalQA(message);
  if (localAnswer) {
    removeLastMessage();
    addMessage(localAnswer, 'ai');
    saveChatToDatabase(message, localAnswer);
    return;
  }

  // Step 4: Fallback
  removeLastMessage();
  addMessage(
    'मुझे इस सवाल का जवाब नहीं मिला। 😕<br><br>कृपया इन topics पर सवाल पूछें:<br>• <b>10th/12th के बाद क्या करें</b><br>• <b>Engineering / Medical कैसे करें</b><br>• <b>Government job (SSC, UPSC, Railway)</b><br>• <b>ITI / Diploma / Commerce / Arts</b><br>• <b>Bank / Army / NDA</b>',
    'ai'
  );
}

async function saveChatToDatabase(question, answer) {
  const user = localStorage.getItem('dreamhubUser') || 'anonymous';
  try {
    await fetch('/save-chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: user, question, answer, timestamp: new Date().toISOString() })
    });
  } catch (e) { /* silent fail */ }
}

// Close modal on backdrop click
document.addEventListener('click', function(event) {
  const modal = document.getElementById('chatbot-modal');
  if (event.target === modal) closeChatbot();
});
