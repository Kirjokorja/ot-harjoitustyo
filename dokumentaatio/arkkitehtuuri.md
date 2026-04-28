# Arrkkitehtuurin kuvaus

## Rakenne

Ohjelma koostuu neljästä tasosta:

1. Käyttöliittymä (ui-pakkaus)
2. Palvelu (services-pakkaus)
3. Varastointi (repositories-pakkaus)
4. Tietokanta (database-pakkaus)

Lisäksi tiedon siirtoon ja käsittelyyn käytetään luokkia entities-pakkauksesta. Jokainen taso käyttää yhtä alempaa tasoa toimituksissaan.

## Sovelluslogiikka

Sovelluksen loogisesta toiminnasta vastaavat luokat Services, ServiceBase, UserService, ProjectService ja PasswordService. UserService ja ProjectService perivät luokan ServiceBase, jossa on niiden jakamat attribuutit ja metodit. 

Services-luokkalle ujutetaan konstruktorin kautta UserService- ja ProjeService-oliot. Services-luokka tarjoaa rajapinnan kutsua sisältämiensä palvelujen metodeja kauttaan. 

UserService-luokkalle ujutetaan konstruktorin kautta PasswordService-luokka, jota se käyttä käyttäjän salasanojen käsittelyssä. Luokalla on myös attribuuttina User-luokan olio, johon tallennetaan istunnon ajaksi kirjautuneen käyttäjän tiedot, ja josta sovellus tarkistaa istunnon tietoja. UserService käyttää konstruktorin kautta ujutettua UserRepository-luokan oliota käyttäjän tietojen tallentamiseen ja hakemiseen tietokannasta. Käyttäjien tietojen manipulointiin ja siirtämiseen luokka käyttää User-luokan olioita.

ProjectService-luokka vastaa maailmojen/hankkeiden käsittelystä ja käyttää ProjectRepository-luokan oliota, joka ujutetaan sille konstruktorin kautta, hankkeiden tietojen tallentamiseen ja hakemiseen tietokannasta. Hankkeiden tietojen käsittelyssä ja siirrossa palvelu käyttää Project-luokkaa, jonka attribuuteista löytyvät TypeClass- ja User-luokat. 

## Luokkakaavio

