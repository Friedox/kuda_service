import '../../styles/mobile/style.css';
import React, { useEffect, useState, useRef } from 'react';
import Button from "../../components/mobile/Button";
import send from "../../assets/icon/send.svg"


function ChatInput({conversation_id}) {
    const [message, setMessage] = useState("");

    const handleInputChange = (e) => {
        setMessage(e.target.value);
    };

    return (
        <>
        <div className="message_input_area">
            <input
                className="message_input_field"
                type="text" 
                placeholder="Type a message..." 
                value={message} 
                onChange={handleInputChange} 
            />
            <div className="send_button">
                <img src={send} alt="Send" />
            </div>
        </div>
        </>
    )
}

export default ChatInput;