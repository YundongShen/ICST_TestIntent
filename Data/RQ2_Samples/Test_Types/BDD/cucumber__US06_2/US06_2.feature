Feature: US06 - Alertas Automatizadas sobre condiciones críticas

  Scenario: Alerta por evento climático
    Given que se pronostica una helada, 
    When el evento se acerca, 
    Then se envía una notificación para prevenir daños.

    Examples:
    
    | Pronostico climatico con evento extremo resivido |
    | Notificar al usuario sobre el pronostico climaco con un evento extremo |

    | Alerta de notificacion al Usuario: |
    | Pronostico climatico extremo en la zona de cultivo, revise las medidas preventivas para perdias minimas en tus cultivos |    
