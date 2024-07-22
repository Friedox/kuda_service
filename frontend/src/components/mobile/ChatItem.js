import React from 'react';
import line from '../../assets/icon/line.svg'
import verified from "../../assets/icon/verified.svg"
import ProfileAvatar from './ProfileAvatar';

const ChatItem = ({ avatar, name, message, time, statusIcon, verified }) => {
  return (
    <div className="chat_item_holder">
    <a href='#' className="chat_item">
      <ProfileAvatar avatar={avatar} verified={verified}/>
      <div className="chat_info">
        <div className="chat_header">
          <span className="chat_name">{name}</span>
          <span className="chat_time">{time}</span>
        </div>
        <div className="chat_header_content">
            <span className="chat_content">{message}</span>
            <div className="chat_status_icon">
                <img src={statusIcon}/>
            </div>
        </div>
      </div>
    </a>
    <div class="chat_line_holder">
    <img class="chat_line" src={line}/>
    </div>
    </div>
  );
};

export default ChatItem;