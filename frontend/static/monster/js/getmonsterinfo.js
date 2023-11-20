const api_address = window.location.origin

// Função para buscar informações do monstro
function getMonsterInfo(id) {
    fetch(`${api_address}/api/monster/${id}`)
        .then(response => response.json())
        .then(data => {
            if ("error" in data) {
                alert(data.error);
            } else {
                // get main info
                document.getElementById("monsterId").textContent = data.id;
                document.getElementById("monsterName").textContent = data.name;
                document.getElementById("monsterHealth").textContent = data.stats.health;
                document.getElementById("monsterLevel").textContent = data.stats.level;
                document.getElementById("monsterDef").textContent = data.stats.defense;
                document.getElementById("monsterMDef").textContent = data.stats.magicDefense;
                // get stats
                document.getElementById("monsterStr").textContent = data.stats.str;
                document.getElementById("monsterAgi").textContent = data.stats.agi;
                document.getElementById("monsterVit").textContent = data.stats.vit;
                document.getElementById("monsterInt").textContent = data.stats.int;
                document.getElementById("monsterDex").textContent = data.stats.dex;
                document.getElementById("monsterLuk").textContent = data.stats.luk;
            }
        })
        .catch(error => {
            console.error("Erro ao buscar informações do monstro:", error);
        });
}

// Obtém o ID do monstro da URL
const urlParams = new URLSearchParams(window.location.search);
const monsterId = urlParams.get("id");

if (monsterId) {
    getMonsterInfo(monsterId);
} else {
    alert("ID do monstro não encontrado na URL.");
}
