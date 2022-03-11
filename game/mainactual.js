let myX = 780, myY = 430;

function update() {

                 //basic movements
 if(isKeyPressed[87] && checkCollide(95, 180, 310, 10, 95, 30, 310, 10)){
    myY-=2;
 }
 if(isKeyPressed[83] && checkCollide(95, 180, 310, 10, 95, 30, 310, 10)){
    myY+=2;
 }
 if(isKeyPressed[68] && checkCollide(95, 30, 10, 160, 395, 30, 10, 75)){
    myX+=2;
 }
 if(isKeyPressed[65] && checkCollide(95, 30, 10, 160, 395, 30, 10, 75)){
    myX-=2;
 }

 if(myX >= 1600){
    myX-=2;
 }
 if(myX <= 0){
    myX+=2;
 }
 if(myY >= 800){
   myY-=2;
}
if(myY <= 0){
   myY+=2;
}
 
}

function draw() {
    drawImage(mars, 0, 0, 1640, 940);
    drawImage(astronaut, myX, myY, 40, 75);
                                        //1housedrawing
   // context.fillStyle = "gray";
   // context.fillRect(95,40,300, 140) // space                                 
    context.fillStyle = 'black';
    context.fillRect(95, 30, 10, 160); //left
    context.fillStyle = 'black';
    context.fillRect(95, 180, 310, 10); //down
    context.fillStyle = 'black';
    context.fillRect(95, 30, 310, 10); // up
    context.fillStyle = 'black';
    context.fillRect(395, 30, 10, 75); //right
    
   

}

function keyup(key) {
    console.log("Pressed", key);
}

function mouseup() {
    console.log("Mouse clicked at", mouseX, mouseY);
}

function checkCollide(boxX, boxY, boxWidth, boxHeight, direction){
   if(direction == down && !areColliding(myX, myY, myX+40, myY+75, boxX, boxY, boxWidth, boxY-1)){ 
      return 1;
   }
   if(direction == up && !areColliding(myX, myY, myX+40, myY+75, boxX, boxY+boxHeight-1, boxWidth, boxY+boxHeight)){ 
      return 1;
   }
   if(direction == right && !areColliding(myX, myY, myX+40, myY+75, boxX, boxY, 1, boxHeight)){ 
      return 1;
   }
   if(direction == left && !areColliding(myX, myY, myX+40, myY+75, boxX+boxWidth-1, boxY, boxX+boxWidth, boxHeight)){ 
      return 1;
   }
};
