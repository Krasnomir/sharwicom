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
function updateConversation() {
    const csrftoken = getCookie('csrftoken');

    // retrieve usernames of people in the conversation from conversation div's data attributes 
    // checks will be performed on the server side to make sure user won't access conversations which they aren't a part of
    // without those checks they could easily access any existing conversations by changing the data attributes
    const conversation = document.querySelector('.conversation');
    const user = conversation.dataset.user;
    const reciepent = conversation.dataset.reciepent;

    // sending xml http request with info about conversation which is requested to be synchronized (it sends usernames of people in the conversation)
    const xhr = new XMLHttpRequest();
    xhr.open('GET', `../conversations/sync?user1=${user}&user2=${reciepent}`, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
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
                const messageClass = (user === author) ? "you" : "reciepent";
                messagesHTML += '<div class="'+messageClass+'"><span><b>'+messageAuthor+':</b> '+content+'</span></div>';
            }
        }

        conversation.innerHTML = messagesHTML;
    }
}

window.onload = () => {
    updateConversation();
    setInterval(updateConversation, 1000);
}