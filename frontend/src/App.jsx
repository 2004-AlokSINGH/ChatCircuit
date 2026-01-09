import { useEffect, useState } from "react";
import Sidebar from "./Sidebar";
import Chat from "./Chat";
import { fetchThreads, fetchConversation } from "./api";
import "./styles.css";

export default function App() {
  const [threads, setThreads] = useState([]);
  const [activeThread, setActiveThread] = useState(null);
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    fetchThreads().then(setThreads);
  }, []);

  async function selectThread(threadId) {
    setActiveThread(threadId);
    const data = await fetchConversation(threadId);
    setMessages(data);
  }



  function newChat() {
    setActiveThread(null);
    setMessages([]);
  }
  

  return (
    <div className="layout">
      <Sidebar
        threads={threads}
        active={activeThread}
        onSelect={selectThread}
        onNewChat={newChat}
      />
      <Chat
      threadId={activeThread}
      setThreadId={setActiveThread}   
      messages={messages}
      setMessages={setMessages}
      refreshThreads={() => fetchThreads().then(setThreads)}
    />
    </div>
  );
}
