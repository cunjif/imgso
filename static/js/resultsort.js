$(function(){
    $(window).bind('load',function(){
        sortImage();
        $(window).on('scroll',function(){
            sortImage();
        });
    });
});

function sortImage(){
    var boxWidth = $('.res-image').width();
    var width = $(window).width();
    var count = Math.floor(width/boxWidth);
    var boxNum = $('res-image');
    var heightArr = [];
    boxNum.each(function(index,value){
        var imgHeight = boxNum.eq(index).height();
        if(index<count)
            heightArr[index] = imgHeight;
        else{
            var minHeight = Math.min.apply(null,heightArr);
            var minIndex = heightArr.indexOf(minHeight);
            $(value).css({
                "position":"absolute",
                "top":minHeight,
                "left":$('.res-image').eq(minIndex).position().left,
            });
            heightArr[minIndex] += boxNum.eq(index).height();
        }
    });
}