# {{project_name}}

{{short_description}}

## Quick Start

First, start two terminal screen T1(client), T2(server)

### Build

``` bash
git clone https://github.com/{{github_username}}/{{project_slug}}

# T1
cd client
npm i

# T2
cd server
pipenv install --dev
pipenv shell
```

### Database Migration

``` bash
# T2
flask db init
flask db migrate
flask db upgrade
```

### Run

Run backend

``` bash
# T2
flask run
```

Run frontend

``` bash
# T1
npm run serve
```