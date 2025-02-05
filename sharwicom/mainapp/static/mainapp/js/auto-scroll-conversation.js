const conversationDiv = document.querySelector('.sharwicom-wrapper .conversation');

function scrollConversation() {
    console.log(conversationDiv.scrollHeight);
    conversationDiv.scrollTop = conversationDiv.scrollHeight;
}

scrollConversation();
