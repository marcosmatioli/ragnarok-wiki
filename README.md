# Ragnarok

## Running

Create a `.env` file to configure some variables like this:

```dotenv
MONGO_INITDB_ROOT_USERNAME=root
MONGO_INITDB_ROOT_PASSWORD=changeme
ME_CONFIG_MONGODB_ADMINUSERNAME=admin
ME_CONFIG_MONGODB_ADMINPASSWORD=admin
API_KEY=e8b1fbd9a8f4dfd9d430174bcfd2bfea
```

Bellow the explanation about each variable:

| Variable                        | Description                                          |
| ------------------------------- | ---------------------------------------------------- |
| MONGO_INITDB_ROOT_USERNAME      | Mongo DB root admin                                  |
| MONGO_INITDB_ROOT_PASSWORD      | Mongo DB root password                               |
| ME_CONFIG_MONGODB_ADMINUSERNAME | Mongo Express admin user                             |
| ME_CONFIG_MONGODB_ADMINPASSWORD | Mongo Express admin password                         |
| API_KEY                         | [Divine Pride](https://www.divine-pride.net) API key |

```bash
docker compose up -d
```
