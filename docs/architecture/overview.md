# Arquitetura

O fluxo principal é:

`client -> API gateway -> auth/classification/DLP -> policy -> model router -> provider -> tool gateway -> output validation -> audit/telemetry`.

Os módulos ofensivos executam contra fixtures locais e produzem achados normalizados. Adapters externos são opt-in e desabilitados no MVP.

