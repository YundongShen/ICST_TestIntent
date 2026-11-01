Feature: US13 - Accesibilidad y navegación inicial

  Scenario: Navegador de diferentes cultivos
    Given que el usuario quiera ver detalles de una planta en específico, 
    When entre al navegar de cultivos y escriba el nombre de la planta, 
    Then le aparecerá una lista de plantas cuyo nombre coincide.

    Examples:
    
    | Planta buscada en el navegador|Filtro: plantas|Buscar|

    | Foto basica de planta 1 | Nombre de planta 1 | Datos basicos de de planta 1 |
    | Foto basica de planta 2 | Nombre de planta 2 | Datos basicos de de planta 2 |
    | Foto basica de planta 3 | Nombre de planta 3 | Datos basicos de de planta 3 |
    | Foto basica de planta 4 | Nombre de planta 4 | Datos basicos de de planta 4 |
