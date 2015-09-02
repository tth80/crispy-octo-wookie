function Map(id) {
    this.ctx = null;
    this.width = 0;
    this.height = 0;
    this.blockSize = 0;
    
    this.init = function(id, blockSize) {
        var c = document.getElementById(id);
        this.width = c.clientWidth;
        this.height = c.clientHeight;
        this.blockSize = blockSize;

        this.ctx = c.getContext('2d');

//        this.ctx.fillstyle = '#000000';
//        this.ctx.fillrect(0, 0, this.width, this.height);
    };

    this.drawGrid = function() {
        this.ctx.strokeStyle = '#303030';
        this.ctx.beginPath();

        for(var y=0;y<this.height;y+=this.blockSize) {
            this.ctx.moveTo(0, y);
            this.ctx.lineTo(this.width, y);

            for(var x=0;x<=this.width;x+=this.blockSize) {
                this.ctx.moveTo(x, 0);
                this.ctx.lineTo(x, y);
            }
        }

        this.ctx.lineWidth = 1;
        this.ctx.stroke();
    };

    this.drawBlock = function(x, y, color) {
        this.ctx.fillStyle = color;
        this.ctx.fillRect(x, y, this.blockSize, this.blockSize);
    }

    this.drawRoom = function() {
        var width=10;
        var height=10;
        
        var room_x = 5;
        var room_y = 10;

        var xlen = room_x + width;
        var ylen = room_y + height;

        this.ctx.strokeStyle = '#ffa0a0';
        this.ctx.fillStyle = '#c0c0c0';

        var paints = 0;

        for(var x=0;x<width;x++) {
            for(var y=0;y<height;y++) {
                var ax = (x + room_x) * this.blockSize;
                var ay = (y + room_y) * this.blockSize;

                this.drawBlock(ax, ay, '#c0c0c0');
            }
        }

        this.ctx.stroke();
    };
};

m = new Map();
m.init('canvasbg', 16);
m.drawGrid();

m = new Map();
m.init('canvas', 16);
m.drawRoom();
