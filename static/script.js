document.getElementById('main-form').onsubmit = function (e) {
    e.preventDefault();
    fetch('/', {
        method: 'POST',
        body: JSON.stringify({
            'description': document.getElementById('description').value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (jsonResponse) {
            console.log(jsonResponse);
            const liItem = document.createElement('li');
            liItem.innerHTML = `<input type="checkbox" data-id="${jsonResponse.id}" class="check">` + jsonResponse['description'];
            document.getElementById('todos').appendChild(liItem);
            document.getElementById('error').className = 'hidden';
        })
        .catch(function () {
            document.getElementById('error').className = '';
        });
}

const checkBoxes = document.querySelectorAll('.check');
for (let checkBox of checkBoxes) {
    checkBox.onchange = function (e) {
        const checked = e.target.checked;
        const id = e.target.dataset['id'];
        fetch('/check/' + id, {
            method: 'POST',
            body: JSON.stringify({
                'checked': checked
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(function (response) {
                return response.json();
            })
            .then(function (jsonResponse) {
                console.log(jsonResponse);
                document.getElementById('error').className = 'hidden';
            })
            .catch(function () {
                document.getElementById('error').className = '';
            });
    }
}