import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
    const [message, setMessage] = useState("");
    const [chat, setChat] = useState([]);
    const [loading, setLoading] = useState(false);

    const sendMessage = async () => {
        if (!message.trim()) return;
        
        const newChat = [...chat, { user: "You", text: message }];
        setChat(newChat);
        setLoading(true);

        try {
            const res = await axios.post("http://localhost:5000/chat", { message });
            setChat([...newChat, { user: "Chatbot", text: res.data.response }]);
        } catch (error) {
            setChat([...newChat, { user: "Chatbot", text: "Error fetching response." }]);
        }
        
        setLoading(false);
        setMessage("");
    };

    return (
        <div className="chat-container">
            <h2>University Chatbot</h2>
            <div className="chat-box">
                {chat.map((msg, index) => (
                    <p key={index}><strong>{msg.user}:</strong> {msg.text}</p>
                ))}
            </div>
            {loading && <p>Thinking...</p>}
            <input 
                type="text"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Ask something..."
            />
            <button onClick={sendMessage}>Send</button>
        </div>
    );
}

export default App;
