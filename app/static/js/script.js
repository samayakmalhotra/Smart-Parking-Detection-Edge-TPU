async function postData(url = 'http://localhost:5000/spaces') {
  const response = await fetch(url, {
    method: 'GET',
    mode: 'cors',
    cache: 'no-cache',
    credentials: 'same-origin',
    headers: {
      'Content-Type': 'application/json'
    },
    redirect: 'follow',
    referrerPolicy: 'no-referrer',
  });
  return response.json();
}

function handleSpaces(data) {
    let emptySpaces = data['empty_spaces'];
    let parkedSpaces = data['parked_spaces'];

    emptyUl = document.createElement('ul');
    let emptyColl = document.getElementById('empty-space-collection')
    
    while (emptyColl.firstChild) {
        emptyColl.removeChild(emptyColl.firstChild);
    }
    emptyColl.appendChild(emptyUl);

    emptySpaces.forEach(function (item) {
        let li = document.createElement('li');
        li.className = 'collection-item'
        emptyUl.appendChild(li);

        li.innerHTML += item;
    });

    parkedUl = document.createElement('ul');
    parkedColl = document.getElementById('parked-space-collection');

    while (parkedColl.firstChild) {
        parkedColl.removeChild(parkedColl.firstChild);
    }
    parkedColl.appendChild(parkedUl);

    parkedSpaces.forEach(function (item) {
        let li = document.createElement('li');
        li.className = 'collection-item'
        parkedUl.appendChild(li);

        li.innerHTML += item;
    });
}

function handleEverything(){
    postData(`${window.location.href}\spaces`)
        .then(data => {
            handleSpaces(data);
        });

        setTimeout(handleEverything, 500);
}

handleEverything();