```mermaid
classDiagram
    Services "1" o-- "1" UserService
    Services "1" o-- "1" ProjectService
    ServiceBase <|-- UserService
    ServiceBase <|-- ProjectService
    UserService "1" o-- "1" PasswordService
    UserService "1" o-- "1" User
    UserService "1" o-- "1" UserRepository
    ProjectService "1" o-- "1" ProjectRepository
    RepositoryBase <|-- UserRepository
    RepositoryBase <|-- ProjectRepository
    UserRepository "1" o-- "1" DatabaseInterface
    Project o-- User
    Project o-- TypeClass
    User <.. UserRepository
    User <.. UserService
    Project <.. ProjectRepository
    Project <.. ProjectService
    TypeClass <.. ProjectService
    class Services{
        -_user_service: UserService
        -_project_service: ProjectService
        +Services(user_service: UserService, project_service: ProjectService)
        +get_user_service() UserService
        +get_project_service() ProjectService
    }
    class ServiceBase{
        -_repository: RepositoryBase
        ~_exceptions: exceptions
        +ServiceBase(repository: RepositoryBase, exceptions)
        +get_exceptions() exceptions
    }
    class UserService{
        ^-_repository: UserRepository
        ^~_exceptions: exceptions
        -_password_service: PasswordService
        -_user: User
        -_username_acceptable(username: String) bool
        -_password_acceptable(password: String, password_confirm: String) bool
        +UserService(user_repository: UserRepository, exceptions, password_service: PasswordService)
        +create_user(username: String, password: String, password_confirm: String) User
        +login(username: String, password: String) void
        +get_current_user() User
        +get_min_password_lenght() String
    }
    class ProjectService{
        ^-_repository: ProjectRepository
        ^~_exceptions: exceptions
        -_project_acceptable(title: String, p_type: TypeClass, owner: User) bool
        +ProjectService(repository: ProjectRepository, exceptions)
        +get_project_classes(title: String) list~TypeClass~
        +create_project(title: String, p_type: TypeClass, description: String, owner: User) Project
        +save_project(project: Project) Project
        +remove_project(user: User, project: Project) void
    }
    class PasswordService{
        +PasswordService()
        +hash_password()
        +password_match()
        +password_long_enough()
        +get_min_password_lenght()
    }
    class User{
        +u_id: int
        +username: String
        +password: String
        +User(user_id: int, username: String, password: String)
    }
    class Project{
        +p_id: int
        +title: String
        +p_type: TypeClass
        +description: String
        +owner: User
        +Project(params: dict~String, value~)
    }
    class TypeClass{
        +t_id: int
        +title: String
        +value: String
    }
    class RepositoryBase{
        -_db: DatabaseInterface
        -_get_class_from_row(row: sqlite3.Row) TypeClass
        -_get_classes_from_rows(list~sqlite3.row~) list~sqlite3.Row~
        +RepositoryBase(db: DatabaseInterface)
        +get_classes(title: String) list~TypeClass~
    }
    class UserRepository{
        ^-_db: DatabaseInterface
        -_get_user_from_row(row: sqlite3.Row) User
        -_get_users_from_rows(rows: List~sqlite3.Row~) List~User~ 
        +UserRepository(db: DatabaseInterface)
        +find_user_by_name(username: String) User
        +add_user(user: User) User
    }
    class ProjectRepository{
        ^-_db: DatabaseInterface
        +ProjectRepository(db: DatbaseInterface)
        +add_project(project: Project) Project
        +edit_project(project: Project) Project
        +delete_project(project_id: Project) void
    }
    class DatabaseInterface{
        -_file_path: String
        +DatabaseInterface(file_path: String)
        -_get_connection() sqlite3.Connection
        +query(sql: String, params: List~String~) List~sqlite3.Row~
        +execute(sql: String, params: List~String~) int
        +executemany(sql: String, params: List~String~) void
        +executescript(statments: String) void
    }
```

## Käyttäjän luonnin sekvenssikaavio

```mermaid
sequenceDiagram
    actor User
    participant UI
    participant Services
    participant UserService
    participant aino
    participant UserRepository
    participant DatabaseInterface

    User->>UI: painaa "Luo" painiketta

    activate UI
    UI->>Services: get_user_service()

    activate Services
    Services->>UserService: create_user("Aino", "HaeTurvapaikkaaAhtolasta!!!!", "HaeTurvapaikkaaAhtolasta!!!!")
    
    activate UserService
    UserService->>UserRepository: find_user_by_name("Aino")
    
    activate UserRepository
    UserRepository->>DatabaseInterface: query("SELECT id, username, password_hash FROM Users WHERE username = ?", ["Aino"])
    
    activate DatabaseInterface
    DatabaseInterface-->>UserRepository: list(None)
    deactivate DatabaseInterface

    UserRepository-->>UserService: None
    deactivate UserRepository

    UserService->>aino: User("Aino", "HaeTurvapaikkaaAhtolasta!!!!")UserService->>UserRepository: add_user(aino)
    UserService->>UserRepository: add_user(aino)

    activate UserRepository
    UserRepository->>DatabaseInterface: execute("INSERT INTO Users (username, password_hash) VALUES (?, ?)", ["Aino", "HaeTurvapaikkaaAhtolasta!!!!"])
    
    activate DatabaseInterface
    DatabaseInterface-->>UserRepository: id
    deactivate DatabaseInterface

    UserRepository->>aino: id
    UserRepository-->>UserService: aino
    deactivate UserRepository

    UserService-->>Services: aino
    deactivate UserService

    Services-->>UI: aino
    deactivate Services

    UI-->>User: _show_login_view()
    deactivate UI
  ```
