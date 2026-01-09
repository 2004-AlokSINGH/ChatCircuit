const API = "http://localhost:8000";

export async function sendMessage(message, threadId) {
  const res = await fetch(`${API}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, thread_id: threadId }),
  });
  return res.json();
}

export async function fetchThreads() {
  const res = await fetch(`${API}/threads`);
  return res.json();
}

export async function fetchConversation(threadId) {
  const res = await fetch(`${API}/conversation/${threadId}`);
  return res.json();
}
