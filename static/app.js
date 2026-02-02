let history = [];

function add(role, text) {
    const chat = document.getElementById("chat");
    const div = document.createElement("div");
    div.className = "msg";
    div.innerHTML = `<b>${role}:</b> ${escapeHtml(text)}`;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

function escapeHtml(text) {
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
}

async function send(textFromSuggestion = null) {
    const input = document.getElementById("input");
    const text = (textFromSuggestion ?? input.value).trim();
    if (!text) return;

    // UI: user
    add("user", text);
    input.value = "";

    // history: user
    history.push({ role: "user", content: text });

    // ===== CHAT =====
    let assistantAnswer = "";
    try {
        const chatResp = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                user_input: text,
                chat_history: history
            })
        });

        const chatData = await chatResp.json();
        assistantAnswer = chatData.answer || "";

    } catch {
        assistantAnswer = "Ошибка при получении ответа фармацевта.";
    }

    // UI: assistant
    add("assistant", assistantAnswer);

    // history: assistant
    history.push({ role: "assistant", content: assistantAnswer });

    // ===== SUGGESTIONS (ПОСЛЕ CHAT) =====
    try {
        const suggResp = await fetch("/suggestions", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                user_input: text,
                chat_history: history
            })
        });

        const suggData = await suggResp.json();
        renderSuggestions(suggData.options || []);

    } catch {
        renderSuggestions([]);
    }
}

function renderSuggestions(options) {
    const box = document.getElementById("suggestions");
    box.innerHTML = "";

    options.forEach(option => {
        const btn = document.createElement("button");
        btn.className = "suggestion-btn";
        btn.textContent = option;
        btn.onclick = () => send(option);
        box.appendChild(btn);
    });
}
