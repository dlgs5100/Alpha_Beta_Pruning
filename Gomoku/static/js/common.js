$(document).ready(function () {
    
    var chess = document.getElementById("chess");
    var context = chess.getContext("2d"); //context可以看作畫筆
    context.strokeStyle="#bfbfbf";              //畫筆的顏色
    var arrayBoard = [];
    var player;

    //載入棋盤
    window.onload = function(){               //頁面載入完成事件
        loadChessBoard()
        player=1;
    }

    chess.onclick=function(e){

        var col = (e.offsetX/30)|0;   //得到點選的x座標
        var row = (e.offsetY/30)|0;   //得到點選的y座標
        
        returnServer(arrayBoard)
        oneStep(col,row,player);
        if(resultComposition(col,row,player)){
            window.alert('Player '+player.toString()+' win!')
            window.location.reload();
        }
        else
            player = 1-player;
    }
    
    function resultComposition(col,row,player){
        var i=0;
        var array = new Array(8).fill(0);
        for(var rowOffset=-1; rowOffset<=1; rowOffset++){
            for(var colOffset=-1; colOffset<=1; colOffset++){
                if(rowOffset==0 && colOffset==0)
                    continue;
                var count = 1;
                while(count<5){
                    if(row+rowOffset*count<0 || row+rowOffset*count>=15 || col+colOffset*count<0 || col+colOffset*count>=15)
                        break
                    else if(arrayBoard[row+rowOffset*count][col+colOffset*count] == player)
                        count++;
                    else
                        break;
                }
                array[i] = count;
                i++;
            }
        }
        // 八方向
        console.log(array);
        for(var i=0; i<4; i++)
            if(array[i]+array[7-i]>=6)
                return true;
        return false
    
    }

    //這裡player true為玩家   false為電腦（下面會寫）
    function oneStep(col,row,player){
        var color;

        context.beginPath();                              //開始畫圓
        context.arc(15+30*col,15+30*row,13,0,2*Math.PI)       //（x,y,半徑，起始點，終止點2*PI即360度）
        context.closePath();                              //結束畫圓
        
        if(player == 1){
            color="black";                                //玩家是黑色
        }else{
            color="white";                                  //電腦是紅色
        }
        
        context.shadowBlur = 5;
        context.shadowColor = "black";
        context.fillStyle=color;                         //設定填充色
        context.fill();                                  //填充顏色
        
        arrayBoard[row][col] = player.toString();
    }

    function loadChessBoard(){
        for(var i=0;i<15;i++){
            var array = new Array(15).fill('x');
            arrayBoard.push(array)
            
            context.moveTo(15,15+30*i);          //橫線（x，y）起始點
            context.lineTo(435,15+30*i);           //橫線（x，y）終止點
            context.stroke();                              //畫一條線
            
            context.moveTo(15+30*i,15);           //豎線
            context.lineTo(15+30*i,435);
            context.stroke();
        }
    }
    function returnServer(arrayBoard){
        var json_data = JSON.stringify(arrayBoard);
        $.ajax({
            url:"/ajax/board_status/",
            type:'POST',
            dataType:'json',
            // tradition:true,
            data:{'data': json_data},
            success: function (arg) {
            }
        });
    }
});

