Feature: US10 - Control de gastos por cultivo

  Scenario: Reporte de gastos acumulados
    Given que el usuario selecciona un cultivo, 
    When accede al panel financiero, 
    Then visualiza un resumen de todos los gastos realizados con fechas, conceptos y montos.

    Examples:
    
    | Seleccion de cultivo | Cultivo Seleccionado |
    | Periodo deseado | Fecha inicio ded periodo | Fecha final del periodo |

    | Tabla dada en el Reporte |
    | Concepto de gasto | Monto del consepto |
    | Concepto de gasto N°1 | Monto del consepto N°1 |
    | Concepto de gasto N°2 | Monto del consepto N°2 |
    | Concepto de gasto N°3 | Monto del consepto N°3 |
    | Inversión total | Monto total invertido |
