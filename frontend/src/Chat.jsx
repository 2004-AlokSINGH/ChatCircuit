import { useEffect, useRef, useState } from "react";
import { sendMessage } from "./api";

export default function Chat({
  threadId,
  setThreadId,   
  messages,
  setMessages,
  refreshThreads
}) {

  const [input, setInput] = useState("");
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);


async function handleSend() {
  if (!input.trim()) return;

  const userMsg = { role: "user", content: input };
  setMessages((m) => [...m, userMsg]);
  setInput("");

  const res = await sendMessage(input, threadId);

 
  if (!threadId) {
    setThreadId(res.thread_id);
  }

  refreshThreads();

  setMessages((m) => [
    ...m,
    {
      role: "assistant",
      content: res.response,
      tools: res.tools_used || [],   
    },
  ]);
}

  return (
    <div className="chat">
      <div className="chat-header">
        {threadId ? `Thread: ${threadId.slice(0, 8)}` : "New Conversation"}
      </div>

      <div className="chat-body">
        {messages.map((m, i) => (
          <div key={i} className={`msg ${m.role}`}>
            {/* Show who is speaking */}
            <div className="msg-author">
              {m.role === "user" ? "You:" : "Agent:"}
            </div>
            
            {/* Show the actual message */}
            <div className="msg-content">{m.content}</div>

            {/* Show tools used if any */}
            {m.role === "assistant" && m.tools?.length > 0 && (
              <div className="tool-indicator">
                🔧 Using tool: {m.tools.join(", ")}
              </div>
            )}
          </div>
        ))}

        <div ref={bottomRef} />
      </div>

      <div className="chat-input">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="Type your message…"
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
}
