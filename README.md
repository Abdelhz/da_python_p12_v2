# Epic Events Project

**Epic Events project is a Django REST Framework application (API) fully command lines oriented.**

## Maine functionalities

- Create, read, update and delete users
- Create, read, update and delete clients.
- Create, read, update and delete contracts for clients.
- Create, read, update and delete events for clients who signed a contract.

## Setup

1. Create a project folder named "project_12_Epic_Events_django_rest_framework":

    ```bash
    mkdir project_12_Epic_Events_django_rest_framework
    ```

2. Navigate into the folder:

    ```bash
    cd project_12_Epic_Events_django_rest_framework
    ```

3. Clone the project from GitHub into this folder:

    ```bash
    git clone https://github.com/Abdelhz/da_python_p12_v2.git
    ```

4. Navigate into the cloned project's directory "da_python_p12_v2":

    ```bash
    cd da_python_p12_v2
    ```

5. Create a virtual environment:

    ```bash
    python3 -m venv env_Epic_Events_django_rest_project
    ```

6. Activate the virtual environment:
    - On Windows:

        ```bash
        cd env_Epic_Events_django_rest_project/Scripts/
        ```

        ```bash
        source activate
        ```

        ```bash
        cd ../../
        ```

    - On Unix or MacOS:

        ```bash
        source env_Epic_Events_django_rest_project/bin/activate
        ```

7. Install the dependencies from the `requirements.txt` file:

    ```bash
    pip install -r requirements.txt
    ```

8. Navigate to the directory where `manage.py` is located:

    ```bash
    cd da_python_p12_v2/Epic_Events
    ```

9. Setting up the database with mysql and sentry :

- Create a local database with mysql server.
- Create a django project in sentry
- modify db_config.ini file :

```ini
[mysql]
database_name = you_database_name
username = you_database_username
password = you_database_password

[sentry]
sentry_link = Use your own sentry link here
```

10. Create a superuser:

```bash
python manage.py user -createsuperuser
```

## Django applications

**There are 4 django applications in this Django rest project:**

### *CustomUser*

- This application contains the models and model managers for users (*CustomUserAccount* and *CustomUserAccountManager*), teams (*Team* and *TeamManager*) and a model for a custom token (*CustomToken*).

- **This application also containes three command manager files :**

1. user.py : to manage CRUD operations for users (*CustomUserAccount* and *CustomUserAccountManager*).
2. authentication.py : to manage the login and logout using a custom token system.
3. team.py : to manage the CRUD operations for teams (*CustomTeam* and *CustomTeamManager*).

### *Client*

- This application contains the models and model managers for clients (*Client* and *ClientManager*).

- **This application also containes one command manager files :**

1. client.py : to manage CRUD operations for clients (*Client* and *ClientManager*).

### *Contract*

- This application contains the models and model managers for contracts (*Contract* and *ContractManager*).

- **This application also containes one command manager files :**

1. contract.py : to manage CRUD operations for contracts (*Contract* and *ContractManager*).

### *Event*

- This application contains the models and model managers for events (*Event* and *EventManager*).

- **This application also containes one command manager files :**

1. event.py : to manage CRUD operations for events (*Event* and *EventManager*).

## Commands

**All commands starts with :**

```bash
python manage.py
```

*After each sent command, follow the prompt instructions.*

## CustomUser

### user commands

**List users : List all users in the system:**

```bash
python manage.py user -list
```

**Create user : Create a normal user:**

```bash
python manage.py user -create
```

**Create superuser : Create a superuser:**

```bash
python manage.py user -createsuperuser
```

**Delete user : Delete a user:**

```bash
python manage.py user -delete
```

**Update user : Update a user:**

```bash
python manage.py user -update
```

**Read user : Read and display detailed information about a user:**

```bash
python manage.py user -read
```

### authentication commands

**Login : login with username and password:**

```bash
python manage.py authentication -login
```

**Logout : logout with username and password:**

```bash
python manage.py authentication -logout
```

### team commands

**List teams : List all teams in the system:**

```bash
python manage.py team -list
```

**Create team : Create a team:**

```bash
python manage.py team -create
```

**Delete user : Delete a team:**

```bash
python manage.py team -delete
```

**Update user : Update a team:**

```bash
python manage.py team -update
```

**Read user : Read and display detailed information about a team:**

```bash
python manage.py team -read
```

## Client

### client commands

**List clients : List all clients in the system:**

```bash
python manage.py client -list
```

**Create client : Create a client:**

```bash
python manage.py client -create
```

**List contact clients : List all clients in the system that are linked to the current user:**

```bash
python manage.py client -list_contact_clients
```

**Delete client : Delete a client:**

```bash
python manage.py client -delete
```

**Update client : Update a client:**

```bash
python manage.py client -update
```

**Read client : Read and display detailed information about a client:**

```bash
python manage.py client -read
```

## Contract

### contract commands

**List contracts : List all contracts in the system:**

```bash
python manage.py contract -list
```

**Create contract : Create a contract:**

```bash
python manage.py contract -create
```

**List contact contracts : List all not signed or none fully payed for contracts that are linked to the current user.**

```bash
python manage.py contract -list_contact_contracts
```

**Delete contract : Delete a client:**

```bash
python manage.py contract -delete
```

**Update contract : Update a client:**

```bash
python manage.py contract -update
```

**Read contract : Read and display detailed information about a client:**

```bash
python manage.py contract -read
```

## Event

### event commands

**List events : List all events in the system:**

```bash
python manage.py event -list
```

**Create event : Create a event:**

```bash
python manage.py event -create
```

**List contact events : List all events in the system that are linked to the current user:**

```bash
python manage.py event -list_contact_events
```

**Delete event : Delete a event:**

```bash
python manage.py event -delete
```

**Update event : Update a event:**

```bash
python manage.py event -update
```

**Read event : Read and display detailed information about a event:**

```bash
python manage.py event -read
```

## Tests

**The tests are made with django testing framework.**

### Run all tests

*Run tests for the whole project:*

```bash
python manage.py test
```

### Run tests for each django app

*Run tests for CustomUser:*

```bash
python manage.py test CustomUser
```

*Run tests for Client:*

```bash
python manage.py test Client
```

*Run tests for Contract:*

```bash
python manage.py test Contract
```

*Run tests for Event:*

```bash
python manage.py test Event
```

## Run coverage test

*Run the coverage test:*

```bash
coverage run manage.py test
```

*Get the test result:*

```bash
coverage report
```

or

```bash
coverage html
```
