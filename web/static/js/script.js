
// Function to make API GET requests to the server on port 8001
function makeApiGetRequest(url) {
    return fetch(`http://localhost:8001${url}`)
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Request failed');
            }
        });
}

function todo() {
    var input = document.querySelector(".inputToDo").value;
    makeApiGetRequest(`/add/${encodeURIComponent(input)}`)
        .then(data => {
            window.location.reload()
        })
        .catch(error => {

            console.error(error);
        });
    }

function editToDo(id) {
    var todo = document.getElementById(id).value;
    var todoID = id;
    console.log({todo})

        makeApiGetRequest(`/edit/${encodeURIComponent(todoID)}/${encodeURIComponent(todo)}`)
           .then(data => {
                window.location.reload()
            })
            .catch(error => {

                console.error(error);
            });
    }

function deleteToDo(id) {
    var todoID = id;

    makeApiGetRequest(`/delete/${encodeURIComponent(todoID)}`)
       .then(data => {
            window.location.reload()
        })
        .catch(error => {
            // Handle the fetch error or request failure
            console.error(error);
        });
}

function checkToDo(id) {
    var todoID = id;

        makeApiGetRequest(`/check/${encodeURIComponent(todoID)}`)
           .then(data => {
                window.location.reload()
            })
            .catch(error => {

                console.error(error);
            });
    }

function uncheckToDo(id) {
    var todoID = id;

        makeApiGetRequest(`/uncheck/${encodeURIComponent(todoID)}`)
           .then(data => {
                window.location.reload()
            })
            .catch(error => {

                console.error(error);
            });
    }

