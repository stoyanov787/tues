let myX = 780, myY = 430;

//DEFINING NUMBER OF X AND Y AXIS LINES
const x_lines_number = 2;
const y_lines_number = 2;

const linesList = {
   x_lines = [
      {
         x = 95,
         y = 180,
         width = 310,
         height = 10,
      }
      ,{
         x = 95,
         y = 30,
         width = 310,
         height = 10,
      }
   ]
   , y_lines = [
      {
         x = 95,
         y = 30,
         width = 10,
         height = 160,
      }
      ,{
         x = 395,
         y = 30,
         width = 10,
         height = 75,
      }
   ]
}

let flag = 1, pointer = "x1";

function update() {

   //basic movements
   if (isKeyPressed[87]) {
      flag = 1;
      for (let i = 0; i < x_lines_number; i++) {
         if(checkCollide(linesList.x_lines[i].x , linesList.x_lines[i].y , linesList.x_lines[i].width , linesList.x_lines[i].height, "up")) flag=0; break;
      }
      if(flag) myY -= 2;
   }

   if (isKeyPressed[83]) {
      flag = 1;
      for (let i = 0; i < x_lines_number; i++) {
         if(checkCollide(linesList.x_lines[i].x , linesList.x_lines[i].y , linesList.x_lines[i].width , linesList.x_lines[i].height, "down")) flag=0; break;
      }
      if(flag) myY += 2;
   }
   if (isKeyPressed[68]) {
      flag = 1;
      for (let i = 0; i < x_lines_number; i++) {
         if(checkCollide(linesList.y_lines[i].x , linesList.y_lines[i].y , linesList.y_lines[i].width , linesList.y_lines[i].height, "right")) flag=0; break;
      }
      if(flag) myX += 2;
   }
   if (isKeyPressed[65]) {
      flag = 1;
      for (let i = 0; i < x_lines_number; i++) {
         if(checkCollide(linesList.y_lines[i].x , linesList.y_lines[i].y , linesList.y_lines[i].width , linesList.y_lines[i].height, "right")) flag=0; break;
      }
      if(flag) myX -= 2;
   }
   





   //BORDERS

   if (myX >= 1600) {
      myX -= 2;
   }
   if (myX <= 0) {
      myX += 2;
   }
   if (myY >= 800) {
      myY -= 2;
   }
   if (myY <= 0) {
      myY += 2;
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
   context.fillRect(95, 180, 310, 10); //bottom
   context.fillStyle = 'black';
   context.fillRect(95, 30, 310, 10); // top
   context.fillStyle = 'black';
   context.fillRect(395, 30, 10, 75); //right



}

function keyup(key) {
   console.log("Pressed", key);
}

function mouseup() {
   console.log("Mouse clicked at", mouseX, mouseY);
}

function checkCollide(boxX, boxY, boxWidth, boxHeight, direction) {
   if (direction == "down" && areColliding(myX, myY, myX + 40, myY + 75, boxX, boxY, boxWidth, boxY - 1)) {
      return 1;
   } else return 0;
   if (direction == "up" && areColliding(myX, myY, myX + 40, myY + 75, boxX, boxY + boxHeight - 1, boxWidth, boxY + boxHeight)) {
      return 1;
   } else return 0;
   if (direction == "right" && areColliding(myX, myY, myX + 40, myY + 75, boxX, boxY, 1, boxHeight)) {
      return 1;
   } else return 0;
   if (direction == "left" && areColliding(myX, myY, myX + 40, myY + 75, boxX + boxWidth - 1, boxY, boxX + boxWidth, boxHeight)) {
      return 1;
   } else return 0;
};


