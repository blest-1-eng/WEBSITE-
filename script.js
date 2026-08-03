// ==============================
// NYRA AI SCRIPT
// ==============================

// Mouse Glow
const cursor = document.getElementById("cursor");

document.addEventListener("mousemove", (e) => {
    cursor.style.left = e.clientX - 12 + "px";
    cursor.style.top = e.clientY - 12 + "px";
});

// ==============================
// Typing Animation
// ==============================

const typing = document.getElementById("typing");

const words = [
    "Your Personal AI Assistant",
    "Powered by Artificial Intelligence",
    "Voice • Vision • Memory",
    "Future of Smart Assistance"
];

let wordIndex = 0;
let charIndex = 0;
let deleting = false;

function typeEffect(){

    const current = words[wordIndex];

    if(!deleting){

        typing.textContent = current.substring(0,charIndex++);

        if(charIndex > current.length){

            deleting = true;

            setTimeout(typeEffect,1200);

            return;

        }

    }

    else{

        typing.textContent = current.substring(0,charIndex--);

        if(charIndex < 0){

            deleting = false;

            wordIndex++;

            if(wordIndex >= words.length){

                wordIndex = 0;

            }

        }

    }

    setTimeout(typeEffect,deleting?35:70);

}

typeEffect();


// ==============================
// Particle Background
// ==============================

tsParticles.load("particles",{

    background:{
        color:"#050816"
    },

    fpsLimit:60,

    particles:{

        number:{
            value:70
        },

        color:{
            value:"#00ffff"
        },

        links:{
            enable:true,
            distance:160,
            color:"#00ffff",
            opacity:.3,
            width:1
        },

        move:{
            enable:true,
            speed:2
        },

        size:{
            value:2
        },

        opacity:{
            value:.6
        }

    }

});

// ==============================
// Launch Button Animation
// ==============================

const launchBtn = document.querySelector(".launch");

launchBtn.addEventListener("mouseenter",()=>{

    launchBtn.style.transform="scale(1.08)";
    launchBtn.style.boxShadow="0 0 40px cyan";

});

launchBtn.addEventListener("mouseleave",()=>{

    launchBtn.style.transform="scale(1)";
    launchBtn.style.boxShadow="0 0 0px cyan";

});

launchBtn.addEventListener("click",()=>{

    launchBtn.innerHTML="<i class='fa-solid fa-spinner fa-spin'></i> Launching...";

    setTimeout(()=>{

        window.location.href="chat.html";

    },1200);

});


// ==============================
// Fade Animation
// ==============================

const observer=new IntersectionObserver(entries=>{

entries.forEach(entry=>{

if(entry.isIntersecting){

entry.target.style.opacity="1";

entry.target.style.transform="translateY(0px)";

}

});

});

document.querySelectorAll(".card,.about").forEach(el=>{

el.style.opacity="0";

el.style.transform="translateY(60px)";

el.style.transition=".8s";

observer.observe(el);

});


// ==============================
// Avatar Glow Pulse
// ==============================

const avatar=document.querySelector(".avatar-box");

setInterval(()=>{

avatar.animate([

{

boxShadow:"0 0 20px cyan"

},

{

boxShadow:"0 0 60px cyan"

},

{

boxShadow:"0 0 20px cyan"

}

],{

duration:2500

});

},2500);


// ==============================
// Navbar Blur On Scroll
// ==============================

window.addEventListener("scroll",()=>{

const nav=document.querySelector("nav");

if(window.scrollY>50){

nav.style.background="rgba(5,10,25,.75)";
nav.style.backdropFilter="blur(20px)";

}

else{

nav.style.background="rgba(255,255,255,.05)";

}

});


// ==============================
// Hero Fade In
// ==============================

window.onload=()=>{

document.querySelector(".hero").animate([

{

opacity:0,

transform:"translateY(40px)"

},

{

opacity:1,

transform:"translateY(0px)"

}

],{

duration:1200,

fill:"forwards"

});

};
