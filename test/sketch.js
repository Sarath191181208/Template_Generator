
var WIDTH;
var HEIGHT;

function preload() {
  WIDTH = windowWidth;
  HEIGHT = windowHeight;
}

function setup() {
  pixelDensity(1);
  createCanvas(WIDTH, HEIGHT);

  // translate(windowWidth / 2, windowHeight / 2);
  // colorMode(HSL);
}

function draw() {
  background('#7dc4e8');
  textAlign(CENTER, CENTER);
  textSize(64);
  text('Success....', WIDTH / 2, HEIGHT / 2);
}
