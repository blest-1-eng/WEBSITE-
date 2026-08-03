const input = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const messages = document.getElementById("messages");

function addUser(text){

    messages.innerHTML += `
    <div class="user">${text}</div>
    `;

    messages.scrollTop = messages.scrollHeight;
}

function addBot(text){

    messages.innerHTML += `
    <div class="bot">${text}</div>
    `;

    messages.scrollTop = messages.scrollHeight;
}

async function sendMessage(){

    const text = input.value.trim();

    if(!text) return;

    addUser(text);

    input.value = "";

    addBot("Typing...");

    const typing = document.querySelector(".bot:last-child");

    try{

        const res = await fetch("http://127.0.0.1:5000/chat",{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                message:text
            })

        });

        const data = await res.json();

        typing.innerHTML = data.reply;

let speech = new SpeechSynthesisUtterance(data.reply);

speech.lang = "hi-IN";

speech.rate = 1;

speech.pitch = 1.2;

speechSynthesis.speak(speech);

    }

    catch(e){
    console.log(e);
    typing.innerHTML = "ERROR: " + e;
}

}

window.onload = () => {

    const input = document.getElementById("messageInput");
    const sendBtn = document.getElementById("sendBtn");

    sendBtn.onclick = sendMessage;

    input.addEventListener("keypress", (e) => {

        if (e.key === "Enter") {
            sendMessage();
        }

    });

};
