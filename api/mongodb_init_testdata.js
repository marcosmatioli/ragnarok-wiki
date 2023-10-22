db = db.getSiblingDB("ragnarok");

if (!db.getCollectionNames().includes("monsters")) {
    db.createCollection("monsters");

    db.monsters.insert({
        "id": 1001,
        "dbname": "SCORPION",
        "drops": [
            {"itemId": 990, "chance": 35, "stealProtected": false, "serverTypeName": null, "optionGroup": "G0"},
            {"itemId": 904, "chance": 2750, "stealProtected": false, "serverTypeName": null, "optionGroup": "G0"},
            {"itemId": 757, "chance": 29, "stealProtected": false, "serverTypeName": null, "optionGroup": "G0"},
            {"itemId": 943, "chance": 105, "stealProtected": false, "serverTypeName": null, "optionGroup": "G0"},
            {"itemId": 601, "chance": 500, "stealProtected": false, "serverTypeName": null, "optionGroup": "G0"},
            {"itemId": 7041, "chance": 500, "stealProtected": false, "serverTypeName": null, "optionGroup": "G0"},
            {"itemId": 625, "chance": 10, "stealProtected": false, "serverTypeName": null, "optionGroup": "G0"},
            {"itemId": 4068, "chance": 1, "stealProtected": true, "serverTypeName": null, "optionGroup": "G0"}
        ],
        "mapDrops": [],
        "metamorphosis": [],
        "mvpdrops": [],
        "name": "Escorpião",
        "propertyTable": {
            "0": 100, "1": 150, "2": 90, "3": 25, "4": 100, "5": 125, "6": 100, "7": 100, "8": 100, "9": 100
        },
        "questObjective": [7131, 7493],
        "skill": [
            {"idx": 22596, "skillId": 186, "status": "BERSERK_ST", "level": 1, "chance": 200, "casttime": 0, "delay": 5000, "interruptable": true, "changeTo": null, "condition": null, "conditionValue": null, "sendType": null, "sendValue": null},
            {"idx": 22597, "skillId": 176, "status": "BERSERK_ST", "level": 1, "chance": 50, "casttime": 800, "delay": 5000, "interruptable": false, "changeTo": null, "condition": null, "conditionValue": null, "sendType": null, "sendValue": null},
            {"idx": 22598, "skillId": 188, "status": "BERSERK_ST", "level": 1, "chance": 50, "casttime": 300, "delay": 5000, "interruptable": false, "changeTo": null, "condition": null, "conditionValue": null, "sendType": null, "sendValue": null}
        ],
        "slaves": [],
        "sounds": ["monster_shell.wav", "scorpion_attack.wav", "scorpion_damage.wav", "scorpion_die.wav"],
        "spawn": [
            {"mapname": "moc_fild11", "amount": 41, "respawnTime": 5000},
            {"mapname": "moc_fild18", "amount": 160, "respawnTime": 5000}
        ],
        "spawnSet": [],
        "stats": {
            "attackRange": 1, "level": 16, "health": 136, "sp": 1, "str": 12, "int": 5, "vit": 10, "dex": 19, "agi": 15, "luk": 5, "rechargeTime": 1564, "atk1": 7, "atk2": 7,
            "attack": {"minimum": 33, "maximum": 36}, "magicAttack": {"minimum": 25, "maximum": 30}, "defense": 16, "baseExperience": 169, "jobExperience": 115,
            "aggroRange": 10, "escapeRange": 12, "movementSpeed": 200, "attackSpeed": 864, "attackedSpeed": 576, "element": 23, "scale": 0, "race": 4,
            "magicDefense": 5, "hit": 231, "flee": 205, "ai": "MONSTER_TYPE_01", "mvp": 0, "class": 0, "attr": 0, "res": 0, "mres": 0
        }
    });

    db.monsters.insert({
        "id": 1168,
        "dbname": "SCORPION_KING",
        "drops": [
            {"itemId": 994, "chance": 23, "stealProtected": false, "serverTypeName": null, "optionGroup": "G0"},
            {"itemId": 1046, "chance": 2425, "stealProtected": false, "serverTypeName": null, "optionGroup": "G0"},
            {"itemId": 1005, "chance": 8, "stealProtected": false, "serverTypeName": null, "optionGroup": "G0"},
            {"itemId": 904, "chance": 2500, "stealProtected": false, "serverTypeName": null, "optionGroup": "G0"},
            {"itemId": 943, "chance": 1500, "stealProtected": false, "serverTypeName": null, "optionGroup": "G0"},
            {"itemId": 509, "chance": 350, "stealProtected": false, "serverTypeName": null, "optionGroup": "G0"},
            {"itemId": 512, "chance": 0, "stealProtected": false, "serverTypeName": null, "optionGroup": "G0"},
            {"itemId": 4130, "chance": 1, "stealProtected": true, "serverTypeName": null, "optionGroup": "G0"}
        ],
        "mapDrops": [],
        "metamorphosis": [],
        "mvpdrops": [],
        "name": "Rei Escorpião",
        "propertyTable": {
            "0": 100,
            "1": 150,
            "2": 90,
            "3": 25,
            "4": 100,
            "5": 125,
            "6": 100,
            "7": 100,
            "8": 100,
            "9": 100
        },
        "questObjective": [],
        "skill": [],
        "slaves": [],
        "sounds": ["monster_shell.wav", "peco_egg_heartbeat.wav", "pupa_die.wav", "pupa_split.wav"],
        "spawn": [],
        "spawnSet": [],
        "stats": {
            "attackRange": 1,
            "level": 50,
            "health": 5719,
            "sp": 1,
            "str": 1,
            "int": 1,
            "vit": 47,
            "dex": 91,
            "agi": 50,
            "luk": 30,
            "rechargeTime": 1700,
            "atk1": 630,
            "atk2": 113,
            "attack": {"minimum": 555, "maximum": 807},
            "magicAttack": {"minimum": 130, "maximum": 197},
            "defense": 64,
            "baseExperience": 1033,
            "jobExperience": 605,
            "aggroRange": 10,
            "escapeRange": 12,
            "movementSpeed": 200,
            "attackSpeed": 1000,
            "attackedSpeed": 500,
            "element": 23,
            "scale": 2,
            "race": 7,
            "magicDefense": 10,
            "hit": 300,
            "flee": 311,
            "ai": "MONSTER_TYPE_17",
            "mvp": 0,
            "class": 1,
            "attr": 0,
            "res": 0,
            "mres": 0
        }
    });
}