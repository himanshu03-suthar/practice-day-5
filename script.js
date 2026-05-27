// ===== CONFIG =====
const API_BASE = "http://127.0.0.1:8000";
const API_URL = `${API_BASE}/CHAT`;
const QUIZ_URL = `${API_BASE}/quiz/generate`;
const HEALTH_URL = `${API_BASE}/health`;

// ===== ELEMENTS =====
const chatMessages = document.getElementById("chatMessages");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const sendIcon = document.getElementById("sendIcon");
const loadIcon = document.getElementById("loadIcon");
const suggestions = document.getElementById("suggestions");
const statusDot = document.getElementById("statusDot");
const statusText = document.getElementById("statusText");

let isLoading = false;
let currentQuiz = null;
let userAnswers = [];

// ===== HEALTH CHECK =====
async function checkHealth() {
  try {
    const res = await fetch(HEALTH_URL);
    const data = await res.json();
    if (data.ai_configured) {
      statusText.textContent = "Online • groq Connected";
      statusDot.style.background = "#22c55e";
      statusDot.style.boxShadow = "0 0 6px #22c55e";
    } else {
      statusText.textContent = "API key missing • Add groq_API_KEY";
      statusDot.style.background = "#f59e0b";
      statusDot.style.boxShadow = "0 0 6px #f59e0b";
    }
  } catch {
    statusText.textContent = "Offline • Start server (uvicorn)";
    statusDot.style.background = "#ef4444";
    statusDot.style.boxShadow = "0 0 6px #ef4444";
  }
}

// ===== TAB SWITCH =====
function switchTab(tab) {
  document.getElementById("tabChat").classList.toggle("active", tab === "chat");
  document.getElementById("tabQuiz").classList.toggle("active", tab === "quiz");
  document.getElementById("chatPanel").classList.toggle("active", tab === "chat");
  document.getElementById("quizPanel").classList.toggle("active", tab === "quiz");
}

// ===== AUTO RESIZE =====
function autoResize(el) {
  el.style.height = "auto";
  el.style.height = Math.min(el.scrollHeight, 120) + "px";
}

function fillInput(text) {
  userInput.value = text;
  autoResize(userInput);
  userInput.focus();
  if (suggestions) suggestions.style.display = "none";
}

function handleKey(e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
}

function scrollToBottom() {
  chatMessages.scrollTo({ top: chatMessages.scrollHeight, behavior: "smooth" });
}

function createMessage(role, content) {
  const isUser = role === "user";
  const row = document.createElement("div");
  row.classList.add("msg-row", isUser ? "user-row" : "ai-row");

  const avatar = document.createElement("div");
  avatar.classList.add("avatar", isUser ? "user-av" : "ai-av");
  avatar.innerHTML = isUser ? "👤" : "◆";

  const bubble = document.createElement("div");
  bubble.classList.add("bubble", isUser ? "user-bubble" : "ai-bubble");

  if (content === "__loading__") {
    bubble.innerHTML = `<div class="typing-dots"><span></span><span></span><span></span></div>`;
  } else {
    bubble.textContent = content;
  }

  if (isUser) {
    row.appendChild(bubble);
    row.appendChild(avatar);
  } else {
    row.appendChild(avatar);
    row.appendChild(bubble);
  }

  return { row, bubble };
}

async function sendMessage() {
  const text = userInput.value.trim();
  if (!text || isLoading) return;

  if (suggestions) suggestions.style.display = "none";

  const { row: userRow } = createMessage("user", text);
  chatMessages.appendChild(userRow);

  userInput.value = "";
  userInput.style.height = "auto";

  const { row: loadRow, bubble: loadBubble } = createMessage("ai", "__loading__");
  chatMessages.appendChild(loadRow);
  scrollToBottom();
  setLoading(true);

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });

    if (!response.ok) throw new Error("Server error: " + response.status);

    const data = await response.json();
    loadBubble.innerHTML = "";
    loadBubble.textContent = data.response || "Koi response nahi mila.";
  } catch (err) {
    console.error("API Error:", err);
    loadBubble.innerHTML = "";
    loadBubble.textContent =
      "Backend se connect nahi ho paya. Server chalu hai? (uvicorn main:app --reload)";
    loadBubble.style.borderColor = "rgba(239,68,68,0.3)";
  } finally {
    setLoading(false);
    scrollToBottom();
    userInput.focus();
  }
}

