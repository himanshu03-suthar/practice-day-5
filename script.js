// ===== CONFIG =====
console.log("JavaScript Connected");

const API_URL = "http://127.0.0.1:8000/CHAT";

// ===== ELEMENTS =====
const chatMessages = document.getElementById("chatMessages");
const userInput    = document.getElementById("userInput");
const sendBtn      = document.getElementById("sendBtn");
const sendIcon     = document.getElementById("sendIcon");
const loadIcon     = document.getElementById("loadIcon");
const suggestions  = document.getElementById("suggestions");

let isLoading = false;

// ===== AUTO RESIZE TEXTAREA =====
function autoResize(el) {
  el.style.height = "auto";
  el.style.height = Math.min(el.scrollHeight, 120) + "px";
}

// ===== FILL INPUT FROM SUGGESTION CHIP =====
function fillInput(text) {
  userInput.value = text;
  autoResize(userInput);
  userInput.focus();
  // Hide suggestions once user picks one
  if (suggestions) suggestions.style.display = "none";
}

// ===== ENTER KEY HANDLER =====
function handleKey(e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
}

// ===== SCROLL TO BOTTOM =====
function scrollToBottom() {
  chatMessages.scrollTo({
    top: chatMessages.scrollHeight,
    behavior: "smooth",
  });
}

// ===== CREATE MESSAGE BUBBLE =====
function createMessage(role, content) {
  const isUser = role === "user";

  const row = document.createElement("div");
  row.classList.add("msg-row", isUser ? "user-row" : "ai-row");

  // Avatar
  const avatar = document.createElement("div");
  avatar.classList.add("avatar", isUser ? "user-av" : "ai-av");
  avatar.innerHTML = isUser ? "👤" : "◆";

  // Bubble
  const bubble = document.createElement("div");
  bubble.classList.add("bubble", isUser ? "user-bubble" : "ai-bubble");

  if (content === "__loading__") {
    bubble.innerHTML = `
      <div class="typing-dots">
        <span></span><span></span><span></span>
      </div>`;
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

// ===== SEND MESSAGE =====
async function sendMessage() {
  const text = userInput.value.trim();
  if (!text || isLoading) return;

  // Hide suggestions on first real message
  if (suggestions) suggestions.style.display = "none";

  // --- Add user message ---
  const { row: userRow } = createMessage("user", text);
  chatMessages.appendChild(userRow);

  // --- Clear input ---
  userInput.value = "";
  userInput.style.height = "auto";

  // --- Add loading bubble ---
  const { row: loadRow, bubble: loadBubble } = createMessage("ai", "__loading__");
  chatMessages.appendChild(loadRow);
  scrollToBottom();

  // --- Set loading state ---
  setLoading(true);

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });

    if (!response.ok) throw new Error("Server error: " + response.status);

    const data = await response.json();
    const aiReply = data.response || "Koi response nahi mila.";

    console.log(data);

    // Replace loading dots with actual reply
    loadBubble.innerHTML = "";
    loadBubble.textContent = aiReply;

  } catch (err) {
    console.error("API Error:", err);
    loadBubble.innerHTML = "";
    loadBubble.textContent =
      "⚠️ Backend se connect nahi ho paya. " +
      "FastAPI server chalu hai? (localhost:8000)";
    loadBubble.style.borderColor = "rgba(239,68,68,0.3)";
  } finally {
    setLoading(false);
    scrollToBottom();
    userInput.focus();
  }
}

// ===== TOGGLE LOADING STATE =====
function setLoading(state) {
  isLoading = state;
  if (state) {
    sendBtn.classList.add("disabled");
    sendIcon.classList.add("hidden");
    loadIcon.classList.remove("hidden");
  } else {
    sendBtn.classList.remove("disabled");
    sendIcon.classList.remove("hidden");
    loadIcon.classList.add("hidden");
  }
}

// ===== INIT =====
userInput.focus();
