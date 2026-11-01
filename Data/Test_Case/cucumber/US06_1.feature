Feature: US06 - Alertas Automatizadas sobre condiciones críticas

  Scenario: Alerta por enfermedad detectada
    Given que el sistema detecta una enfermedad potencial, 
    When el nivel de riesgo supera el umbral,
    Then se envía una alerta al celular del usuario.

    Examples:

    | Datos de los sensoers e imagenes del cultivo |
    | Detección de estado anormal en el cultivo | Busqueda de enfermedad o plaga en el cultivo |
    | Enfermedad o plaga especifica detectada | Notificar al usuario sobre la plaga o enfermedad |

    | Alerta de notificacion al Usuario: |
    | Plaga/Enfermedad detectada en sus cultivos, revisar datos de la plaga/enfermedad |
    
