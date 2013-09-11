function getTime() {
c1 = new Image(); c1.src = "/static/images/1.png";
c2 = new Image(); c2.src = "/static/images/2.png";
c3 = new Image(); c3.src = "/static/images/3.png";
c4 = new Image(); c4.src = "/static/images/4.png";
c5 = new Image(); c5.src = "/static/images/5.png";
c6 = new Image(); c6.src = "/static/images/6.png";
c7 = new Image(); c7.src = "/static/images/7.png";
c8 = new Image(); c8.src = "/static/images/8.png";
c9 = new Image(); c9.src = "/static/images/9.png";
c0 = new Image(); c0.src = "/static/images/0.png";
Cc = new Image(); Cc.src = "Cc.gif";
now = new Date();
later = new Date("Sept 1 2010 00:00:00");
days = (later - now) / 1000 / 60 / 60 / 24;
daysRound = Math.floor(days);
hours = (later - now) / 1000 / 60 / 60 - (24 * daysRound);
hoursRound = Math.floor(hours);
minutes = (later - now) / 1000 /60 - (24 * 60 * daysRound) - (60 * hoursRound);
minutesRound = Math.floor(minutes);
seconds = (later - now) / 1000 - (24 * 60 * 60 * daysRound) - (60 * 60 * hoursRound) - (60 * minutesRound);
secondsRound = Math.round(seconds);

if (secondsRound <= 9) {
document.getElementById("g").src = c0.src;
document.getElementById("h").src = eval("c"+secondsRound+".src");
}
else {
document.getElementById("g").src = eval("c"+Math.floor(secondsRound/10)+".src");
document.getElementById("h").src = eval("c"+(secondsRound%10)+".src");
}
if (minutesRound <= 9) {
document.images.d.src = c0.src;
document.images.e.src = eval("c"+minutesRound+".src");
}
else {
document.images.d.src = eval("c"+Math.floor(minutesRound/10)+".src");
document.images.e.src = eval("c"+(minutesRound%10)+".src");
}
if (hoursRound <= 9) {
document.images.y.src = c0.src;
document.images.z.src = eval("c"+hoursRound+".src");
}
else {
document.images.y.src = eval("c"+Math.floor(hoursRound/10)+".src");
document.images.z.src = eval("c"+(hoursRound%10)+".src");
}
if (daysRound <= 9) {
document.images.x.src = c0.src;
document.images.a.src = c0.src;
document.images.b.src = eval("c"+daysRound+".src");
}
if (daysRound <= 99) {
document.images.x.src = c0.src;
document.images.a.src = eval("c"+Math.floor((daysRound/10)%10)+".src");
document.images.b.src = eval("c"+Math.floor(daysRound%10)+".src");
}
if (daysRound <= 999){
document.images.x.src = eval("c"+Math.floor(daysRound/100)+".src");
document.images.a.src = eval("c"+Math.floor((daysRound/10)%10)+".src");
document.images.b.src = eval("c"+Math.floor(daysRound%10)+".src");
}
newtime = window.setTimeout("getTime();", 1000);
}