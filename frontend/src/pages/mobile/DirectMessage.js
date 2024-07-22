import '../../styles/mobile/style.css';
import React, { useEffect, useState, useRef } from 'react';
import profile_example from '../../assets/profile_example.png';
import arrow from "../../assets/icon/arrow.svg";
import blue_circle from "../../assets/icon/blue_circle.svg";
import seen from "../../assets/icon/seen.svg";
import GreyHeader from "../../components/mobile/GreyHeader";
import ChatItem from '../../components/mobile/ChatItem';

function DirectMessages() {
    // Place holder for chat getter, including DM and group messages, sorted in reverse chronological order
    const recentMessaages = useState(null);
    //

    return (
        <>
            <section className="mobile_section">
                <GreyHeader header_text="Chats"/>
                <ChatItem avatar={profile_example} name="Dmitry Zdivin" message="Hello" time="13:23" statusIcon={blue_circle} verified={true}/>
                
                <ChatItem avatar={profile_example} name="Dmitry Zdivin" message="Hello" time="13:23" statusIcon={seen} verified={false}/>
            
            </section>
        </>
    )
}

export default DirectMessages;