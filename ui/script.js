// =========================================================
// 🔥 GLOBAL SAFE CHAT FUNCTION FIX
// =========================================================

// 🔥 backward compatibility
function addMessage(msg){
    return window.addMessage(msg);
}

// 🔥 safe global
window.addMessage = function(msg){

    try{

        let chat = document.getElementById("chat");

        if(!chat) return;

        if(!msg) return;

        // 🔥 limit message size
        if(msg.length > 300){
            msg = msg.substring(0,300) + "...";
        }

        let div = document.createElement("div");

        div.className = "chat-message";

        div.innerText = msg;

        chat.appendChild(div);

        // 🔥 auto remove old messages
        while(chat.children.length > 20){
            chat.removeChild(chat.firstChild);
        }

        // 🔥 smooth scroll
        chat.scrollTo({
            top: chat.scrollHeight,
            behavior: "smooth"
        });

    }catch(e){

        console.log("addMessage error:", e);
    }
};


// =========================================================
// 🔥 VARIABLES
// =========================================================
let bridge = null;

const canvas = document.getElementById("hudCanvas");

const ctx = canvas ? canvas.getContext("2d") : null;

let angle = 0;


// =========================================================
// 🔥 SAFE DOM GET
// =========================================================
function $(id){
    return document.getElementById(id);
}


// =========================================================
// 🔥 SAFE CANVAS RESIZE
// =========================================================
function resizeCanvas(){

    if(!canvas) return;

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

resizeCanvas();

window.addEventListener("resize", resizeCanvas);


// =========================================================
// 🔥 HUD DRAW
// =========================================================
function draw(){

    if(!ctx || !canvas) return;

    ctx.clearRect(0,0,canvas.width,canvas.height);

    let cx = canvas.width / 2;
    let cy = canvas.height / 2;

    ctx.lineWidth = 2;

    // =====================================================
    // 🔥 OUTER ARC
    // =====================================================
    ctx.strokeStyle = "#00ffff";

    ctx.beginPath();

    ctx.arc(
        cx,
        cy,
        160,
        angle,
        angle + Math.PI * 1.5
    );

    ctx.stroke();

    // =====================================================
    // 🔥 SECOND ARC
    // =====================================================
    ctx.strokeStyle = "rgba(0,255,255,0.3)";

    ctx.beginPath();

    ctx.arc(
        cx,
        cy,
        200,
        -angle,
        -angle + Math.PI
    );

    ctx.stroke();

    // =====================================================
    // 🔥 CENTER GLOW
    // =====================================================
    let grad = ctx.createRadialGradient(
        cx,
        cy,
        0,
        cx,
        cy,
        120
    );

    grad.addColorStop(0,"rgba(0,255,255,0.5)");
    grad.addColorStop(1,"transparent");

    ctx.fillStyle = grad;

    ctx.beginPath();

    ctx.arc(cx,cy,120,0,Math.PI*2);

    ctx.fill();

    // 🔥 rotation speed
    angle += 0.015;

    requestAnimationFrame(draw);
}


// =========================================================
// 🔥 UI INIT
// =========================================================
window.onload = function(){

    try{

        // 🔥 start HUD
        draw();

        // =================================================
        // 🔥 SAFE QWEBCHANNEL INIT
        // =================================================
        if(window.qt && qt.webChannelTransport){

            new QWebChannel(
                qt.webChannelTransport,

                function(channel){

                    bridge = channel.objects.bridge;

                    console.log("✅ Bridge Connected");
                }
            );
        }

        // =================================================
        // 🔥 COMMAND INPUT
        // =================================================
        const cmdInput = $("cmd");

        if(cmdInput){

            cmdInput.addEventListener("keydown", function(e){

                if(e.key === "Enter"){

                    let cmd = this.value.trim();

                    if(!cmd) return;

                    this.value = "";

                    // 🔥 show user message
                    addMessage("You: " + cmd);

                    // 🔥 send to python
                    if(bridge){

                        bridge.sendCommand(cmd);

                    }else{

                        console.log("Bridge not connected");
                    }
                }
            });
        }

        // =================================================
        // 🔥 LIVE CLOCK
        // =================================================
        setInterval(()=>{

            const timeEl = $("time");

            if(timeEl){

                timeEl.innerText =
                    new Date().toLocaleTimeString();
            }

        },1000);

        console.log("✅ UI Loaded");

    }catch(e){

        console.log("UI Init Error:", e);
    }
};


// =========================================================
// 🔥 SYSTEM STATS
// =========================================================
function updateSystemStats(data){

    try{

        let [cpu,ram,battery] = data.split("|");

        if($("cpu")){
            $("cpu").innerText = cpu + "%";
        }

        if($("ram")){
            $("ram").innerText = ram + "%";
        }

        if($("battery")){
            $("battery").innerText = battery + "%";
        }

    }catch(e){

        console.log("Stats Error:", e);
    }
}


// =========================================================
// 🔥 VOICE START ANIMATION
// =========================================================
function startVoiceAnimation(){

    try{

        const ring = $("voiceRing");

        if(ring){

            ring.style.transform =
                "translate(-50%, -50%) scale(1.3)";

            ring.style.boxShadow =
                "0 0 60px cyan";
        }

    }catch(e){}
}


// =========================================================
// 🔥 VOICE STOP ANIMATION
// =========================================================
function stopVoiceAnimation(){

    try{

        const ring = $("voiceRing");

        if(ring){

            ring.style.transform =
                "translate(-50%, -50%) scale(1)";

            ring.style.boxShadow =
                "0 0 20px cyan";
        }

    }catch(e){}
}

// =========================================================
// 🔥 NOVA MODES
// =========================================================

function setListeningMode(){

    const wave = document.querySelector(".voice-wave");
    const ring = document.querySelector(".voice-ring");

    if(wave){
        wave.classList.add("listening");
    }

    if(ring){
        ring.classList.remove(
            "speaking",
            "processing"
        );
    }
}


function setSpeakingMode(){

    const wave = document.querySelector(".voice-wave");
    const ring = document.querySelector(".voice-ring");

    if(wave){
        wave.classList.remove("listening");
    }

    if(ring){
        ring.classList.remove("processing");
        ring.classList.add("speaking");
    }
}


function setProcessingMode(){

    const wave = document.querySelector(".voice-wave");
    const ring = document.querySelector(".voice-ring");

    if(wave){
        wave.classList.remove("listening");
    }

    if(ring){
        ring.classList.remove("speaking");
        ring.classList.add("processing");
    }
}


function setIdleMode(){

    const wave = document.querySelector(".voice-wave");
    const ring = document.querySelector(".voice-ring");

    if(wave){
        wave.classList.remove("listening");
    }

    if(ring){
        ring.classList.remove(
            "speaking",
            "processing"
        );
    }
}