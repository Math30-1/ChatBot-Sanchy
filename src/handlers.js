// handlers.js
export function handleMessage(client, message) {
  const msg = message.body.toLowerCase();

  if (msg === "oi") {
    client.sendText(message.from, "Olá! Como posso ajudar?");
  } else {
    client.sendText(message.from, "Mensagem recebida!");
  }
}