function setLoading(state) {
  isLoading = state;
  sendBtn.classList.toggle("disabled", state);
  sendIcon.classList.toggle("hidden", state);
  loadIcon.classList.toggle("hidden", !state);
}

// ===== QUIZ =====
async function generateQuiz() {
  const topic = document.getElementById("quizTopic").value.trim();
  const count = parseInt(document.getElementById("quizCount").value, 10);
  const btn = document.getElementById("quizGenBtn");

  if (!topic) {
    alert("Pehle topic likho!");
    return;
  }

  btn.disabled = true;
  btn.textContent = "Generating...";

  try {
    const res = await fetch(QUIZ_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic, num_questions: count }),
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Quiz generate nahi hua");

    currentQuiz = data.questions;
    userAnswers = new Array(currentQuiz.length).fill(null);
    renderQuiz(data.topic);
  } catch (err) {
    alert("Error: " + err.message);
  } finally {
    btn.disabled = false;
    btn.textContent = "Generate Quiz";
  }
}

function renderQuiz(topic) {
  document.getElementById("quizSetup").classList.add("hidden");
  document.getElementById("quizResult").classList.add("hidden");

  const container = document.getElementById("quizQuestions");
  container.innerHTML = `<h2 class="quiz-topic-title">Topic: ${topic}</h2>`;

  currentQuiz.forEach((q, qi) => {
    const block = document.createElement("div");
    block.className = "quiz-q-block";
    block.innerHTML = `<p class="quiz-q-text">${qi + 1}. ${q.question}</p>`;

    q.options.forEach((opt, oi) => {
      const label = document.createElement("label");
      label.className = "quiz-option";
      label.innerHTML = `
        <input type="radio" name="q${qi}" value="${oi}" onchange="selectAnswer(${qi}, ${oi})" />
        <span>${opt}</span>`;
      block.appendChild(label);
    });

    container.appendChild(block);
  });

  const submitBtn = document.createElement("button");
  submitBtn.className = "quiz-gen-btn quiz-submit-btn";
  submitBtn.textContent = "Submit Answers";
  submitBtn.onclick = submitQuiz;
  container.appendChild(submitBtn);

  container.classList.remove("hidden");
}

function selectAnswer(qIndex, optionIndex) {
  userAnswers[qIndex] = optionIndex;
}

function submitQuiz() {
  if (userAnswers.includes(null)) {
    alert("Sab questions ke answers select karo!");
    return;
  }

  let correct = 0;
  currentQuiz.forEach((q, i) => {
    if (userAnswers[i] === q.answer) correct++;
  });

  document.getElementById("quizQuestions").classList.add("hidden");
  document.getElementById("quizResult").classList.remove("hidden");
  document.getElementById("resultTitle").textContent = "Quiz Complete!";
  document.getElementById("resultScore").textContent =
    `Aapne ${correct} / ${currentQuiz.length} sahi kiye (${Math.round((correct / currentQuiz.length) * 100)}%)`;
}

function resetQuiz() {
  currentQuiz = null;
  userAnswers = [];
  document.getElementById("quizTopic").value = "";
  document.getElementById("quizSetup").classList.remove("hidden");
  document.getElementById("quizQuestions").classList.add("hidden");
  document.getElementById("quizResult").classList.add("hidden");
  document.getElementById("quizQuestions").innerHTML = "";
}

// ===== INIT =====
checkHealth();
userInput.focus();
