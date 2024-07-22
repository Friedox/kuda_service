import '../../styles/mobile/style.css';
import React, { useEffect, useState, useRef } from 'react';
import Button from "../../components/mobile/Button";
import profile_example from '../../assets/profile_example.png';
import seen from "../../assets/icon/seen.svg";
import GreyHeader from "../../components/mobile/GreyHeader";
import ChatItem from '../../components/mobile/ChatItem';
import ChatInput from '../../components/mobile/ChatInput';

function Conversation(conversationID) {
    // TODO: Get conversation information
    const conversationInfo = {
        ConversationID: 165,
        ConversationName: "Universitetskaya",
        isGroup: true,
    }
    // TODO: Get conversation participants for faster access
    const participants = {
        users:[0, 1],
    }
    // TODO: Get information about participants
    const participantsInfo = new Array();
    for (let i = 0; i < participants.users.length; i++) {
        participantsInfo.push();
    }
    // TODO: Get messages from backend
    const messages = {
        messagesList: [
            {
                messageID: 0,
                conversationID: 165,
                senderUserID: 0,
                content: "Hello, I want to go with you, tell me do you have air conditioning in the car?",
                timestamp: new Date(),
                isRead: true
            },
            {
                messageID: 1,
                conversationID: 165,
                senderUserID: 1,
                content: "Hi, yes of course",
                timestamp: new Date(),
                isRead: true
            },
            {
                messageID: 3,
                conversationID: 165,
                senderUserID: 0,
                content: "Cool, then I'm booking a trip.",
                timestamp: new Date(),
                isRead: true
            },
        ]
    }

    // Display
    return (
        <>
            <section className='mobile_section'>
            <   GreyHeader header_text={conversationInfo.ConversationName}/>
                <div className="conversation_container">
                    <div className="white_bar"></div>
                    <div className="conversation_holder">
                        <div className="conversation_area">
                            <ChatInput conversation_id={Conversation.ConversationID}/>
                            <div>Test</div>
                            <div>Test2</div>
                        </div>
                    </div>
                </div>
                
            </section>
        </>
    )
}

export default Conversation;