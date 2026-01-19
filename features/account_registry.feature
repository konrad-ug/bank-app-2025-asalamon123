Feature: Account registry

Scenario: User is able to create 2 accounts
    Given The account registry is empty
    When I create an account using name: "kurt", last name: "cobain", pesel: "89092909246"
    And I create an account using name: "tadeusz", last name: "szcześniak", pesel: "791010112345"
    Then Number of accounts in registry equals: "2"
    And Account with pesel "89092909246" exists in registry
    And Account with pesel "791010112345" exists in registry

Scenario: User is able to update surname of already created account
    Given Account registry is empty
    And I create an account using name: "nata", last name: "haydamaky", pesel: "95092909876"
    When I update "surname" of account with pesel: "95092909876" to "filatov"
    Then Account with pesel "95092909876" has "surname" equal to "filatov"

Scenario: User is able to update name of already created account
    Given Account registry is empty
    And I create an account using name: "ola", last name: "kowalska", pesel: "93010112345"
    When I update "name" of account with pesel: "93010112345" to "anna"
    Then Account with pesel "93010112345" has "name" equal to "anna"

Scenario: Created account has all fields correctly set
    Given Account registry is empty
    And I create an account using name: "jan", last name: "kowalski", pesel: "92020212345"
    Then Account with pesel "92020212345" has "name" equal to "jan"
    And Account with pesel "92020212345" has "surname" equal to "kowalski"
    And Account with pesel "92020212345" exists in registry
    
Scenario: User is able to delete created account
    Given Account registry is empty
    And I create an account using name: "parov", last name: "stelar", pesel: "01092909876"
    When I delete account with pesel: "01092909876"
    Then Account with pesel "01092909876" does not exist in registry
    And Number of accounts in registry equals: "0"