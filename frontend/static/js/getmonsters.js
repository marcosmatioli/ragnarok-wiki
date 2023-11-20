let currentPage = 1;
const perPage = 100;
const api_address = window.location.origin

async function loadPage(direction) {
    currentPage += direction;

    if (currentPage < 1) {
        currentPage = 1;
    }

    const searchName = document.getElementById('search-name').value;

    try {
        // call monsters api with the name parameter
        const response = await fetch(`${api_address}/api/monsters?name=${searchName}&page=${currentPage}&per_page=${perPage}`);
        const data = await response.json();
        const tableBody = document.getElementById('table-body');

        tableBody.innerHTML = ''; // clean table body

        data.forEach(item => {
            // create table elements
            const row = document.createElement('tr');
            const idCell = document.createElement('td');
            const nameCell = document.createElement('td');
            const imageCell = document.createElement('td');
            const imageLink = document.createElement('a');
            const image = document.createElement('img');

            // create link of each monster
            const monsterLink = document.createElement('a');
            monsterLink.href = `monster?id=${item.id}`;
            monsterLink.textContent = `${item.id}`;

            idCell.appendChild(monsterLink);
            nameCell.textContent = item.name;

            // build image link based on id
            const imageUrl = `https://static.divine-pride.net/images/mobs/png/${item.id}.png`;
            image.src = imageUrl;
            image.alt = `Monster Image ${item.id}`;
            image.height = 75;

            imageLink.appendChild(image);
            imageCell.appendChild(imageLink);

            row.appendChild(idCell);
            row.appendChild(nameCell);
            row.appendChild(imageCell);
            tableBody.appendChild(row);
        });

        // update button pagination based on actual state
        document.getElementById('prev-page').hidden = currentPage === 1;
        document.getElementById('next-page').hidden = data.length < perPage;
    } catch (error) {
        console.error('Error loading JSON data:', error);
    }
}

// eventlistener based on "Enter" event key
const search_box = document.getElementById('search-name');
search_box?.addEventListener('keyup', function(event) {
    if (event.key === 'Enter') {
        loadPage(0);
    }
});

// call function to load first page
window.addEventListener('load', () => {
    loadPage(0);
});
