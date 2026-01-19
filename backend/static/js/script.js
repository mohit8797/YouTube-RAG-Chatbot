// const API_BASE = "http://127.0.0.1:8000";

// const processBtn = document.getElementById("processBtn");
// const sendBtn = document.getElementById("sendBtn");


// // ---------------- PAGE 1: PROCESS VIDEO ----------------

// if (processBtn) {
//     processBtn.addEventListener("click", async () => {
//         const url = document.getElementById("videoUrl").value;
//         const status = document.getElementById("status");

//         if (!url) {
//             alert("Please paste a YouTube link");
//             return;
//         }

//         status.innerText = "Processing video... ⏳";

//         try {
//             const res = await fetch(`${API_BASE}/process_video`, {
//                 method: "POST",
//                 headers: { "Content-Type": "application/json" },
//                 body: JSON.stringify({ url: url })
//             });

//             const data = await res.json();

//             if (!res.ok) {
//                 throw new Error(data.detail || "Processing failed");
//             }

//             localStorage.setItem("yt_url", url);
//             status.innerText = "Video processed! Redirecting... ✅";

//             setTimeout(() => {
//                 window.location.href = "/chat";
//             }, 800);

//         } catch (err) {
//             console.error(err);
//             status.innerText = "Error: " + err.message;
//         }
//     });
// }


// // ---------------- PAGE 2: CHAT ----------------

// if (sendBtn) {
//     const url = localStorage.getItem("yt_url");

//     const videoId = extractVideoId(url);
//     document.getElementById("ytPlayer").src =
//         `https://www.youtube.com/embed/${videoId}`;

//     sendBtn.addEventListener("click", sendMessage);
// }


// function extractVideoId(url) {
//     if (!url) return "";
//     if (url.includes("youtu.be")) {
//         return url.split("/").pop();
//     }
//     if (url.includes("watch?v=")) {
//         return url.split("watch?v=")[1].split("&")[0];
//     }
//     return "";
// }


// async function sendMessage() {
//     const input = document.getElementById("questionInput");
//     const msg = input.value;

//     if (!msg) return;

//     addMessage(msg, "user");
//     input.value = "";

//     addMessage("Thinking... 🤔", "bot");

//     try {
//         const res = await fetch(`${API_BASE}/chat`, {
//             method: "POST",
//             headers: { "Content-Type": "application/json" },
//             body: JSON.stringify({ question: msg })
//         });

//         const data = await res.json();

//         if (!res.ok) {
//             throw new Error(data.detail || "Chat failed");
//         }

//         removeLastBotMessage();
//         addMessage(data.answer, "bot");

//     } catch (err) {
//         console.error(err);
//         removeLastBotMessage();
//         addMessage("Error: " + err.message, "bot");
//     }
// }


// function addMessage(text, sender) {
//     const div = document.createElement("div");
//     div.className = sender === "user" ? "msg-user" : "msg-bot";
//     div.innerText = text;

//     const box = document.getElementById("messages");
//     box.appendChild(div);
//     box.scrollTop = box.scrollHeight;
// }


// function removeLastBotMessage() {
//     const msgs = document.getElementById("messages");
//     if (msgs.lastChild) msgs.removeChild(msgs.lastChild);
// }

const messagesDiv = document.getElementById("messages");
const sendBtn = document.getElementById("sendBtn");
const input = document.getElementById("questionInput");
const ytPlayer = document.getElementById("ytPlayer");

const urlParams = new URLSearchParams(window.location.search);
const videoId = urlParams.get("v");

if (videoId) {
    ytPlayer.src = `https://www.youtube.com/embed/${videoId}`;
}

function addMessage(text, sender) {
    const div = document.createElement("div");
    div.classList.add("message", sender);
    div.innerText = text;
    messagesDiv.appendChild(div);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

sendBtn.onclick = askQuestion;
input.addEventListener("keypress", e => {
    if (e.key === "Enter") askQuestion();
});

async function askQuestion() {
    const question = input.value.trim();
    if (!question) return;

    addMessage(question, "user");
    input.value = "";

    const loading = document.createElement("div");
    loading.classList.add("message", "bot");
    loading.innerText = "Thinking...";
    messagesDiv.appendChild(loading);

    try {
        const res = await fetch("http://127.0.0.1:8000/ask", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({question})
        });

        const data = await res.json();
        loading.remove();
        addMessage(data.answer, "bot");

    } catch (err) {
        loading.remove();
        addMessage("Error getting response", "bot");
    }
}
