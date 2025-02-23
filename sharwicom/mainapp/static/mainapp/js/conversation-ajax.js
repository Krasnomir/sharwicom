function getCookie(name) {
    let cookieValue = null;

    if(window.document.cookie && window.document.cookie !== '') {
        const cookies = window.document.cookie.split(';');

        // iterate through stored cookies 
        for(let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            
            if(cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// dynamically load messages from the server wihtout refreshing the whole page
function syncMessages() {
    // retrieve usernames of people in the conversation from conversation div's data attributes 
    // checks will be performed on the server side to make sure user won't access conversations which they aren't a part of
    // without those checks they could easily access any existing conversations by changing the data attributes
    const conversation = document.querySelector('.conversation');
    const user = conversation.dataset.user;
    const recipient = conversation.dataset.recipient;

    // sending xml http request with info about conversation which is requested to be synchronized (it sends usernames of people in the conversation)
    const xhr = new XMLHttpRequest();
    xhr.open('GET', `../conversations/sync?user1=${user}&user2=${recipient}`, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send();

    // recieving server response (that contains an array of messages if server accepts the request)
    xhr.onload = () => {
        const response = JSON.parse(xhr.responseText);

        // clear the contents of the conversation wrapper
        conversation.innerHTML = '';

        let messagesHTML = '';

        if(response.success == 'false') {
            messagesHTML.concat("Error synchronizing messages");
        }
        else {
            const messages = response.messages;

            for(let i = 0; i < messages.length; i++) {
                const date = messages[i].date; // curently not being used
                const author = messages[i].author__username;
                const content = messages[i].content;
                
                const messageAuthor = (user === author) ? 'You' : author;
                const messageClass = (user === author) ? "you" : "recipient";
                messagesHTML += '<div class="'+messageClass+'"><div class="message"><b>'+messageAuthor+':</b> '+content+'</div></div>';
            }
        }

        conversation.innerHTML = messagesHTML;
    }
}

function sendMessage() {
    const csrftoken = getCookie('csrftoken');

    const conversation = document.querySelector('.conversation');
    const user = conversation.dataset.user;
    const recipient = conversation.dataset.recipient;
    const message_container = window.document.querySelector('.sharwicom-wrapper .create .message');
    const message_content = message_container.value;
    
    // clear the message input field
    message_container.value = "";

    // sending xml http request with info about conversation which is requested to be synchronized (it sends usernames of people in the conversation)
    const xhr = new XMLHttpRequest();
    xhr.open('POST', `../conversations/send?sender=${user}&message=${message_content}`, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    const data = JSON.stringify({
        sender: user,
        recipient: recipient,
        message_content: message_content
    });
    xhr.send(data);

    xhr.onload = () => {
        syncMessages();

        setTimeout(scrollConversation, 100); // can't be called immediately beacuse syncMessages function takes some time to add new messages to the user page 
    }
}

onload = () => {
    syncMessages();

    // so previously i used forms to create POST requests regarding the message creation 
    // but i didnt want it to refresh the entire page every time a user sends a message
    // now its implemented using ajax, just like the message syncing
    const sendBtn = document.querySelector('.sharwicom-wrapper .send-message');
    sendBtn.addEventListener('click', sendMessage);

    //setInterval(syncMessages, 1000); // updates the messages every x milliseconds 
}