// bot.js
import venom from "venom-bot";
import { handleMessage } from "./handlers.js";

venom
  .create(
    "session", // Nome da sessão
    (base64Qrimg, asciiQR, attempts, urlCode) => {
      console.log("Escaneie este QR Code:");
      console.log(asciiQR); // QR Code no terminal
    },
    undefined, // Pasta de sessão (deixe undefined para padrão)
    {
      headless: false, // Chrome visível
      useChrome: true,
      browserArgs: ["--no-sandbox", "--disable-setuid-sandbox"]
    }
  )
  .then(client => start(client))
  .catch(error => console.log("Erro ao iniciar o bot:", error));

function start(client) {
  console.log("Bot rodando! Aguardando mensagens...");

  // Evento de recebimento de mensagem
  client.onMessage(message => {
    if (!message.body) return; // Ignora mensagens sem corpo
    console.log("Mensagem recebida de", message.from, ":", message.body);

    // Chama o handler para responder
    handleMessage(client, message);
  });
}
