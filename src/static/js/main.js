const BOT_IMG = "https://img.icons8.com/fluency-systems-regular/48/bot--v1.png";
const PERSON_IMG =
  "https://img.icons8.com/puffy/64/experimental-user-puffy.png";
let BOT_NAME = "{{ config.bot }}";
const PERSON_NAME = "Você";

const setConfig = (config) => {
  BOT_NAME = config.bot;
};

const get = (selector, root = document) => root.querySelector(selector);

const formatDate = (date) => {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();
  return `${h.slice(-2)}:${m.slice(-2)}`;
};

const delay = async (time) => {
  return await new Promise((resolve) => setTimeout(resolve, time));
};

const inputFilled = () => {
  return document.getElementById('textInput').value
}

const inputFill = (value) => {
  document.getElementById('textInput').value = value;
  document.getElementById('textInput').focus()
}

const appendMessage = ({
  name = BOT_NAME,
  img = BOT_IMG,
  side = "left",
  text,
}) => {
  const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-img" style="background-image: url(${img})"></div>
      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${formatDate(new Date())}</div>
        </div>
        <div class="msg-text">${text}</div>
      </div>
    </div>
  `;
  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop += 500;
};

const appendMenu = ({
  side = "right",
  action="inputFill",
  label, 
}) => {
  if(action === "inputFill"){
    const msgHTML = `
      <div class="msg ${side}-msg btn">
        <div class="msg-bubble btn">
          <div class="msg-text btn" onclick="inputFill('${label}: ')">${label}</div>
        </div>
      </div>
    `;
    msgerChat.insertAdjacentHTML("beforeend", msgHTML);
    msgerChat.scrollTop += 500;
  }
};

const botResponse = (rawText) => {
  return new Promise((resolve, reject) => {
    $.ajax({
      url: "/message",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify({ message: rawText }),
      success: (data) => resolve(data),
      error: (error) => {
        const errorMessage = error.message
          ? error.message
          : error.statusText || "Internal Server Error";
        console.error(errorMessage);
        resolve({
          message:
            "Desculpe, tive um problema para te responder :( \nRepete por favor ou tente mais tarde",
          tag: "error",
        });
      },
    });
  });
};

const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");
const msgerSendBtn = get(".msger-send-btn");

msgerInput.addEventListener('input', function() {
  if (msgerInput.value.trim() !== '') {
    msgerSendBtn.removeAttribute('disabled');
  } else {
    msgerSendBtn.setAttribute('disabled', '');
  }
});

msgerForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const msgUser = msgerInput.value;
  appendMessage({
    name: PERSON_NAME,
    img: PERSON_IMG,
    side: "right",
    text: msgUser,
  });
  msgerInput.value = "";
  msgerSendBtn.setAttribute('disabled', '');
  const responseBot = await botResponse(msgUser).then((data) => data);
  const msgBot = responseBot.message.split("\n");
  msgBot.forEach((msg) => {
    const button = msg.match(/<(.*)>/)
    if(button){
      const buttonContent = button[1]
      appendMenu({
        side: "left",
        action: "inputFill",
        label: buttonContent
      });
    }else{
      appendMessage({
        name: BOT_NAME,
        img: BOT_IMG,
        side: "left",
        text: msg,
      });
    }
  });
  const commandBot = responseBot.command;
  if (commandBot) {
    switch(commandBot.name){
      case "redirect": {
        await delay(2500);
        window.open(commandBot.param[0])
      }
    }
  }
});
