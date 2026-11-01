Feature: US10 - Control de gastos por cultivo

  Scenario: Ingreso de gastos individuales
    Given que el usuario compró fertilizante,
    When registra “Compra de fertilizante – S/ 150” en el cultivo de papa, 
    Then el gasto se asocia a ese cultivo y se suma al total invertido.

    Examples:

    | Cultivos asociados | Cultivo 1 | Cultivo 2 | ... |
    | Concepto de gasto N°1 | Monto de gasto |
    | Concepto de gasto N°2 | Monto de gasto |
    | Concepto de gasto N°3 | Monto de gasto |

    | Registro de gastos en la base de datos | Actualización ddel total invertido |
