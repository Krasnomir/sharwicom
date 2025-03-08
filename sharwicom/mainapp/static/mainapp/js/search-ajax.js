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

// sends a get request to the server
// if there is no conversation object between the requesting user, the server is going to create one
// if not it's just going to redirect the user to the existing conversation page
function conversationRequest(username) {

    const xhr = new XMLHttpRequest();
    xhr.open('GET', `../conversations/request?username=${username}`, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send();

    xhr.addEventListener('load', () => {
        const parsedJSONResponse = JSON.parse(xhr.responseText);

        if(parsedJSONResponse.success) {
            location.href = '../conversation/' + username;
        }
    });
}

// displays the search results inside the first found div that has a search-results class
// adds an event listener for each added div that calls conversationRequest function upon clicking it with the username assosiated with that div
function displaySearchResults(results, type , resultsDiv) {
    resultsDiv.innerHTML = '';

    if(type === "conversations") {
        for(const user of results) {
            const searchResultDiv = document.createElement('div');
            searchResultDiv.className = 'search-result';
            searchResultDiv.innerHTML = user.username;
            resultsDiv.appendChild(searchResultDiv);
    
            searchResultDiv.addEventListener('click', () => {
                conversationRequest(user.username)
            });
        }
    }
    else if(type === "content") {
        for(const content of results) {
            const searchResultDiv = document.createElement('div');
            searchResultDiv.className = 'search-result';
            searchResultDiv.innerHTML = `<a href=../content/${content.url_name}>${content.title}<br>${content.type}<br>by ${content.author}</a>`;
            resultsDiv.appendChild(searchResultDiv);
            
            /*
            searchResultDiv.addEventListener('click', () => {
                conversationRequest(user.username)
            });
            */
        }
    }
}

function getSearchResults(searchQuery, type, resultsDiv) {
    // create a xml http GET request with the search query in url query string
    const xhr = new XMLHttpRequest();
    xhr.open('GET', `../conversations/search?query=${searchQuery}&type=${type}`, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send();

    xhr.addEventListener('load', () => {
        const results = JSON.parse(xhr.responseText);

        displaySearchResults(results.search_results, type, resultsDiv);
    });
}

addEventListener('load', () => {
    const searchButtons = document.querySelectorAll('.search-button');

    for(const searchButton of searchButtons) {
        searchButton.addEventListener('click', () => {
            const type = searchButton.parentElement.parentElement.dataset['type']; // either "content" or "conversations" (for now)
            const searchQuery = searchButton.parentElement.children[0].value;
            const resultsDiv = searchButton.parentElement.parentElement.children[1];

            getSearchResults(searchQuery, type, resultsDiv);
        });
    }

    /*
    searchButton.addEventListener('click', (event) => {
        getSearchResults(searchQuery.value);
    })
    */
});