# Bot Features

### Add Company

Params: `company_id, interval, request_method, error_codes.`

Aciona o monitoramento de uma company, dado um tempo de inicio e término e código de resposta. Assim, quando uma request que cumpre as características enviadas na assinatura forem atendidas, um alerta é enviado.

Resposta individual à quem executou o comando.

### Remove Company

Params: `company_id`

Desabilita o monitoramento de uma company dado um ID pré-cadastrado.

Resposta de confirmação ao usuário que executou o comando.

### Deploy Mode

Params: não tem

Altera os parâmetros que definem quando um alerta será enviado ou não (para qualquer company).

Exemplo:
```
Antes:
Enviar quando houver erro em 50% das requests da última hora

Depois:
Enviar quando houver erro em 25% das requests da última hora
```
