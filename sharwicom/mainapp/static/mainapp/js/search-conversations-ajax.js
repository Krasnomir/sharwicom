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

function getSearchResults(searchQuery, callback) {
    const csrftoken = getCookie('csrftoken');

    const xhr = new XMLHttpRequest();
    xhr.open('GET', `../conversations/search?query=${searchQuery}`, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    xhr.send();

    xhr.addEventListener('load', () => {
        const response = JSON.parse(xhr.responseText);

        console.log(response.search_results);

        callback(response.search_results);
    });
}

addEventListener('load', () => {
    const searchButton = document.getElementById('search-button');
    const searchQuery = document.getElementById('search-query');

    searchButton.addEventListener('click', (event) => {
        getSearchResults(searchQuery.value, (results) => {
            console.log(results);
        });
    })
});