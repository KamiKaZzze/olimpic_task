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

/* ===== ЧАТ ===== */

async function send(textFromSuggestion = null) {
    const input = document.getElementById("input");
    const text = (textFromSuggestion ?? input.value).trim();
    if (!text) return;

    add("user", text);
    input.value = "";

    history.push({ role: "user", content: text });

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
        assistantAnswer = "Ошибка при получении ответа ассистента.";
    }

    add("assistant", assistantAnswer);
    history.push({ role: "assistant", content: assistantAnswer });

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

/* ===== ВАЛИДАЦИЯ ФЛАГА ===== */

async function validateFlag() {
    const input = document.getElementById("flag-input");
    const resultBox = document.getElementById("flag-result");

    const flag = input.value.trim();
    if (!flag) return;

    try {
        const resp = await fetch("/validate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ flag })
        });

        if (resp.status === 200) {
            resultBox.innerHTML = `
                <div class="flag-success">
                    ✔ Флаг принят!
                </div>`;
        } else {
            resultBox.innerHTML = `
                <div class="flag-error">
                    ✖ Неверный флаг
                </div>`;
        }
    } catch {
        resultBox.innerHTML = `
            <div class="flag-error">
                Ошибка проверки
            </div>`;
    }
}

/* ===== ENTER ===== */

document.addEventListener("DOMContentLoaded", function () {
    const chatInput = document.getElementById("input");
    const flagInput = document.getElementById("flag-input");

    chatInput.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            send();
        }
    });

    flagInput.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            validateFlag();
        }
    });
});