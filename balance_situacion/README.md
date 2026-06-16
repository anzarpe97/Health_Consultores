# Balance de Situación - CONVECA
**Módulo Odoo 17** · `balance_situacion_conveca`

## Descripción
Genera el reporte **Balance de Situación** en PDF con el formato usado por
**CONSTRUCTORES VENEZOLANOS, C.A.**, incluyendo saldos en Bolívares (Bs.) y la
estructura jerárquica exacta visible en el reporte original.

---

## Instalación
1. Copiar la carpeta `balance_situacion_conveca` en el directorio `addons` de tu instancia Odoo 17.
2. Reiniciar el servidor Odoo.
3. Activar el **modo desarrollador** (Settings → Activate developer mode).
4. Ir a **Apps**, buscar _"Balance de Situación"_ e instalar.

---

## Uso
1. Ir a **Contabilidad → Reportes → Balance de Situación**.
2. Configurar los filtros en el wizard:
   - **Empresa** y **fecha corte** (obligatorio).
   - Diarios específicos (opcional).
   - Activar/desactivar "Solo asientos publicados" y "Accrual Basis".
3. Hacer clic en **Generar PDF**.

---

## Estructura del reporte
```
ACTIVOS                                  2.736.827.354,74 Bs.
  Activos corrientes                     2.736.827.354,74 Bs.
    Cuentas bancarias y en efectivo         13.353.201,31 Bs.
    Por cobrar                           2.211.622.424,46 Bs.
    Activos corrientes                     511.851.728,97 Bs.
    Prepagos
  Activos adicionales fijos
  Activos no corrientes extras
PASIVOS                                  1.749.811.907,76 Bs.
  Pasivos corrientes                     1.749.811.907,76 Bs.
    Pasivos corrientes                   1.268.045.582,84 Bs.
    Por pagar                              481.766.324,92 Bs.
  Pasivos adicionales no corrientes
CAPITAL                                    987.015.446,98 Bs.
  Ganancias sin asignar                   987.015.446,98 Bs.
    Ganancias no asignadas del año actual  987.492.451,57 Bs.
      Ganancias del año actual             987.492.451,57 Bs.
      Ganancias asignadas del año actual
    Ganancias no asignados de años ant.       -477.004,59 Bs.
  Ganancias acumuladas
PASIVOS + CAPITAL                        2.736.827.354,74 Bs.
```

---

## Dependencias
- `account`
- `account_reports`

## Notas de configuración contable
El módulo mapea los saldos usando los **tipos de cuenta** (`account.account.type`) de Odoo:

| Sección del balance          | Tipo de cuenta Odoo         |
|------------------------------|-----------------------------|
| Cuentas bancarias            | `asset_cash`                |
| Por cobrar                   | `asset_receivable`          |
| Activos corrientes (otros)   | `asset_current`             |
| Prepagos                     | `asset_prepayments`         |
| Activos fijos                | `asset_fixed`               |
| Activos no corrientes extras | `asset_non_current`         |
| Pasivos corrientes (otros)   | `liability_current`         |
| Por pagar                    | `liability_payable`         |
| Pasivos no corrientes        | `liability_non_current`     |
| Ganancias del año            | `income`, `income_other`    |
| Ganancias años anteriores    | `equity_unaffected`         |
| Ganancias acumuladas         | `equity`                    |

> Si el plan de cuentas venezolano usa prefijos numéricos (ej. 1.1 = Activo Corriente),
> el método `_balance_by_account_codes()` en `models/balance_situacion.py` permite
> filtrar por prefijo de código de cuenta alternativamente.
