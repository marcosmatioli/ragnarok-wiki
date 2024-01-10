const API_ADDRESS = window.location.origin

let currentPage = 1;
let perPage = 100;

const raceIcons = {
    0: {
      icon: 'icon-formless',
      color: 'rgb(119, 0, 255)',
      title: 'Monstro do tipo amorfo',
    },
    1: {
      icon: 'icon-undead',
      color: 'rgb(0, 0, 0)',
      title: 'Monstro do tipo morto-vivo',
    },
    2: {
      icon: 'icon-brute',
      color: 'rgb(138, 58, 0)',
      title: 'Monstro do tipo bruto',
    },
    3: {
      icon: 'icon-plant',
      color: 'rgb(0, 165, 0)',
      title: 'Monstro do tipo planta',
    },
    4: {
      icon: 'icon-insect',
      color: 'rgb(0, 138, 2)',
      title: 'Monstro do tipo inseto',
    },
    5: {
      icon: 'icon-fish',
      color: 'rgb(0, 47, 255)',
      title: 'Monstro do tipo peixe',
    },
    6: {
      icon: 'icon-demon',
      color: 'rgb(252, 19, 3)',
      title: 'Monstro do tipo demônio',
    },
    7: {
      icon: 'icon-human',
      color: 'rgb(252, 210, 124)',
      title: 'Monstro do tipo humanoide',
    },
    8: {
      icon: 'icon-angel',
      color: 'rgb(3, 157, 252)',
      title: 'Monstro do tipo anjo',
    },
    9: {
      icon: 'icon-dragon',
      color: 'rgb(252, 119, 3)',
      title: 'Monstro do tipo dragão',
    },
};

const monsterScale = {
    0: { scale: 'Pequeno' },
    1: { scale: 'Médio' },
    2: { scale: 'Grande' }
}

const monsterType = {
    0: { monsterType: 'Neutro', monsterTypeColor: 'rgb(171, 171, 171)' },
    1: { monsterType: 'Água', monsterTypeColor: 'rgb(0, 208, 255)' },
    2: { monsterType: 'Terra', monsterTypeColor: 'rgb(135, 41, 1)' },
    3: { monsterType: 'Fogo', monsterTypeColor: 'rgb(255, 38, 0)' },
    4: { monsterType: 'Vento', monsterTypeColor: 'rgb(65, 136, 150)' },
    5: { monsterType: 'Veneno', monsterTypeColor: 'rgb(144, 3, 252)' },
    6: { monsterType: 'Sagrado', monsterTypeColor: 'rgb(176, 159, 26)' },
    7: { monsterType: 'Sombrio', monsterTypeColor: 'rgb(1, 15, 79)' },
    8: { monsterType: 'Fantasma', monsterTypeColor: 'rgb(82, 82, 82)' },
    9: { monsterType: 'Maldito', monsterTypeColor: 'rgb(0, 0, 0)'}
}

async function loadPage(direction) {
    currentPage += direction;

    if (currentPage < 1) {
        currentPage = 1;
    }

    const searchName = document.getElementById('search-name').value;

    try {
        // call monsters api with the name parameter
        const response = await fetch(`${API_ADDRESS}/api/monsters?name=${searchName}&page=${currentPage}&per_page=${perPage}`);
        const data = await response.json();
        const rowContainer = document.querySelector('.row.row-cols-1.row-cols-md-4.mb-3');

        rowContainer.innerHTML = '';

        data.forEach(item => {
            // create monster card elements
            const monsterCard = document.createElement('div');
            monsterCard.className = 'col mt-3';
            
            if (raceIcons[item.stats.race]) {
                const { icon, color, title } = raceIcons[item.stats.race];

                if (monsterScale[item.stats.scale]) {
                    const { scale } = monsterScale[item.stats.scale];
                    
                    let monsterTypeLevel = ""
                    
                    if (Math.trunc(item.stats.element/20) != 0) {
                        const roman = { 1: 'I', 2: 'II', 3: 'III', 4: 'IV' };
                        monsterTypeLevel = " " + roman[Math.trunc(item.stats.element/20)]
                    }
                    
                    let monsterTypeKey = item.stats.element%20

                    const monsterTypeText = monsterType[monsterTypeKey];
                    if (monsterTypeText) {

                        const { monsterType, monsterTypeColor } = monsterTypeText;
                        monsterCard.innerHTML = `
                            <div class="card h-100 shadow-sm">
                                <div class="card-img-top d-flex justify-content-center align-items-center" style="background-color: rgb(235, 235, 235); height: 10rem;">
                                    <img src="https://static.divine-pride.net/images/mobs/png/${item.id}.png" class="img-fluid" alt="Monster Image ${item.id}" style="max-height: 90%;">
                                    <i class="${icon} position-absolute m-1 fa-xl" title="${title}" style="top: 0; left: 0; color: ${color}; font-size: 20px;"></i>
                                    <span class="badge text-bg-danger position-absolute m-1" style="top: 0; right: 0;">
                                        #${item.id}
                                    </span>
                                </div>
                                <div class="card-body">
                                    <h5 class="card-title">
                                        <span class="d-inline-block text-truncate" title="${item.name}" style="max-width: 100%;">
                                            ${item.name}
                                        </span>
                                    </h5>
                                    <ul class="list-group list-group-flush">
                                        <li class="list-group-item d-flex justify-content-between align-items-center">
                                            Level
                                            <span class="badge bg-secondary text-truncate ms-1">${item.stats.level}</span>
                                        </li>
                                        <li class="list-group-item d-flex justify-content-between align-items-center">
                                            Elemento
                                            <span class="badge text-truncate ms-1" style="background-color: ${monsterTypeColor}">${monsterType}${monsterTypeLevel}</span>
                                        </li>
                                        <li class="list-group-item d-flex justify-content-between align-items-center">
                                            Tamanho
                                            <span class="badge bg-secondary text-truncate ms-1">${scale}</span>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        `;

                        rowContainer.appendChild(monsterCard);
                    }
                } 
            }
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
        currentPage = 1
        loadPage(0);
    }
});

// call function to load first page
window.addEventListener('load', () => {
    loadPage(0);
});
