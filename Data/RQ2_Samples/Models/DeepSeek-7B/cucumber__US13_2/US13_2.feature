Feature: US13 - Accesibilidad y navegación inicial

  Scenario: Ver detalles de una planta
    Given que el usuario encuentre la planta buscada en el navegador, 
    When haga click en la planta deseada,
    Then le abrirá una página detallada sobre las necesidades y propiedades de esta planta.

    Examples:

    | Nombre de la planta seleccionada |
    | Foto de la plaanta seleccionada |
    | Datos basicos |
    | Necesidades de la planta |
    | Datos especificos de la planta |
