export default function Sidebar({ threads, active, onSelect, onNewChat }) {
  return (
    <div className="sidebar">
      <h2>Agent ChatCircuit</h2>

      <button className="new-chat" onClick={onNewChat}>
        + New Chat
      </button>

      <div className="thread-list">
        {threads.slice().reverse().map((id) => (
          <button
            key={id}
            className={`thread ${id === active ? "active" : ""}`}
            onClick={() => onSelect(id)}
          >
            {id.slice(0, 8)}
          </button>
        ))}
      </div>
    </div>
  );
}
