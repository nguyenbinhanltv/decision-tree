canvas = document.getElementById("mainCanvas");
ctx = canvas.getContext("2d");

WIDTH = window.innerHeight * 4;
HEIGHT = window.innerHeight;

console.log(tree);

function drawTree() {
  ctx.canvas.width = WIDTH;
  ctx.canvas.height = HEIGHT;
  pos = {
    x: WIDTH / 2,
    y: 10,
  };
  let keys = Object.keys(tree);
  ctx.lineWidth = 2;
  let nodeRoot = new Node(pos, keys[0], "#000", "#fff");
  nodeRoot.draw(ctx);
  let decisions = Object.keys(tree[keys[0]]);
  let space = WIDTH / decisions.length;
  let currentX = 0;
  let paddingX = 10;
  let i = 0;
  for (let decision of decisions) {
    drawNode(
      tree[keys[0]][decision],
      decision,
      nodeRoot,
      {
        x: currentX + space / 2,
        y: nodeRoot.position.y + 150,
      },
      space * i,
      space,
      i
    );
    currentX += space;
    i++;
  }
}

function drawNode(branch, decision, parentPos, pos, start, space, region) {
  let keys = Object.keys(branch);
  ctx.font = "20px Arial";
  ctx.fillStyle = "#000";
  ctx.fillText(decision, pos.x, pos.y - 20);
  let node = new Node(pos, keys[0], "#000", "#fff");
  if (typeof branch[keys[0]] == "string") {
    let lastNode = new Node(pos, branch[keys[0]], "green", "#fff");
    lastNode.draw(ctx);
    ctx.beginPath();
    ctx.strokeStyle = "#000";
    ctx.moveTo(parentPos.getBottom().x, parentPos.getBottom().y);
    ctx.lineTo(lastNode.getTop().x, lastNode.getTop().y);
    ctx.stroke();
    return;
  }
  node.draw(ctx);
  ctx.beginPath();
  ctx.strokeStyle = "#000";
  ctx.moveTo(parentPos.getBottom().x, parentPos.getBottom().y);
  ctx.lineTo(node.getTop().x, node.getTop().y);
  ctx.stroke();

  let decisions = Object.keys(branch[keys[0]]);
  let branchSpace = space / decisions.length;
  let currentX = space * region;
  let i = 0;
  for (let decision of decisions) {
    drawNode(
      branch[keys[0]][decision],
      decision,
      node,
      {
        x: start + branchSpace * i,
        y: parentPos.getBottom().y + 300,
      },
      start + branchSpace * i,
      branchSpace,
      i
    );
    currentX += branchSpace;
    i++;
  }
}

const Node = function (pos, text, background, forecolor) {
  this.position = pos;
  this.text = text;
  this.background = background;
  this.forecolor = forecolor;
  this.width = this.text.length * 11 + 10;
  this.height = 50;
};

Node.prototype.draw = function (ctx) {
  ctx.fillStyle = this.background;
  ctx.strokeStyle = this.forecolor;
  ctx.fillRect(this.position.x, this.position.y, this.width, this.height);
  ctx.font = "20px Arial";
  ctx.fillStyle = this.forecolor;
  ctx.fillText(this.text, this.position.x + 5, this.position.y + 30);
};

Node.prototype.getBottom = function () {
  return {
    x: this.position.x + this.width / 2,
    y: this.position.y + this.height,
  };
};

Node.prototype.getTop = function () {
  return {
    x: this.position.x + this.width / 2,
    y: this.position.y,
  };
};
